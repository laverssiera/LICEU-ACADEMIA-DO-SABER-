import type { FastifyInstance } from "fastify";
import { ACADEMY_SUBJECTS, publishAcademyEvent } from "../../lib/academy-events.js";

export default async function learningRoutes(app: FastifyInstance) {
  app.post("/academy/learning/adaptive-path/generate", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.LEARNING_PATH_GENERATED, {
      action: "learning.adaptive-path.generate",
      generated_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { generated: true, mode: "adaptive" };
  });

  app.post("/academy/learning/student/runtime/update", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.STUDENT_EVOLUTION_UPDATED, {
      action: "learning.student.runtime.update",
      updated_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { updated: true, target: "student-runtime" };
  });

  app.post("/academy/learning/skills/map", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.KNOWLEDGE_DISTRIBUTED, {
      action: "learning.skills.map",
      mapped_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { mapped: true, source: "ecosystem-needs" };
  });

  app.post("/academy/learning/mission/create", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.PROBLEM_ASSIGNED, {
      action: "learning.mission.create",
      created_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { created: true, mission_type: "real-problem" };
  });

  app.post("/academy/learning/ecosystem/problem/assign", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.PROBLEM_ASSIGNED, {
      action: "learning.ecosystem.problem.assign",
      assigned_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { assigned: true, queue: "ecosystem-problems" };
  });

  app.post("/academy/learning/scientific-mentor/connect", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.KNOWLEDGE_DISTRIBUTED, {
      action: "learning.scientific-mentor.connect",
      connected_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { connected: true, mentor_mode: "scientific" };
  });

  app.get("/academy/learning/student/evolution", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.STUDENT_EVOLUTION_UPDATED, {
      action: "learning.student.evolution.read",
      read_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { level: "advanced", impact_score: 92 };
  });

  app.get("/academy/learning/scientific-profile", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.KNOWLEDGE_DISTRIBUTED, {
      action: "learning.scientific-profile.read",
      read_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { profile: "applied-scientist", readiness: "high" };
  });
}