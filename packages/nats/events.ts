import { connect } from "nats";

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

export async function publishEvent(subject: string, payload: any) {
  const nc = await connect({
    servers: "nats://localhost:4222",
  });

  nc.publish(subject, Buffer.from(JSON.stringify(payload)));
  console.log("event published", subject);
}

export async function publishAcademyEvent(subject: AcademySubject, payload: unknown) {
  await publishEvent(subject, payload);
}
