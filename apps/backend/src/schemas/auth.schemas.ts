import { z } from "zod";

export const registerSchema = z.object({
  email: z
    .string({ message: "email is required" })
    .min(1, "email is required")
    .email("invalid email format"),
  password: z
    .string({ message: "password is required" })
    .min(1, "password is required")
    .min(8, "password must have at least 8 characters"),
});

export type RegisterInput = z.infer<typeof registerSchema>;
