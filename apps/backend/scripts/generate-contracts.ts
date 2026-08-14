import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { zodToJsonSchema } from "zod-to-json-schema";

import { enrollSchema } from "../src/schemas/academy.schemas.js";
import { registerSchema } from "../src/schemas/auth.schemas.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const contractsDir = path.resolve(__dirname, "../contracts");
const docsContractsDir = path.resolve(__dirname, "../../../docs/contracts");
const outputFile = path.join(contractsDir, "backend.contracts.json");
const docsOutputFile = path.join(docsContractsDir, "backend.contracts.json");

const contracts = {
  service: "liceu-academy-api",
  version: "7.0",
  schemas: {
    registerRequest: zodToJsonSchema(registerSchema, "RegisterRequest"),
    enrollRequest: zodToJsonSchema(enrollSchema, "EnrollRequest"),
  },
  endpoints: [
    {
      method: "POST",
      path: "/auth/register",
      requestSchema: "RegisterRequest",
      responses: {
        200: {
          description: "User registered",
        },
        400: {
          description: "Validation error",
        },
      },
    },
    {
      method: "POST",
      path: "/academy/enroll",
      requestSchema: "EnrollRequest",
      responses: {
        200: {
          description: "Enrollment confirmed",
        },
        400: {
          description: "Validation error",
        },
      },
    },
  ],
};

await mkdir(contractsDir, { recursive: true });
await mkdir(docsContractsDir, { recursive: true });
await writeFile(outputFile, JSON.stringify(contracts, null, 2));
await writeFile(docsOutputFile, JSON.stringify(contracts, null, 2));

console.log(`contracts generated: ${outputFile}`);
console.log(`contracts published: ${docsOutputFile}`);
