import assert from "node:assert/strict"
import test from "node:test"

import { processConsumedEvent } from "../src/runtime/process-consumed-event.js"

class MemoryDouble {
  counters = new Map<string, number>()
  lastKey = ""
  lastPayload: unknown = null

  async incrementLearningCounter(key: string): Promise<number> {
    const next = (this.counters.get(key) ?? 0) + 1
    this.counters.set(key, next)
    return next
  }

  async storeLearningMemory<T>(key: string, payload: T): Promise<void> {
    this.lastKey = key
    this.lastPayload = payload
  }
}

class ObservabilityDouble {
  researchPrograms = 0

  registerResearchProgram(): void {
    this.researchPrograms += 1
  }
}

test("processConsumedEvent stores telemetry and publishes routed events", async () => {
  const memory = new MemoryDouble()
  const observability = new ObservabilityDouble()
  const published: Array<{ subject: string; payload: Record<string, unknown> }> = []

  const outputCount = await processConsumedEvent({
    subject: "research.breakthrough",
    received: JSON.stringify({ id: "evt-r2" }),
    publish: (subject, payload) => {
      published.push({ subject, payload })
    },
    memory,
    observability
  })

  assert.equal(outputCount, 2)
  assert.equal(published.length, 2)
  assert.equal(published[0]?.subject, "academy.research.program.created")
  assert.equal(published[1]?.subject, "academy.knowledge.sync")
  assert.equal(memory.counters.get("events:consumed:research.breakthrough"), 1)
  assert.equal(memory.counters.get("events:published:academy.research.program.created"), 1)
  assert.equal(memory.counters.get("events:published:academy.knowledge.sync"), 1)
  assert.equal(memory.lastKey, "events:last:research.breakthrough")
  assert.equal(observability.researchPrograms, 1)
})

test("processConsumedEvent handles invalid json payload and non-research events", async () => {
  const memory = new MemoryDouble()
  const observability = new ObservabilityDouble()
  const published: Array<{ subject: string; payload: Record<string, unknown> }> = []

  const outputCount = await processConsumedEvent({
    subject: "hub.workforce.shortage",
    received: "not-json",
    publish: (subject, payload) => {
      published.push({ subject, payload })
    },
    memory,
    observability
  })

  assert.equal(outputCount, 1)
  assert.equal(published[0]?.subject, "academy.workforce.generated")
  assert.equal(published[0]?.payload.response, "accelerated-workforce-pipeline")
  assert.equal(observability.researchPrograms, 0)

  const stored = memory.lastPayload as { payload?: Record<string, unknown> }
  assert.equal(stored.payload?.raw, "not-json")
})
