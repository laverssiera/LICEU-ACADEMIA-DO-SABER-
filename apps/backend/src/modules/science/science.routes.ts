import type { FastifyInstance } from "fastify";
import { ACADEMY_SUBJECTS, publishAcademyEvent } from "../../lib/academy-events.js";

export default async function scienceRoutes(app: FastifyInstance) {
  app.post("/academy/science/research/create", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.SCIENCE_RESEARCH_CREATED, {
      action: "research.create",
      created_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { created: true, track: "applied-research" };
  });

  app.post("/academy/science/research/validate", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RESEARCH_VALIDATED, {
      action: "research.validate",
      validated_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { validated: true, standard: "ecosystem-impact" };
  });

  app.post("/academy/science/research/publish", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RESEARCH_PROMOTED, {
      action: "research.publish",
      published_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    void publishAcademyEvent(ACADEMY_SUBJECTS.GAMEMKT_CONTENT_PUBLISHED, {
      action: "gamemkt.publish",
      published_at: new Date().toISOString(),
      channel: "gamemkt-science",
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { published: true, channel: "gamemkt-science" };
  });

  app.post("/academy/science/scientific-runtime/run", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "scientific-runtime.run",
      runtime: "scientific",
      executed_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { executed: true, runtime: "scientific" };
  });

  app.post("/academy/science/knowledge/sync", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.KNOWLEDGE_DISTRIBUTED, {
      action: "knowledge.sync",
      synced_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { synced: true, target: "academy-knowledge-graph" };
  });

  app.post("/academy/science/simulation/generate", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.SCIENCE_SIMULATION_GENERATED, {
      action: "simulation.generate",
      generated_at: new Date().toISOString(),
      simulation_type: "advanced-scenario",
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { generated: true, type: "advanced-scenario" };
  });

  app.post("/academy/science/planetary/scenario", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "planetary.scenario",
      executed_at: new Date().toISOString(),
      domain: "planetary-engineering",
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { scenario_ready: true, domain: "planetary-engineering" };
  });

  app.get("/academy/science/research/domains", async () => {
    return {
      domains: [
        "climate-engineering",
        "resilient-cities",
        "oceanic-engineering",
        "autonomous-systems",
      ],
    };
  });
}