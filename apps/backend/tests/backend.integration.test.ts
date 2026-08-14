import assert from "node:assert/strict";
import test from "node:test";

import { buildApp } from "../src/app.js";

test("GET / returns ecosystem metadata", async () => {
  const app = buildApp();
  const response = await app.inject({ method: "GET", url: "/" });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    ecosystem: "LICEU Academia do Saber",
    version: "7.0",
  });

  await app.close();
});

test("GET /academy/dashboard returns KPIs", async () => {
  const app = buildApp();
  const response = await app.inject({ method: "GET", url: "/academy/dashboard" });

  assert.equal(response.statusCode, 200);
  assert.equal(response.json().students_online, 14482);

  await app.close();
});

test("POST /auth/register returns hashed password", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/auth/register",
    payload: {
      email: "student@liceu.ai",
      password: "secure-pass",
    },
  });

  assert.equal(response.statusCode, 200);
  const body = response.json();
  assert.equal(body.success, true);
  assert.equal(body.user.email, "student@liceu.ai");
  assert.notEqual(body.user.password_hash, "secure-pass");

  await app.close();
});

test("POST /auth/login returns JWT token", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/auth/login",
  });

  assert.equal(response.statusCode, 200);
  const body = response.json();
  assert.equal(typeof body.token, "string");
  assert.ok(body.token.length > 20);

  await app.close();
});

test("POST /academy/enroll returns enrollment confirmation", async () => {
  const app = buildApp();
  const payload = { course_id: "course-001" };
  const response = await app.inject({
    method: "POST",
    url: "/academy/enroll",
    payload,
  });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    enrolled: true,
    course_id: payload.course_id,
  });

  await app.close();
});

test("POST /simulation/structural returns simulation metrics", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/simulation/structural",
  });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    simulation: "structural",
    stress_factor: 0.81,
    collapse_probability: 0.03,
    status: "stable",
  });

  await app.close();
});

test("POST /holographic/render returns holographic render payload", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/holographic/render",
  });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    scene: "bim_city",
    fps: 60,
    xr_ready: true,
  });

  await app.close();
});

test("POST /academy/science/research/create returns scientific create payload", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/academy/science/research/create",
  });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    created: true,
    track: "applied-research",
  });

  await app.close();
});

test("POST /academy/interplanetary/habitat/simulate returns habitat simulation payload", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/academy/interplanetary/habitat/simulate",
  });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    simulated: true,
    system: "habitat-engineering",
  });

  await app.close();
});

test("GET /academy/learning/scientific-profile returns learning profile", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "GET",
    url: "/academy/learning/scientific-profile",
  });

  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), {
    profile: "applied-scientist",
    readiness: "high",
  });

  await app.close();
});

test("POST /auth/register without password returns 400", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/auth/register",
    payload: {
      email: "student@liceu.ai",
    },
  });

  assert.equal(response.statusCode, 400);
  assert.deepEqual(response.json(), {
    error: "password is required",
  });

  await app.close();
});

test("POST /academy/enroll without course_id returns 400", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/academy/enroll",
    payload: {},
  });

  assert.equal(response.statusCode, 400);
  assert.deepEqual(response.json(), {
    error: "course_id is required",
  });

  await app.close();
});

test("POST /auth/register with invalid email returns 400", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/auth/register",
    payload: {
      email: "invalid-email",
      password: "secure-pass",
    },
  });

  assert.equal(response.statusCode, 400);
  assert.deepEqual(response.json(), {
    error: "invalid email format",
  });

  await app.close();
});

test("POST /auth/register with short password returns 400", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/auth/register",
    payload: {
      email: "student@liceu.ai",
      password: "1234567",
    },
  });

  assert.equal(response.statusCode, 400);
  assert.deepEqual(response.json(), {
    error: "password must have at least 8 characters",
  });

  await app.close();
});

test("POST /academy/enroll with invalid course_id format returns 400", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "POST",
    url: "/academy/enroll",
    payload: {
      course_id: "invalid-001",
    },
  });

  assert.equal(response.statusCode, 400);
  assert.deepEqual(response.json(), {
    error: "course_id must match course-<id> pattern",
  });

  await app.close();
});

test("GET /auth/login with wrong method returns 404", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "GET",
    url: "/auth/login",
  });

  assert.equal(response.statusCode, 404);

  await app.close();
});

test("GET /simulation/structural with wrong method returns 404", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "GET",
    url: "/simulation/structural",
  });

  assert.equal(response.statusCode, 404);

  await app.close();
});

test("GET unknown route returns 404", async () => {
  const app = buildApp();
  const response = await app.inject({
    method: "GET",
    url: "/unknown-route",
  });

  assert.equal(response.statusCode, 404);

  await app.close();
});
