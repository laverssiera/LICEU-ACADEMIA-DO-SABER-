import { routeEvent, type ConsumedEvent } from "./event-router.js"

interface MemoryOps {
  incrementLearningCounter(key: string): Promise<number>
  storeLearningMemory<T>(key: string, payload: T): Promise<void>
}

interface ObservabilityOps {
  registerResearchProgram(): void
}

interface ProcessConsumedEventInput {
  subject: ConsumedEvent
  received: string
  publish: (subject: string, payload: Record<string, unknown>) => void
  memory: MemoryOps
  observability: ObservabilityOps
}

export async function processConsumedEvent(input: ProcessConsumedEventInput): Promise<number> {
  const { subject, received, publish, memory, observability } = input

  let parsedPayload: Record<string, unknown> = {}

  try {
    parsedPayload = JSON.parse(received) as Record<string, unknown>
  } catch {
    parsedPayload = { raw: received }
  }

  await memory.incrementLearningCounter(`events:consumed:${subject}`)
  await memory.storeLearningMemory(`events:last:${subject}`, {
    payload: parsedPayload,
    received_at: Date.now()
  })

  const emissions = routeEvent(subject, parsedPayload)

  for (const emission of emissions) {
    publish(emission.subject, emission.payload)
    await memory.incrementLearningCounter(`events:published:${emission.subject}`)
  }

  if (subject.startsWith("research.")) {
    observability.registerResearchProgram()
  }

  return emissions.length
}
