import assert from "node:assert/strict"
import test from "node:test"

import { UnifiedObservability } from "../src/observability/unified-observability.js"

test("UnifiedObservability exports civilization brain sync metrics", async () => {
  const observability = new UnifiedObservability()

  observability.registerAcademyBrainSyncSuccess(3, 0.87, 120)
  observability.registerAcademyBrainSyncFailure()

  const metrics = await observability.metrics()

  assert.ok(metrics.includes("civilization_education_brain_sync_total"))
  assert.ok(metrics.includes('status="success"'))
  assert.ok(metrics.includes('status="failure"'))
  assert.ok(metrics.includes("civilization_education_signals_published_total"))
  assert.ok(metrics.includes("civilization_education_global_intelligence_score"))
  assert.ok(metrics.includes("civilization_education_global_events"))
  assert.ok(metrics.includes("civilization_education_last_sync_timestamp_seconds"))
})
