import assert from "node:assert/strict";
import test from "node:test";

import {
  ACADEMY_SUBJECTS,
  __resetAcademyEventsForTests,
  __setAcademyEventsConnectForTests,
  publishAcademyEvent,
} from "../src/lib/academy-events.js";

test("publishAcademyEvent returns false when events are disabled", async () => {
  const previousEnabled = process.env.NATS_EVENTS_ENABLED;
  delete process.env.NATS_EVENTS_ENABLED;

  let connectCalled = false;
  __setAcademyEventsConnectForTests(async () => {
    connectCalled = true;
    throw new Error("should not connect");
  });

  const published = await publishAcademyEvent(ACADEMY_SUBJECTS.LEARNING_PATH_GENERATED, {
    student_id: "STD-001",
  });

  assert.equal(published, false);
  assert.equal(connectCalled, false);

  __resetAcademyEventsForTests();
  if (previousEnabled === undefined) {
    delete process.env.NATS_EVENTS_ENABLED;
  } else {
    process.env.NATS_EVENTS_ENABLED = previousEnabled;
  }
});

test("publishAcademyEvent publishes payload when events are enabled", async () => {
  const previousEnabled = process.env.NATS_EVENTS_ENABLED;
  const previousUrl = process.env.NATS_URL;

  process.env.NATS_EVENTS_ENABLED = "1";
  process.env.NATS_URL = "nats://mock:4222";

  const publishedCalls: Array<{ subject: string; payload: string }> = [];
  const receivedServers: string[] = [];

  __setAcademyEventsConnectForTests(async ({ servers }) => {
    receivedServers.push(String(servers));

    return {
      publish(subject: string, data: Uint8Array) {
        publishedCalls.push({
          subject,
          payload: Buffer.from(data).toString("utf8"),
        });
      },
    } as unknown as import("nats").NatsConnection;
  });

  const payload = { mission_id: "MSN-100", status: "created" };
  const published = await publishAcademyEvent(ACADEMY_SUBJECTS.PROBLEM_ASSIGNED, payload);

  assert.equal(published, true);
  assert.equal(receivedServers[0], "nats://mock:4222");
  assert.equal(publishedCalls.length, 1);
  assert.equal(publishedCalls[0]?.subject, ACADEMY_SUBJECTS.PROBLEM_ASSIGNED);
  assert.deepEqual(JSON.parse(publishedCalls[0]?.payload || "{}"), payload);

  __resetAcademyEventsForTests();

  if (previousEnabled === undefined) {
    delete process.env.NATS_EVENTS_ENABLED;
  } else {
    process.env.NATS_EVENTS_ENABLED = previousEnabled;
  }

  if (previousUrl === undefined) {
    delete process.env.NATS_URL;
  } else {
    process.env.NATS_URL = previousUrl;
  }
});

test("publishAcademyEvent reuses NATS connection across multiple publishes", async () => {
  const previousEnabled = process.env.NATS_EVENTS_ENABLED;
  const previousUrl = process.env.NATS_URL;

  process.env.NATS_EVENTS_ENABLED = "1";
  process.env.NATS_URL = "nats://mock:4222";

  let connectCalls = 0;
  const publishedSubjects: string[] = [];

  __setAcademyEventsConnectForTests(async () => {
    connectCalls += 1;

    return {
      publish(subject: string) {
        publishedSubjects.push(subject);
      },
    } as unknown as import("nats").NatsConnection;
  });

  const firstPublish = await publishAcademyEvent(ACADEMY_SUBJECTS.LEARNING_PATH_GENERATED, {
    student_id: "STD-100",
  });

  const secondPublish = await publishAcademyEvent(ACADEMY_SUBJECTS.STUDENT_EVOLUTION_UPDATED, {
    student_id: "STD-100",
  });

  assert.equal(firstPublish, true);
  assert.equal(secondPublish, true);
  assert.equal(connectCalls, 1);
  assert.deepEqual(publishedSubjects, [
    ACADEMY_SUBJECTS.LEARNING_PATH_GENERATED,
    ACADEMY_SUBJECTS.STUDENT_EVOLUTION_UPDATED,
  ]);

  __resetAcademyEventsForTests();

  if (previousEnabled === undefined) {
    delete process.env.NATS_EVENTS_ENABLED;
  } else {
    process.env.NATS_EVENTS_ENABLED = previousEnabled;
  }

  if (previousUrl === undefined) {
    delete process.env.NATS_URL;
  } else {
    process.env.NATS_URL = previousUrl;
  }
});
