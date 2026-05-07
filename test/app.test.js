const test = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");

const app = require("../src/app");

// ─── ISSUE 0: RBAC base ──────────────────────────────────────────────────────

test("RBAC deve bloquear rota sem x-holding-user-id", async () => {
  const response = await request(app).get("/school/fundamental");
  assert.equal(response.statusCode, 401);
  assert.match(response.body.error, /x-holding-user-id/i);
});

test("RBAC deve permitir leitura com usuario autorizado", async () => {
  const response = await request(app)
    .get("/school/fundamental")
    .set("x-holding-user-id", "HLD-004");
  assert.equal(response.statusCode, 200);
  assert.equal(response.body.title, "Ensino Fundamental (Base Cognitiva)");
});

test("Evento do P&D deve gerar curso automatico no SDK", async () => {
  const publishEvent = await request(app)
    .post("/pd-ia/events/new-technologies")
    .set("x-holding-user-id", "HLD-003")
    .send({
      title: "BIM 6D com IA generativa",
      domain: "BIM",
      level: "avancado",
      workloadHours: 40,
      skillTags: ["bim", "ia", "planejamento"]
    });
  assert.equal(publishEvent.statusCode, 201);
  assert.equal(publishEvent.body.processedEvents, 1);
  assert.equal(publishEvent.body.courses[0].trackName, "tecnico BIM");

  const listCourses = await request(app)
    .get("/sdk/certification/courses")
    .set("x-holding-user-id", "HLD-006");
  assert.equal(listCourses.statusCode, 200);
  assert.ok(Array.isArray(listCourses.body));
  assert.ok(listCourses.body.some((course) => course.title.includes("BIM 6D com IA generativa")));
});

test("RBAC deve negar publicacao de evento para papel sem permissao", async () => {
  const response = await request(app)
    .post("/pd-ia/events/new-technologies")
    .set("x-holding-user-id", "HLD-006")
    .send({ title: "IoT Predial Basico", domain: "IoT" });
  assert.equal(response.statusCode, 403);
  assert.equal(response.body.requiredPermission, "pd_events:publish");
});

test("SDK deve permitir criacao manual de trilha por papel autorizado", async () => {
  const response = await request(app)
    .post("/sdk/certification/tracks")
    .set("x-holding-user-id", "HLD-002")
    .send({
      name: "Trilha BIM Executivo",
      level: "avancado",
      objective: "Formar lideres em planejamento BIM integrado",
      skills: ["bim", "coordenacao", "planejamento"]
    });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.name, "Trilha BIM Executivo");
  assert.equal(response.body.origin, "sdk");
  assert.ok(Array.isArray(response.body.courses));
});

test("Governanca RBAC deve permitir listar usuarios para papel autorizado", async () => {
  const response = await request(app)
    .get("/holding/rbac/users")
    .set("x-holding-user-id", "HLD-002");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
  assert.equal(response.body.length, 6);
  assert.ok(response.body.every((user) => Array.isArray(user.permissions)));
});

test("Governanca RBAC deve negar listar usuarios para papel nao autorizado", async () => {
  const response = await request(app)
    .get("/holding/rbac/users")
    .set("x-holding-user-id", "HLD-004");
  assert.equal(response.statusCode, 403);
  assert.match(response.body.error, /acesso negado/i);
});

// ─── ISSUE 1: Domínio educacional ───────────────────────────────────────────

test("ISSUE 1 — Deve criar um curso no dominio educacional", async () => {
  const response = await request(app)
    .post("/academy/courses")
    .set("x-holding-user-id", "HLD-001")
    .send({ title: "Fundamentos BIM", domain: "BIM", level: "basico" });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.title, "Fundamentos BIM");
});

test("ISSUE 1 — Deve listar cursos criados", async () => {
  const response = await request(app)
    .get("/academy/courses")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
});

// ─── ISSUE 3: Trilhas por monólito ──────────────────────────────────────────

test("ISSUE 3 — Deve listar trilhas por monolito", async () => {
  const response = await request(app)
    .get("/academy/tracks/monolith")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(response.body.archimedes);
});

// ─── ISSUE 4: Core LICEU training ───────────────────────────────────────────

test("ISSUE 4 — Deve retornar trilha Core LICEU obrigatoria", async () => {
  const response = await request(app)
    .get("/academy/training/core-liceu")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(response.body.modules);
  assert.ok(Array.isArray(response.body.modules));
});

// ─── ISSUE 5: John Training Engine ──────────────────────────────────────────

test("ISSUE 5 — John deve identificar areas fracas e sugerir acoes", async () => {
  const response = await request(app)
    .post("/academy/john/train")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-TEST", currentScores: { bim: 40, juridico: 35 }, completedCourses: [] });
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.weakAreas));
  assert.ok(response.body.weakAreas.includes("bim"));
  assert.equal(response.body.recommendedDifficulty, "basico");
});

// ─── ISSUE 6: Score cognitivo ────────────────────────────────────────────────

test("ISSUE 6 — Deve criar score cognitivo de usuario", async () => {
  const response = await request(app)
    .post("/academy/users/USR-COG-001/cognitive-score")
    .set("x-holding-user-id", "HLD-001")
    .send({ skillMatrix: { bim: 80, juridico: 45, vendas: 90 } });
  assert.equal(response.statusCode, 201);
  assert.ok(response.body.cognitive_score > 0);
});

// ─── ISSUE 7: Aprendizado por erro ──────────────────────────────────────────

test("ISSUE 7 — John deve gerar licao a partir de erro", async () => {
  const response = await request(app)
    .post("/academy/john/learn-from-error")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-ERR-001", errorType: "deal", sourceSystem: "Archimedes" });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.generatedLesson.domain, "vendas");
});

// ─── ISSUE 8: Sandbox simulation ────────────────────────────────────────────

test("ISSUE 8 — Deve executar simulacao de sandbox", async () => {
  const response = await request(app)
    .post("/academy/sandbox/simulate")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-SBX-001", simulationType: "venda" });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.monolith, "archimedes");
  assert.ok(response.body.score >= 0);
});

// ─── ISSUE 9: Certificação automática ───────────────────────────────────────

test("ISSUE 9 — Deve certificar usuario com kpi >= 75", async () => {
  const response = await request(app)
    .post("/academy/certification/auto-certify")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-CERT-001", trackId: "vendas", kpiScore: 85 });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "certificado");
});

test("ISSUE 9 — Deve reprovar usuario com kpi < 75 sem aprovacoes extras", async () => {
  const response = await request(app)
    .post("/academy/certification/auto-certify")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-CERT-002", trackId: "juridico", kpiScore: 60 });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "reprovado");
  assert.equal(response.body.issuedAt, null);
});

// ─── ISSUE 10-12: RH / Onboarding ───────────────────────────────────────────

test("ISSUE 10 — Deve criar onboarding com trilhas corretas para corretor/clt", async () => {
  const response = await request(app)
    .post("/academy/hr/onboarding")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-ON-001", name: "João Silva", role: "corretor", contractType: "clt" });
  assert.equal(response.statusCode, 201);
  assert.ok(Array.isArray(response.body.mandatoryTracks));
  assert.ok(response.body.mandatoryTracks.includes("vendas"));
  assert.equal(response.body.trainingStatus, "pending");
});

test("ISSUE 11 — Deve retornar trilhas obrigatorias por funcao", async () => {
  const response = await request(app)
    .get("/academy/hr/mandatory-tracks/corretor")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.mandatoryTracks));
});

test("ISSUE 12 — Deve retornar trilhas para contrato CLT", async () => {
  const response = await request(app)
    .get("/academy/hr/contract-tracks/clt")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.mandatoryTracks));
});

test("ISSUE 12 — Deve retornar 404 para tipo de contrato invalido", async () => {
  const response = await request(app)
    .get("/academy/hr/contract-tracks/freelancer")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 404);
});

// ─── ISSUE 14: Compliance ────────────────────────────────────────────────────

test("ISSUE 14 — Deve listar cursos de compliance obrigatorios", async () => {
  const response = await request(app)
    .get("/academy/legal/compliance-courses")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
  assert.ok(response.body.every((c) => c.mandatory === true || c.mandatory === false));
});

test("ISSUE 14 — Deve registrar aceite juridico e gerar assinatura", async () => {
  const response = await request(app)
    .post("/academy/legal/sign-acceptance")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-LEGAL-001", courseId: 1 });
  assert.equal(response.statusCode, 201);
  assert.match(response.body.signature, /ACEITE/);
});

// ─── ISSUES 15-16: Métricas ──────────────────────────────────────────────────

test("ISSUE 15 — Dashboard deve retornar KPIs", async () => {
  const response = await request(app)
    .get("/academy/metrics/dashboard")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(response.body.kpis);
});

test("ISSUE 16 — Endpoint de correlacao deve retornar array", async () => {
  const response = await request(app)
    .get("/academy/metrics/correlation")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.correlations));
});

// ─── ISSUES 17-19: EdTech Externo ────────────────────────────────────────────

test("ISSUE 17 — Deve criar oferta SaaS", async () => {
  const response = await request(app)
    .post("/academy/saas/courses")
    .set("x-holding-user-id", "HLD-001")
    .send({ title: "BIM para Iniciantes", domain: "BIM", price: 299.9 });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.type, "saas_externo");
});

test("ISSUE 18 — Deve publicar curso no marketplace com status pending_review", async () => {
  const response = await request(app)
    .post("/academy/marketplace/courses")
    .set("x-holding-user-id", "HLD-001")
    .send({ title: "Energia Solar Residencial", domain: "Energia", authorId: "ESP-001" });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "pending_review");
});

test("ISSUE 19 — Deve criar whitelabel corporativo", async () => {
  const response = await request(app)
    .post("/academy/whitelabel/setup")
    .set("x-holding-user-id", "HLD-001")
    .send({ companyId: "CORP-001", companyName: "Construtora Alpha", tracks: ["bim_basico"] });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "active");
});

test("ISSUE 19 — Deve bloquear duplicacao de whitelabel (409)", async () => {
  await request(app)
    .post("/academy/whitelabel/setup")
    .set("x-holding-user-id", "HLD-001")
    .send({ companyId: "CORP-DUP-001", companyName: "Empresa X" });
  const response = await request(app)
    .post("/academy/whitelabel/setup")
    .set("x-holding-user-id", "HLD-001")
    .send({ companyId: "CORP-DUP-001", companyName: "Empresa X" });
  assert.equal(response.statusCode, 409);
});

// ─── ISSUE 22-23: CEFEIDA ────────────────────────────────────────────────────

test("ISSUE 24 — CEFEIDA deve analisar comportamento e retornar adaptive_path", async () => {
  const response = await request(app)
    .post("/academy/cefeida/analyze")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-CEF-001", performanceHistory: [90, 85, 80], errorPatterns: ["juridico"] });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.adaptivePath, "avancado");
});

test("ISSUE 25 — CEFEIDA deve gerar conteudo microlearning", async () => {
  const response = await request(app)
    .post("/academy/cefeida/generate-content")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-CEF-002", domain: "BIM", format: "microlearning" });
  assert.equal(response.statusCode, 201);
  assert.match(response.body.generatedContent.title, /Micro-aula/i);
});

// ─── ISSUES 24-25: Ranking e Dashboard ──────────────────────────────────────

test("ISSUE 27 — Ranking gamificado deve retornar array", async () => {
  const response = await request(app)
    .get("/academy/ranking/gamified")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
});

test("ISSUE 26 — Dashboard institucional deve retornar blocos", async () => {
  const response = await request(app)
    .get("/academy/dashboard/institutional")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(response.body.blocks);
});

// ─── ISSUE 28: RBAC educacional ──────────────────────────────────────────────

test("ISSUE 28 — Deve listar papeis educacionais", async () => {
  const response = await request(app)
    .get("/academy/rbac/roles")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(response.body.ADMIN);
});

// ─── ISSUE 29: RBAC por monólito ─────────────────────────────────────────────

test("ISSUE 29 — Deve retornar permissoes de trilha por monolito (archimedes)", async () => {
  const response = await request(app)
    .get("/academy/monolith-rbac/archimedes")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.required_tracks));
  assert.ok(Array.isArray(response.body.optional_tracks));
  assert.ok(Array.isArray(response.body.admin_only_tracks));
  assert.ok(response.body.required_tracks.includes("cultura_liceu"));
});

test("ISSUE 29 — Deve retornar 404 para monolito inexistente", async () => {
  const response = await request(app)
    .get("/academy/monolith-rbac/monolito-invalido")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 404);
});

// ─── ISSUE 30-31: John DNA + John professor ───────────────────────────────────

test("ISSUE 30 — John deve absorver conhecimento no core_dna", async () => {
  const response = await request(app)
    .post("/academy/john/feed-dna")
    .set("x-holding-user-id", "HLD-001")
    .send({ source: "cefeida_analysis", knowledge: "Usuários com trilha juridica fecham mais contratos", domain: "juridico", confidence: 0.92 });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.entry.status, "absorbed");
});

test("ISSUE 31 — John deve gerar estrutura completa de aula", async () => {
  const response = await request(app)
    .post("/academy/john/teach")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-TEACH-001", topic: "BIM", doubt: "Como usar BIM em obras pequenas?" });
  assert.equal(response.statusCode, 200);
  assert.ok(response.body.lesson.keyPoints);
  assert.ok(response.body.lesson.scenario);
});

// ─── ISSUE 32: Kanban task learning ───────────────────────────────────────────

test("ISSUE 32 — Task blocked deve gerar treinamento com urgencia alta", async () => {
  const response = await request(app)
    .post("/academy/kanban/task-learning")
    .set("x-holding-user-id", "HLD-001")
    .send({ taskId: "TASK-001", userId: "USR-KAN-001", taskDomain: "juridico", taskOutcome: "blocked" });
  assert.equal(response.statusCode, 201);
  assert.ok(response.body.generatedTraining);
  assert.equal(response.body.generatedTraining.urgency, "alta");
});

test("ISSUE 32 — Task completed nao deve gerar treinamento", async () => {
  const response = await request(app)
    .post("/academy/kanban/task-learning")
    .set("x-holding-user-id", "HLD-001")
    .send({ taskId: "TASK-002", userId: "USR-KAN-002", taskDomain: "juridico", taskOutcome: "completed" });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.generatedTraining, null);
});

// ─── ISSUE 33: Feedback loop ──────────────────────────────────────────────────

test("ISSUE 33 — Deve iniciar ciclo de feedback a partir de erro", async () => {
  const response = await request(app)
    .post("/academy/feedback-loop")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-FL-001", errorType: "deal", sourceSystem: "Archimedes" });
  assert.equal(response.statusCode, 201);
  assert.equal(response.body.loop.status, "in_progress");
  assert.equal(response.body.loop.steps.length, 6);
  assert.equal(response.body.loop.steps[0].label, "erro_registrado");
  assert.ok(response.body.loop.steps[0].completedAt);
  assert.equal(response.body.loop.steps[2].completedAt, null);
});

test("ISSUE 33 — Deve listar ciclos de feedback por usuario", async () => {
  // Cria um loop primeiro
  await request(app)
    .post("/academy/feedback-loop")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-FL-LIST", errorType: "audit", sourceSystem: "Sistema" });

  const response = await request(app)
    .get("/academy/feedback-loop/USR-FL-LIST")
    .set("x-holding-user-id", "HLD-001");
  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
  assert.ok(response.body.length >= 1);
});

