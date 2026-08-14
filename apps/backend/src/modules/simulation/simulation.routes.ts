import type { FastifyInstance } from "fastify";
import { ACADEMY_SUBJECTS, publishAcademyEvent } from "../../lib/academy-events.js";

export default async function simulationRoutes(app: FastifyInstance) {
  app.post("/simulation/structural", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.RUNTIME_SIMULATION_EXECUTED, {
      action: "simulation.structural.run",
      simulation: "structural",
      executed_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return {
      simulation: "structural",
      stress_factor: 0.81,
      collapse_probability: 0.03,
      status: "stable",
    };
  });
}
