import bcrypt from "bcrypt";
import "@fastify/jwt";
import type { FastifyInstance } from "fastify";
import { getValidationErrorMessage } from "../../lib/validation.js";
import { registerSchema } from "../../schemas/auth.schemas.js";

export default async function authRoutes(app: FastifyInstance) {
  app.post<{ Body: { email?: string; password?: string } }>("/auth/register", async (req, reply) => {
    const parsed = registerSchema.safeParse(req.body);
    if (!parsed.success) {
      return reply.status(400).send({
        error: getValidationErrorMessage(parsed.error),
      });
    }

    const body = parsed.data;

    const hash = await bcrypt.hash(body.password, 10);

    return {
      success: true,
      user: {
        email: body.email,
        password_hash: hash,
      },
    };
  });

  app.post("/auth/login", async () => {
    return {
      token: app.jwt.sign({
        id: "usr-001",
        role: "student",
      }),
    };
  });
}
