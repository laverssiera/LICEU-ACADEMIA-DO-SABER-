import { connect, type NatsConnection } from "nats";

export const ACADEMY_SUBJECTS = {
  SCIENCE_RESEARCH_CREATED: "academy.science.research.created",
  SCIENCE_SIMULATION_GENERATED: "academy.science.simulation.generated",
  INTERPLANETARY_TRAINING_STARTED: "academy.interplanetary.training.started",
  LEARNING_PATH_GENERATED: "academy.learning.path.generated",
  STUDENT_EVOLUTION_UPDATED: "academy.student.evolution.updated",
  PROBLEM_ASSIGNED: "academy.problem.assigned",
  PROBLEM_SOLVED: "academy.problem.solved",
  RESEARCH_VALIDATED: "academy.research.validated",
  RESEARCH_PROMOTED: "academy.research.promoted",
  KNOWLEDGE_DISTRIBUTED: "academy.knowledge.distributed",
  GAMEMKT_CONTENT_PUBLISHED: "academy.gamemkt.content.published",
  HOLOGRAPHIC_TRAINING_STARTED: "academy.holographic.training.started",
  RUNTIME_SIMULATION_EXECUTED: "academy.runtime.simulation.executed",
} as const;

export type AcademySubject = (typeof ACADEMY_SUBJECTS)[keyof typeof ACADEMY_SUBJECTS];

let ncPromise: Promise<NatsConnection> | null = null;
let connectFn: typeof connect = connect;

function isEventsEnabled() {
  return process.env.NATS_EVENTS_ENABLED === "1";
}

function getServerUrl() {
  return process.env.NATS_URL || "nats://localhost:4222";
}

async function getConnection() {
  if (!ncPromise) {
    ncPromise = connectFn({ servers: getServerUrl() });
  }
  return ncPromise;
}

export async function publishAcademyEvent(subject: AcademySubject, payload: unknown) {
  if (!isEventsEnabled()) {
    return false;
  }

  const nc = await getConnection();
  nc.publish(subject, Buffer.from(JSON.stringify(payload)));
  return true;
}

export function __setAcademyEventsConnectForTests(fn: typeof connect) {
  connectFn = fn;
  ncPromise = null;
}

export function __resetAcademyEventsForTests() {
  connectFn = connect;
  ncPromise = null;
}
