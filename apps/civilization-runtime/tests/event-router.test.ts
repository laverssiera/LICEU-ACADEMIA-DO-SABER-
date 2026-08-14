import assert from "node:assert/strict"
import test from "node:test"

import { CONSUMED_EVENTS, routeEvent } from "../src/runtime/event-router.js"

test("routeEvent maps research.breakthrough to research program and knowledge sync", () => {
  const emissions = routeEvent("research.breakthrough", { id: "evt-r1" }, 123456)

  assert.equal(emissions.length, 2)
  assert.equal(emissions[0]?.subject, "academy.research.program.created")
  assert.equal(emissions[1]?.subject, "academy.knowledge.sync")
  assert.equal(emissions[0]?.payload.generated_at, 123456)
  assert.equal(emissions[1]?.payload.synchronized_at, 123456)
})

test("routeEvent maps archimedes housing issue to workforce generation", () => {
  const emissions = routeEvent("archimedes.housing.problem", { id: "evt-h1" }, 321)

  assert.equal(emissions.length, 2)
  assert.equal(emissions[1]?.subject, "academy.workforce.generated")
  assert.equal(emissions[1]?.payload.role, "housing-systems-engineer")
  assert.equal(emissions[1]?.payload.generated_at, 321)
})

test("routeEvent has at least one output for each consumed event", () => {
  for (const subject of CONSUMED_EVENTS) {
    const emissions = routeEvent(subject, { probe: true })
    assert.ok(emissions.length >= 1, `expected at least one emission for ${subject}`)
  }
})
