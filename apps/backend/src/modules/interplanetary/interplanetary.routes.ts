import type { FastifyInstance } from "fastify";
import { ACADEMY_SUBJECTS, publishAcademyEvent } from "../../lib/academy-events.js";

export default async function interplanetaryRoutes(app: FastifyInstance) {
  app.post("/academy/interplanetary/habitat/simulate", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "interplanetary.habitat.simulate",
      executed_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { simulated: true, system: "habitat-engineering" };
  });

  app.post("/academy/interplanetary/radiation/training", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.INTERPLANETARY_TRAINING_STARTED, {
      action: "interplanetary.radiation.training",
      started_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { training_started: true, module: "radiation-protection" };
  });

  app.post("/academy/interplanetary/low-gravity/training", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.INTERPLANETARY_TRAINING_STARTED, {
      action: "interplanetary.low-gravity.training",
      started_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { training_started: true, module: "low-gravity" };
  });

  app.post("/academy/interplanetary/planetary-engineering/run", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "interplanetary.planetary-engineering.run",
      executed_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { executed: true, runtime: "planetary-engineering" };
  });

  app.post("/academy/interplanetary/orbital-structure/train", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.INTERPLANETARY_TRAINING_STARTED, {
      action: "interplanetary.orbital-structure.train",
      started_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { training_started: true, module: "orbital-structures" };
  });

  app.post("/academy/interplanetary/survival/scenario", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "interplanetary.survival.scenario",
      executed_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { scenario_ready: true, environment: "extreme" };
  });

  app.post("/academy/interplanetary/terraforming/simulation", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "interplanetary.terraforming.simulation",
      executed_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { simulated: true, scope: "terraforming" };
  });

  app.post("/academy/interplanetary/rover/operation/train", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.INTERPLANETARY_TRAINING_STARTED, {
      action: "interplanetary.rover.operation.train",
      started_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return { training_started: true, module: "rover-operations" };
  });
}