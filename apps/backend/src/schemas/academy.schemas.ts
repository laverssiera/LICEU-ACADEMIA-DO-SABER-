import { z } from "zod";

export const enrollSchema = z.object({
  course_id: z
    .string({ message: "course_id is required" })
    .min(1, "course_id is required")
    .regex(/^course-[a-zA-Z0-9_-]+$/, "course_id must match course-<id> pattern"),
});

export type EnrollInput = z.infer<typeof enrollSchema>;
