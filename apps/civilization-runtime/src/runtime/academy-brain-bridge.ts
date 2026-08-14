interface MemoryOps {
  incrementLearningCounter(key: string): Promise<number>
  storeLearningMemory<T>(key: string, payload: T): Promise<void>
}

interface BridgeInput {
  syncUrl: string
  limit: number
  publish: (subject: string, payload: Record<string, unknown>) => void
  memory: MemoryOps
  fetchFn?: typeof fetch
  now?: () => number
}

interface BridgeResult {
  signalsPublished: number
  statePublished: boolean
  collectiveIntelligenceScore: number
  globalEvents: number
}

function asRecord(value: unknown): Record<string, unknown> {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    return value as Record<string, unknown>
  }

  return {}
}

export async function bridgeAcademyCivilizationBrain(input: BridgeInput): Promise<BridgeResult> {
  const fetchFn = input.fetchFn ?? fetch

  const response = await fetchFn(input.syncUrl, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify({ limit: input.limit })
  })

  if (!response.ok) {
    throw new Error(`Academia brain sync failed with status ${response.status}`)
  }

  const payload = asRecord(await response.json())
  const federationNode = asRecord(payload.learning_signals_federation)
  const rawSignals = federationNode.signals
  const signals = Array.isArray(rawSignals) ? rawSignals : []
  let signalsPublished = 0

  await input.memory.incrementLearningCounter("events:consumed:academy.civilization-brain.sync")

  for (const signal of signals) {
    const signalRecord = asRecord(signal)
    const signalPayload = asRecord(signalRecord.signal_payload)
    const subject = String(signalRecord.subject ?? "unknown")
    const events = Number(signalRecord.events ?? 0)
    const cognitionSignal = Number(signalRecord.cognition_signal ?? 0)

    input.publish("civilization.education.signal.propagated", {
      source_runtime: "academia-civilization-brain",
      subject,
      events,
      cognition_signal: cognitionSignal,
      payload: signalPayload,
      propagated_at: (input.now ?? Date.now)()
    })

    signalsPublished += 1
    await input.memory.incrementLearningCounter("events:published:civilization.education.signal.propagated")
  }

  input.publish("civilization.education.global-state.updated", {
    source_runtime: "academia-civilization-brain",
    global_knowledge_state: asRecord(payload.global_knowledge_state),
    collective_educational_intelligence: asRecord(payload.collective_educational_intelligence),
    civilization_learning_intelligence: asRecord(payload.civilization_learning_intelligence),
    temporal_window: asRecord(payload.temporal_window),
    propagated_at: (input.now ?? Date.now)()
  })
  await input.memory.incrementLearningCounter("events:published:civilization.education.global-state.updated")

  await input.memory.storeLearningMemory("civilization:brain:last-sync", {
    synced_at: (input.now ?? Date.now)(),
    signals_published: signalsPublished,
    source_url: input.syncUrl,
    global_state: asRecord(payload.global_knowledge_state)
  })

  return {
    signalsPublished,
    statePublished: true,
    collectiveIntelligenceScore: Number(asRecord(payload.collective_educational_intelligence).score ?? 0),
    globalEvents: Number(asRecord(payload.global_knowledge_state).events ?? 0)
  }
}