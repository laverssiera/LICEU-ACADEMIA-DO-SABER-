import type { FastifyInstance } from "fastify";
import { ACADEMY_SUBJECTS, publishAcademyEvent } from "../../lib/academy-events.js";

export default async function holographicRoutes(app: FastifyInstance) {
  app.post("/holographic/render", async () => {
    void publishAcademyEvent(ACADEMY_SUBJECTS.HOLOGRAPHIC_TRAINING_STARTED, {
      action: "holographic.render",
      scene: "bim_city",
      started_at: new Date().toISOString(),
    }).catch((error: unknown) => app.log.warn({ error }, "nats publish failed"));

    return {
      scene: "bim_city",
      fps: 60,
      xr_ready: true,
    };
  });
}
