const test = require("node:test");
const assert = require("node:assert/strict");
const request = require("supertest");

const app = require("../src/app");

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
    .send({
      title: "IoT Predial Basico",
      domain: "IoT"
    });

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

// ─── ISSUE 1: Domínio educacional unificado ──────────────────────────────────

test("Issue 1: deve criar curso no dominio educacional", async () => {
  const response = await request(app)
    .post("/academy/courses")
    .set("x-holding-user-id", "HLD-002")
    .send({ title: "BIM Avancado", domain: "BIM", level: "avancado", workloadHours: 20, skillTags: ["bim", "revit"] });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.title, "BIM Avancado");
  assert.equal(response.body.domain, "BIM");
});

test("Issue 1: deve listar cursos do dominio educacional", async () => {
  const response = await request(app)
    .get("/academy/courses")
    .set("x-holding-user-id", "HLD-004");

  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
});

// ─── ISSUE 2: Trilhas por monólito ───────────────────────────────────────────

test("Issue 2: deve retornar trilha do monolito Archimedes", async () => {
  const response = await request(app)
    .get("/academy/tracks/monolith/archimedes")
    .set("x-holding-user-id", "HLD-004");

  assert.equal(response.statusCode, 200);
  assert.equal(response.body.name, "Archimedes Track");
});

test("Issue 2: deve retornar todas as trilhas de monolitos", async () => {
  const response = await request(app)
    .get("/academy/tracks/monolith")
    .set("x-holding-user-id", "HLD-004");

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.archimedes);
  assert.ok(response.body.johnCopilot);
});

test("Issue 2: deve retornar 404 para monolito inexistente", async () => {
  const response = await request(app)
    .get("/academy/tracks/monolith/inexistente")
    .set("x-holding-user-id", "HLD-004");

  assert.equal(response.statusCode, 404);
});

// ─── ISSUE 3: Core LICEU Training ────────────────────────────────────────────

test("Issue 3: deve retornar trilha transversal obrigatoria CORE LICEU", async () => {
  const response = await request(app)
    .get("/academy/training/core-liceu")
    .set("x-holding-user-id", "HLD-004");

  assert.equal(response.statusCode, 200);
  assert.equal(response.body.name, "CORE LICEU TRAINING");
  assert.equal(response.body.requiredForOnboarding, true);
  assert.ok(Array.isArray(response.body.modules));
  assert.equal(response.body.modules.length, 5);
});

// ─── ISSUE 4: John Training Engine ───────────────────────────────────────────

test("Issue 4: John deve analisar performance e sugerir trilhas", async () => {
  const response = await request(app)
    .post("/academy/john/train")
    .set("x-holding-user-id", "HLD-004")
    .send({ userId: "USR-001", currentScores: { bim: 45, juridico: 30 }, completedCourses: ["cultura_liceu"] });

  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.weakAreas));
  assert.ok(response.body.weakAreas.includes("bim"));
  assert.ok(response.body.weakAreas.includes("juridico"));
  assert.ok(["basico", "intermediario", "avancado"].includes(response.body.recommendedDifficulty));
});

// ─── ISSUE 5: Score cognitivo ────────────────────────────────────────────────

test("Issue 5: deve criar e recuperar score cognitivo do usuario", async () => {
  const create = await request(app)
    .post("/academy/users/USR-COG-001/cognitive-score")
    .set("x-holding-user-id", "HLD-002")
    .send({ skillMatrix: { bim: 80, juridico: 60, financeiro: 70 }, specializationLevel: "intermediario" });

  assert.equal(create.statusCode, 201);
  assert.equal(create.body.userId, "USR-COG-001");
  assert.ok(typeof create.body.cognitive_score === "number");

  const get = await request(app)
    .get("/academy/users/USR-COG-001/cognitive-score")
    .set("x-holding-user-id", "HLD-002");

  assert.equal(get.statusCode, 200);
  assert.equal(get.body.specializationLevel, "intermediario");
});

// ─── ISSUE 6: Aprendizado baseado em erro ────────────────────────────────────

test("Issue 6: John deve gerar licao automatica baseada em erro real", async () => {
  const response = await request(app)
    .post("/academy/john/learn-from-error")
    .set("x-holding-user-id", "HLD-004")
    .send({ userId: "USR-001", errorType: "deal", sourceSystem: "Archimedes", errorDescription: "Negociacao perdida por falta de argumentos juridicos" });

  assert.equal(response.statusCode, 201);
  assert.ok(response.body.generatedLesson);
  assert.ok(response.body.generatedLesson.title.includes("deal"));
  assert.ok(Array.isArray(response.body.generatedLesson.exercises));
});

// ─── ISSUE 7: Sandbox simulação ──────────────────────────────────────────────

test("Issue 7: deve simular operacao real em sandbox", async () => {
  const response = await request(app)
    .post("/academy/sandbox/simulate")
    .set("x-holding-user-id", "HLD-004")
    .send({ userId: "USR-001", simulationType: "venda", scenario: "venda_alto_padrao" });

  assert.equal(response.statusCode, 201);
  assert.ok(["aprovado", "em_reforco"].includes(response.body.outcome));
  assert.equal(response.body.monolith, "archimedes");
  assert.ok(response.body.feedback);
});

// ─── ISSUE 8: Replay de operações ────────────────────────────────────────────

test("Issue 8: deve registrar e recuperar replay de operacao real", async () => {
  const create = await request(app)
    .post("/academy/replay")
    .set("x-holding-user-id", "HLD-004")
    .send({ userId: "USR-001", replayType: "deal", referenceId: "DEAL-999", sourceSystem: "Archimedes" });

  assert.equal(create.statusCode, 201);
  assert.ok(Array.isArray(create.body.insights));

  const list = await request(app)
    .get("/academy/replay?userId=USR-001")
    .set("x-holding-user-id", "HLD-004");

  assert.equal(list.statusCode, 200);
  assert.ok(list.body.some((r) => r.referenceId === "DEAL-999"));
});

// ─── ISSUE 9: Certificação por performance ───────────────────────────────────

test("Issue 9: deve certificar usuario com KPI alto", async () => {
  const response = await request(app)
    .post("/academy/certification/auto-certify")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-CERT-001", trackId: "archimedes", kpiScore: 85 });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "certificado");
  assert.ok(response.body.issuedAt);
});

test("Issue 9: deve reprovar usuario com KPI baixo sem aprovacao complementar", async () => {
  const response = await request(app)
    .post("/academy/certification/auto-certify")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-CERT-002", trackId: "finance", kpiScore: 50 });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "reprovado");
  assert.equal(response.body.issuedAt, null);
});

// ─── ISSUE 10: Onboarding RH ─────────────────────────────────────────────────

test("Issue 10: deve executar onboarding automatico por funcao e contrato", async () => {
  const response = await request(app)
    .post("/academy/hr/onboarding")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-HR-001", name: "Lucas Oliveira", role: "corretor", contractType: "clt" });

  assert.equal(response.statusCode, 201);
  assert.ok(Array.isArray(response.body.mandatoryTracks));
  assert.ok(response.body.mandatoryTracks.includes("cultura_liceu"));
  assert.equal(response.body.trainingStatus, "pending");
});

// ─── ISSUE 11: Trilha obrigatória por função ──────────────────────────────────

test("Issue 11: deve retornar trilhas obrigatorias por funcao", async () => {
  const response = await request(app)
    .get("/academy/hr/mandatory-tracks/financeiro")
    .set("x-holding-user-id", "HLD-001");

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.mandatoryTracks.includes("cea"));
  assert.ok(response.body.mandatoryTracks.includes("compliance"));
});

// ─── ISSUE 12: Controle CLT + PJ ─────────────────────────────────────────────

test("Issue 12: deve retornar trilhas obrigatorias para PJ", async () => {
  const response = await request(app)
    .get("/academy/hr/contract-tracks/pj")
    .set("x-holding-user-id", "HLD-001");

  assert.equal(response.statusCode, 200);
  assert.equal(response.body.contractType, "PJ");
  assert.ok(response.body.mandatoryTracks.includes("nao_circunvencao"));
  assert.ok(response.body.mandatoryTracks.includes("lgpd"));
});

// ─── ISSUES 13-14: Compliance + Aceite jurídico ───────────────────────────────

test("Issue 13: deve listar cursos de compliance obrigatorios", async () => {
  const response = await request(app)
    .get("/academy/legal/compliance-courses")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.length >= 5);
  assert.ok(response.body.every((c) => c.mandatory === true));
});

test("Issue 14: deve registrar aceite juridico educacional", async () => {
  const response = await request(app)
    .post("/academy/legal/sign-acceptance")
    .set("x-holding-user-id", "HLD-002")
    .send({ userId: "USR-LEGAL-001", courseId: 1 });

  assert.equal(response.statusCode, 201);
  assert.ok(response.body.signature.startsWith("ACEITE-"));
  assert.equal(response.body.courseId, 1);
});

// ─── ISSUE 15: Dashboard educacional ─────────────────────────────────────────

test("Issue 15: deve retornar dashboard de metricas educacionais", async () => {
  const response = await request(app)
    .get("/academy/metrics/dashboard")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.kpis);
  assert.ok(typeof response.body.kpis.totalEnrollments === "number");
  assert.ok(Array.isArray(response.body.recentEvents));
});

// ─── ISSUE 16: Correlação com resultados reais ────────────────────────────────

test("Issue 16: deve retornar correlacao de treinamento com resultado real", async () => {
  const response = await request(app)
    .get("/academy/metrics/correlation")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body.correlations));
  assert.ok(response.body.analyzedAt);
});

// ─── ISSUES 17-19: EdTech externo ────────────────────────────────────────────

test("Issue 17: deve criar oferta SaaS de curso externo", async () => {
  const response = await request(app)
    .post("/academy/saas/courses")
    .set("x-holding-user-id", "HLD-002")
    .send({ title: "BIM para Iniciantes", domain: "BIM", price: 299.9, level: "basico", certificationIncluded: true });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.type, "saas_externo");
  assert.equal(response.body.certificationIncluded, true);
});

test("Issue 18: deve publicar curso no marketplace", async () => {
  const response = await request(app)
    .post("/academy/marketplace/courses")
    .set("x-holding-user-id", "HLD-002")
    .send({ title: "Energia Solar Residencial", domain: "Energia", authorId: "ESP-001", authorType: "especialista", price: 199 });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "pending_review");
  assert.equal(response.body.type, "marketplace");
});

test("Issue 19: deve configurar white-label corporativo", async () => {
  const response = await request(app)
    .post("/academy/whitelabel/setup")
    .set("x-holding-user-id", "HLD-001")
    .send({ companyId: "CORP-001", companyName: "Construtora Alpha", tracks: ["bim_basico", "opera"] });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.status, "active");
  assert.equal(response.body.companyName, "Construtora Alpha");
});

// ─── ISSUES 20-21: Eventos NATS ──────────────────────────────────────────────

test("Issues 20-21: deve recuperar eventos educacionais emitidos", async () => {
  // Trigger an enrollment to generate events
  await request(app)
    .post("/academy/hr/onboarding")
    .set("x-holding-user-id", "HLD-001")
    .send({ userId: "USR-EVT-001", role: "tecnico", contractType: "clt" });

  const response = await request(app)
    .get("/academy/events")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
  assert.ok(response.body.some((e) => e.type === "academy.enrolled"));
});

// ─── ISSUES 22-23: CEFEIDA ───────────────────────────────────────────────────

test("Issue 22: CEFEIDA deve analisar comportamento de estudo", async () => {
  const response = await request(app)
    .post("/academy/cefeida/analyze")
    .set("x-holding-user-id", "HLD-003")
    .send({ userId: "USR-CEFEIDA-001", performanceHistory: [70, 55, 80, 60], errorPatterns: ["juridico", "financeiro"] });

  assert.equal(response.statusCode, 201);
  assert.ok(typeof response.body.averagePerformance === "number");
  assert.ok(["basico", "intermediario", "avancado"].includes(response.body.adaptivePath));
  assert.ok(Array.isArray(response.body.recommendations));
});

test("Issue 23: CEFEIDA deve gerar conteudo dinamico adaptativo", async () => {
  const response = await request(app)
    .post("/academy/cefeida/generate-content")
    .set("x-holding-user-id", "HLD-003")
    .send({ userId: "USR-CEFEIDA-001", domain: "BIM", format: "microlearning", targetLevel: "basico" });

  assert.equal(response.statusCode, 201);
  assert.ok(response.body.generatedContent.title.includes("Micro-aula"));
  assert.equal(response.body.generatedContent.estimatedDuration, "15min");
});

// ─── ISSUE 24: Tela institucional ────────────────────────────────────────────

test("Issue 24: deve retornar dashboard institucional completo", async () => {
  const response = await request(app)
    .get("/academy/dashboard/institutional")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.blocks);
  assert.ok(typeof response.body.blocks.totalTracks === "number");
  assert.ok(Array.isArray(response.body.blocks.rankingTop10));
});

// ─── ISSUE 25: Ranking gamificado ────────────────────────────────────────────

test("Issue 25: deve retornar ranking gamificado com XP e nivel", async () => {
  // Seed a gamification session
  await request(app)
    .post("/academy/gamification/start")
    .set("x-holding-user-id", "HLD-002")
    .send({ studentId: "USR-RANK-001", mode: "mission" });

  const response = await request(app)
    .get("/academy/ranking/gamified")
    .set("x-holding-user-id", "HLD-002");

  assert.equal(response.statusCode, 200);
  assert.ok(Array.isArray(response.body));
  if (response.body.length > 0) {
    assert.ok(response.body[0].xp !== undefined);
    assert.ok(response.body[0].level);
    assert.ok(response.body[0].position === 1);
  }
});

// ─── ISSUES 26-27: RBAC educacional ──────────────────────────────────────────

test("Issues 26-27: deve retornar papeis RBAC educacionais", async () => {
  const response = await request(app)
    .get("/academy/rbac/roles")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.ADMIN);
  assert.ok(response.body.INSTRUTOR);
  assert.ok(response.body.COLABORADOR);
  assert.ok(response.body.CLIENTE_EXTERNO);
});

test("Issues 26-27: deve retornar papel especifico com permissoes", async () => {
  const response = await request(app)
    .get("/academy/rbac/roles/INSTRUTOR")
    .set("x-holding-user-id", "HLD-006");

  assert.equal(response.statusCode, 200);
  assert.equal(response.body.role, "INSTRUTOR");
  assert.ok(Array.isArray(response.body.permissions));
});

// ─── ISSUE 28: John DNA Feed ──────────────────────────────────────────────────

test("Issue 28: deve alimentar core_dna do John", async () => {
  const response = await request(app)
    .post("/academy/john/feed-dna")
    .set("x-holding-user-id", "HLD-001")
    .send({ source: "academia", knowledge: "Corretores que concluem trilha juridica fecham 32% mais contratos", domain: "juridico", confidence: 0.92 });

  assert.equal(response.statusCode, 201);
  assert.match(response.body.message, /core_dna/i);
  assert.equal(response.body.entry.status, "absorbed");
});

// ─── ISSUE 29: John como professor ───────────────────────────────────────────

test("Issue 29: John deve gerar aula e responder duvidas", async () => {
  const response = await request(app)
    .post("/academy/john/teach")
    .set("x-holding-user-id", "HLD-004")
    .send({ userId: "USR-001", topic: "Contratos Imobiliarios", doubt: "Qual a diferenca entre promessa e contrato definitivo?" });

  assert.equal(response.statusCode, 200);
  assert.ok(response.body.lesson);
  assert.ok(Array.isArray(response.body.lesson.keyPoints));
  assert.equal(response.body.answeredDoubt, "Qual a diferenca entre promessa e contrato definitivo?");
});

// ─── ISSUE 30: Kanban task learning ──────────────────────────────────────────

test("Issue 30: task bloqueada deve gerar treinamento de reforco", async () => {
  const response = await request(app)
    .post("/academy/kanban/task-learning")
    .set("x-holding-user-id", "HLD-004")
    .send({ taskId: "TASK-101", userId: "USR-001", taskTitle: "Elaborar contrato de permuta", taskDomain: "juridico", taskOutcome: "blocked" });

  assert.equal(response.statusCode, 201);
  assert.ok(response.body.generatedTraining);
  assert.equal(response.body.generatedTraining.urgency, "alta");
  assert.match(response.body.recommendation, /refor/i);
});

test("Issue 30: task concluida nao deve gerar treinamento", async () => {
  const response = await request(app)
    .post("/academy/kanban/task-learning")
    .set("x-holding-user-id", "HLD-004")
    .send({ taskId: "TASK-102", userId: "USR-001", taskTitle: "Analise de viabilidade", taskDomain: "financeiro", taskOutcome: "completed" });

  assert.equal(response.statusCode, 201);
  assert.equal(response.body.generatedTraining, null);
});
