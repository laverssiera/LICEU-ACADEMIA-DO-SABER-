import assert from "node:assert/strict"
import test from "node:test"

import { bridgeAcademyCivilizationBrain } from "../src/runtime/academy-brain-bridge.js"

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

test("bridgeAcademyCivilizationBrain propagates federated educational signals and global state", async () => {
  const memory = new MemoryDouble()
  const published: Array<{ subject: string; payload: Record<string, unknown> }> = []

  const result = await bridgeAcademyCivilizationBrain({
    syncUrl: "http://academia.local/sync",
    limit: 10,
    publish: (subject, payload) => {
      published.push({ subject, payload })
    },
    memory,
    fetchFn: async () => {
      return {
        ok: true,
        status: 200,
        json: async () => ({
          learning_signals_federation: {
            signals: [
              {
                subject: "astrofederacao",
                events: 8,
                cognition_signal: 0.91,
                signal_payload: {
                  avg_progression: 0.92,
                  avg_retention: 0.89
                }
              },
              {
                subject: "engenharia",
                events: 5,
                cognition_signal: 0.86,
                signal_payload: {
                  avg_progression: 0.87,
                  avg_retention: 0.84
                }
              }
            ]
          },
          global_knowledge_state: {
            events: 13,
            subjects: 2,
            students: 9
          },
          collective_educational_intelligence: {
            score: 0.88,
            status: "active"
          },
          civilization_learning_intelligence: {
            sovereign: true
          },
          temporal_window: {
            first_event_at: "2026-01-01T00:00:00Z",
            last_event_at: "2026-01-02T00:00:00Z"
          }
        })
      } as Response
    },
    now: () => 1234
  })

  assert.equal(result.signalsPublished, 2)
  assert.equal(result.statePublished, true)
  assert.equal(result.collectiveIntelligenceScore, 0.88)
  assert.equal(result.globalEvents, 13)
  assert.equal(published.length, 3)
  assert.equal(published[0]?.subject, "civilization.education.signal.propagated")
  assert.equal(published[1]?.subject, "civilization.education.signal.propagated")
  assert.equal(published[2]?.subject, "civilization.education.global-state.updated")
  assert.equal(memory.counters.get("events:consumed:academy.civilization-brain.sync"), 1)
  assert.equal(memory.counters.get("events:published:civilization.education.signal.propagated"), 2)
  assert.equal(memory.counters.get("events:published:civilization.education.global-state.updated"), 1)
  assert.equal(memory.lastKey, "civilization:brain:last-sync")
})

test("bridgeAcademyCivilizationBrain throws on non-success status", async () => {
  const memory = new MemoryDouble()

  await assert.rejects(
    bridgeAcademyCivilizationBrain({
      syncUrl: "http://academia.local/sync",
      limit: 10,
      publish: () => {},
      memory,
      fetchFn: async () => {
        return {
          ok: false,
          status: 503,
          json: async () => ({})
        } as Response
      }
    }),
    /status 503/
  )
})
