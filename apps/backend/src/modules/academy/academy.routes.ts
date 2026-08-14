import type { FastifyInstance } from "fastify";
import { getValidationErrorMessage } from "../../lib/validation.js";
import { enrollSchema } from "../../schemas/academy.schemas.js";

export default async function academyRoutes(app: FastifyInstance) {
  app.get("/academy/dashboard", async () => {
    return {
      students_online: 14482,
      active_courses: 892,
      active_simulations: 212,
      holographic_rooms: 22,
      ai_accuracy: 98,
    };
  });

  app.post<{ Body: { course_id?: string } }>("/academy/enroll", async (req, reply) => {
    const parsed = enrollSchema.safeParse(req.body);
    if (!parsed.success) {
      return reply.status(400).send({
        error: getValidationErrorMessage(parsed.error),
      });
    }

    return {
      enrolled: true,
      course_id: parsed.data.course_id,
    };
  });
}
