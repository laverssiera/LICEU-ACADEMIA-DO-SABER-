import cors from "@fastify/cors";
import jwt from "@fastify/jwt";
import websocket from "@fastify/websocket";
import Fastify from "fastify";

import academyRoutes from "./modules/academy/academy.routes.js";
import authRoutes from "./modules/auth/auth.routes.js";
import holographicRoutes from "./modules/holographic/holographic.routes.js";
import interplanetaryRoutes from "./modules/interplanetary/interplanetary.routes.js";
import learningRoutes from "./modules/learning/learning.routes.js";
import scienceRoutes from "./modules/science/science.routes.js";
import simulationRoutes from "./modules/simulation/simulation.routes.js";

export function buildApp() {
  const app = Fastify({ logger: true });

  app.register(cors, { origin: true });
  app.register(jwt, { secret: process.env.JWT_SECRET || "liceu" });
  app.register(websocket);

  app.register(authRoutes);
  app.register(academyRoutes);
  app.register(scienceRoutes);
  app.register(interplanetaryRoutes);
  app.register(learningRoutes);
  app.register(simulationRoutes);
  app.register(holographicRoutes);

  app.get("/", async () => ({
    ecosystem: "LICEU Academia do Saber",
    version: "7.0",
  }));

  return app;
}