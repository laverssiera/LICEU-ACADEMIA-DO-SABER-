const express = require("express");
const {
  school,
  enrollments,
  gamificationSessions,
  labResults,
  evaluations,
  technologyEvents,
  certificationTracks,
  generatedCourses,
  holdingUsers,
  rolePermissions,
  courses,
  modules,
  lessons,
  progress,
  academyCertifications,
  monolithTracks,
  coreLiceuTraining,
  cognitiveScores,
  errorLessons,
  sandboxSimulations,
  replays,
  performanceCertifications,
  onboardings,
  mandatoryTracksByRole,
  contractTracks,
  complianceCourses,
  legalAcceptances,
  academyEvents,
  emitAcademyEvent,
  cefeidaAnalyses,
  dynamicContents,
  saasOffers,
  marketplaceCourses,
  whitelabels,
  educationalRoles,
  johnDnaFeed,
  taskLearnings
} = require("./data");

const app = express();
app.use(express.json());

function authenticateHoldingUser(req, res, next) {
  const userId = req.header("x-holding-user-id");

  if (!userId) {
    return res.status(401).json({
      error: "Header x-holding-user-id e obrigatorio para RBAC da Holding."
    });
  }

  const holdingUser = holdingUsers.find((user) => user.id === userId);
  if (!holdingUser) {
    return res.status(401).json({
      error: "Usuario da Holding nao encontrado para o RBAC informado."
    });
  }

  req.holdingUser = holdingUser;
  return next();
}

function authorize(resource, action) {
  return (req, res, next) => {
    const permissions = rolePermissions[req.holdingUser.role] || [];
    const requiredPermission = `${resource}:${action}`;

    if (permissions.includes("*") || permissions.includes(requiredPermission)) {
      return next();
    }

    return res.status(403).json({
      error: "Acesso negado pelo RBAC da Holding.",
      requiredPermission,
      role: req.holdingUser.role
    });
  };
}

function withPermission(resource, action, handler) {
  return [authenticateHoldingUser, authorize(resource, action), handler];
}

function mapTechnologyToTrack(domain, title) {
  const normalized = `${String(domain || "")} ${String(title || "")}`.toLowerCase();

  if (normalized.includes("energia") || normalized.includes("solar") || normalized.includes("microgrid")) {
    return "tecnico energia solar microgrid";
  }

  if (normalized.includes("bim") || normalized.includes("modelagem")) {
    return "tecnico BIM";
  }

  if (normalized.includes("iot") || normalized.includes("automacao") || normalized.includes("predial")) {
    return "tecnico IoT construcao";
  }

  if (normalized.includes("manutencao")) {
    return "tecnico manutencao predial";
  }

  return "tecnico industrializacao construcao";
}

function createCourseFromTechnology(eventData) {
  const trackName = mapTechnologyToTrack(eventData.domain, eventData.title);
  const course = {
    id: generatedCourses.length + 1,
    sourceEventId: eventData.id,
    trackName,
    title: `Curso Auto: ${eventData.title}`,
    domain: eventData.domain,
    skillTags: eventData.skillTags,
    workloadHours: eventData.workloadHours,
    level: eventData.level,
    status: "generated",
    createdAt: new Date().toISOString()
  };

  generatedCourses.push(course);

  let track = certificationTracks.find((item) => item.name === trackName);
  if (!track) {
    track = {
      id: certificationTracks.length + 1,
      name: trackName,
      origin: "sdk",
      courses: [],
      updatedAt: new Date().toISOString()
    };
    certificationTracks.push(track);
  }

  track.courses.push({
    courseId: course.id,
    title: course.title,
    level: course.level,
    workloadHours: course.workloadHours
  });
  track.updatedAt = new Date().toISOString();

  return course;
}

app.get("/", (_req, res) => {
  res.json({
    project: "LICEU ENGENHARIA - LICEU 6.0",
    mission: "Tornar o aprendizado uma constancia vitalicia (3 a 120 anos)",
    status: "online",
    auth: "RBAC Holding (header x-holding-user-id)"
  });
});

app.get("/school/fundamental", ...withPermission("school", "read", (_req, res) => {
  res.json(school.fundamental);
}));

app.get("/school/high-school", ...withPermission("school", "read", (_req, res) => {
  res.json(school.highSchool);
}));

app.get("/school/technical", ...withPermission("school", "read", (_req, res) => {
  res.json(school.technical);
}));

app.post("/school/enroll", ...withPermission("school", "enroll", (req, res) => {
  const { name, age, track } = req.body;

  if (!name || typeof age !== "number") {
    return res.status(400).json({
      error: "Campos obrigatorios: name (string) e age (number)."
    });
  }

  const enrollment = {
    id: enrollments.length + 1,
    name,
    age,
    track: track || "recomendacao_automatica",
    createdAt: new Date().toISOString()
  };

  enrollments.push(enrollment);
  return res.status(201).json(enrollment);
}));

app.post("/academy/gamification/start", ...withPermission("academy_gamification", "write", (req, res) => {
  const { studentId, mode } = req.body;

  if (!studentId) {
    return res.status(400).json({ error: "studentId e obrigatorio." });
  }

  const session = {
    id: gamificationSessions.length + 1,
    studentId,
    mode: mode || "mission",
    score: 0,
    status: "started",
    createdAt: new Date().toISOString()
  };

  gamificationSessions.push(session);
  return res.status(201).json(session);
}));

app.post("/academy/gamification/visit", ...withPermission("academy_gamification", "write", (req, res) => {
  const { sessionId, missionPoints } = req.body;
  const session = gamificationSessions.find((item) => item.id === sessionId);

  if (!session) {
    return res.status(404).json({ error: "Sessao de gamificacao nao encontrada." });
  }

  session.score += Number(missionPoints) || 10;
  return res.json(session);
}));

app.get("/academy/gamification/ranking", ...withPermission("academy_gamification", "read", (_req, res) => {
  const ranking = [...gamificationSessions]
    .sort((a, b) => b.score - a.score)
    .map((item, index) => ({
      position: index + 1,
      sessionId: item.id,
      studentId: item.studentId,
      score: item.score
    }));

  res.json(ranking);
}));

app.post("/academy/lab/simulate", ...withPermission("academy_lab", "write", (req, res) => {
  const { studentId, simulationType } = req.body;

  if (!studentId || !simulationType) {
    return res.status(400).json({
      error: "Campos obrigatorios: studentId e simulationType."
    });
  }

  const result = {
    id: labResults.length + 1,
    studentId,
    simulationType,
    outcome: "approved",
    score: Math.floor(Math.random() * 31) + 70,
    createdAt: new Date().toISOString()
  };

  labResults.push(result);
  return res.status(201).json(result);
}));

app.post("/academy/lab/material-test", ...withPermission("academy_lab", "write", (req, res) => {
  const { studentId, material } = req.body;

  if (!studentId || !material) {
    return res.status(400).json({
      error: "Campos obrigatorios: studentId e material."
    });
  }

  const result = {
    id: labResults.length + 1,
    studentId,
    simulationType: "material-test",
    material,
    resistanceIndex: Math.floor(Math.random() * 41) + 60,
    createdAt: new Date().toISOString()
  };

  labResults.push(result);
  return res.status(201).json(result);
}));

app.get("/academy/lab/results", ...withPermission("academy_lab", "read", (_req, res) => {
  res.json(labResults);
}));

app.post("/john/academy/recommend", ...withPermission("john_ai", "execute", (req, res) => {
  const { age } = req.body;

  if (typeof age !== "number") {
    return res.status(400).json({ error: "age (number) e obrigatorio." });
  }

  let recommendation = "tecnico profissional";
  if (age <= 10) recommendation = "base cognitiva";
  else if (age <= 14) recommendation = "ciencia aplicada";
  else if (age <= 17) recommendation = "medio tecnico";

  return res.json({ age, recommendation });
}));

app.post("/john/academy/evaluate", ...withPermission("john_ai", "execute", (req, res) => {
  const { studentId, cognitiveScore, practicalScore } = req.body;

  if (!studentId || typeof cognitiveScore !== "number" || typeof practicalScore !== "number") {
    return res.status(400).json({
      error: "Campos obrigatorios: studentId, cognitiveScore, practicalScore."
    });
  }

  const average = Number(((cognitiveScore + practicalScore) / 2).toFixed(2));
  const evaluation = {
    id: evaluations.length + 1,
    studentId,
    cognitiveScore,
    practicalScore,
    average,
    status: average >= 70 ? "aprovado" : "em_reforco",
    createdAt: new Date().toISOString()
  };

  evaluations.push(evaluation);
  return res.status(201).json(evaluation);
}));

app.post("/john/academy/career-path", ...withPermission("john_ai", "execute", (req, res) => {
  const { interests = [] } = req.body;

  if (!Array.isArray(interests)) {
    return res.status(400).json({ error: "interests deve ser um array de strings." });
  }

  const map = {
    energia: "tecnico energia solar microgrid",
    obras: "tecnico em planejamento obra",
    modelagem: "tecnico BIM",
    automacao: "tecnico IoT construcao"
  };

  const suggestions = interests
    .map((interest) => map[String(interest).toLowerCase()])
    .filter(Boolean);

  return res.json({
    interests,
    suggestions: suggestions.length ? suggestions : school.technical.tracks.slice(0, 3)
  });
}));

app.post("/john/academy/learning-plan", ...withPermission("john_ai", "execute", (req, res) => {
  const { studentId, goal } = req.body;

  if (!studentId || !goal) {
    return res.status(400).json({ error: "studentId e goal sao obrigatorios." });
  }

  return res.json({
    studentId,
    goal,
    plan: [
      "Diagnostico cognitivo inicial",
      "Modulo teorico interdisciplinar",
      "Missao pratica gamificada",
      "Simulacao no laboratorio virtual",
      "Avaliacao continua e certificacao"
    ]
  });
}));

app.get("/sdk/certification/tracks", ...withPermission("certification_sdk", "read", (_req, res) => {
  res.json(certificationTracks);
}));

app.post("/sdk/certification/tracks", ...withPermission("certification_sdk", "write", (req, res) => {
  const { name, level = "intermediario", objective, skills = [] } = req.body;

  if (!name || !objective) {
    return res.status(400).json({
      error: "Campos obrigatorios: name e objective."
    });
  }

  if (!Array.isArray(skills)) {
    return res.status(400).json({
      error: "skills deve ser um array de strings."
    });
  }

  const newTrack = {
    id: certificationTracks.length + 1,
    name,
    level,
    objective,
    skills,
    origin: "sdk",
    courses: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };

  certificationTracks.push(newTrack);
  return res.status(201).json(newTrack);
}));

app.get("/sdk/certification/courses", ...withPermission("certification_sdk", "read", (_req, res) => {
  res.json(generatedCourses);
}));

app.get("/pd-ia/events/new-technologies", ...withPermission("pd_events", "read", (_req, res) => {
  res.json(technologyEvents);
}));

app.post("/pd-ia/events/new-technologies", ...withPermission("pd_events", "publish", (req, res) => {
  const incomingEvents = Array.isArray(req.body) ? req.body : [req.body];
  const createdEvents = [];
  const createdCourses = [];

  for (let index = 0; index < incomingEvents.length; index += 1) {
    const event = incomingEvents[index];
    if (!event || !event.title || !event.domain) {
      return res.status(400).json({
        error: "Cada evento precisa de title e domain.",
        invalidIndex: index
      });
    }

    const normalizedEvent = {
      id: technologyEvents.length + 1,
      title: String(event.title),
      domain: String(event.domain),
      level: event.level || "intermediario",
      workloadHours: Number(event.workloadHours) || 24,
      skillTags: Array.isArray(event.skillTags) ? event.skillTags : [],
      source: "P&D.IA",
      consumedBy: req.holdingUser.id,
      createdAt: new Date().toISOString()
    };

    technologyEvents.push(normalizedEvent);
    createdEvents.push(normalizedEvent);

    const generatedCourse = createCourseFromTechnology(normalizedEvent);
    createdCourses.push(generatedCourse);
  }

  return res.status(201).json({
    message: "Eventos consumidos e cursos gerados automaticamente.",
    processedEvents: createdEvents.length,
    events: createdEvents,
    courses: createdCourses
  });
}));

app.get("/holding/rbac/users", authenticateHoldingUser, (req, res) => {
  if (!["holding_admin", "academy_director", "auditor"].includes(req.holdingUser.role)) {
    return res.status(403).json({
      error: "Acesso negado para consultar usuarios RBAC.",
      role: req.holdingUser.role
    });
  }

  return res.json(
    holdingUsers.map((user) => ({
      ...user,
      permissions: rolePermissions[user.role] || []
    }))
  );
});

// ─── ISSUE 1: Domínio educacional unificado ─────────────────────────────────

app.get("/academy/courses", ...withPermission("academy_domain", "read", (_req, res) => {
  res.json(courses);
}));

app.post("/academy/courses", ...withPermission("academy_domain", "write", (req, res) => {
  const { title, trackId, domain, level, workloadHours, skillTags = [], modules: courseModules = [] } = req.body;

  if (!title || !domain) {
    return res.status(400).json({ error: "Campos obrigatorios: title e domain." });
  }

  const course = {
    id: courses.length + 1,
    title,
    trackId: trackId || null,
    domain,
    level: level || "basico",
    workloadHours: Number(workloadHours) || 8,
    skillTags,
    modules: courseModules,
    status: "active",
    createdAt: new Date().toISOString()
  };

  courses.push(course);
  return res.status(201).json(course);
}));

app.get("/academy/courses/:courseId/progress", ...withPermission("academy_domain", "read", (req, res) => {
  const courseId = Number(req.params.courseId);
  const courseProgress = progress.filter((p) => p.courseId === courseId);
  res.json(courseProgress);
}));

app.post("/academy/courses/:courseId/progress", ...withPermission("academy_domain", "write", (req, res) => {
  const courseId = Number(req.params.courseId);
  const { userId, completedModules = [], percentageDone } = req.body;

  if (!userId) {
    return res.status(400).json({ error: "userId e obrigatorio." });
  }

  const existing = progress.find((p) => p.courseId === courseId && p.userId === userId);
  if (existing) {
    existing.completedModules = completedModules;
    existing.percentageDone = Number(percentageDone) || existing.percentageDone;
    existing.updatedAt = new Date().toISOString();
    return res.json(existing);
  }

  const record = {
    id: progress.length + 1,
    courseId,
    userId,
    completedModules,
    percentageDone: Number(percentageDone) || 0,
    status: Number(percentageDone) >= 100 ? "completed" : "in_progress",
    updatedAt: new Date().toISOString()
  };

  progress.push(record);

  if (record.status === "completed") {
    emitAcademyEvent("academy.completed", { userId, courseId });
  }

  return res.status(201).json(record);
}));

// ─── ISSUE 2: Trilhas por monólito ──────────────────────────────────────────

app.get("/academy/tracks/monolith", ...withPermission("academy_tracks", "read", (_req, res) => {
  res.json(monolithTracks);
}));

app.get("/academy/tracks/monolith/:monolith", ...withPermission("academy_tracks", "read", (req, res) => {
  const key = req.params.monolith;
  const track = monolithTracks[key];

  if (!track) {
    return res.status(404).json({
      error: "Trilha de monolito nao encontrada.",
      available: Object.keys(monolithTracks)
    });
  }

  return res.json(track);
}));

// ─── ISSUE 3: Trilha transversal obrigatória ────────────────────────────────

app.get("/academy/training/core-liceu", ...withPermission("academy_tracks", "read", (_req, res) => {
  res.json(coreLiceuTraining);
}));

// ─── ISSUE 4: John Training Engine ──────────────────────────────────────────

app.post("/academy/john/train", ...withPermission("john_ai", "execute", (req, res) => {
  const { userId, currentScores = {}, completedCourses = [] } = req.body;

  if (!userId) {
    return res.status(400).json({ error: "userId e obrigatorio." });
  }

  const weak = Object.entries(currentScores)
    .filter(([, v]) => Number(v) < 60)
    .map(([skill]) => skill);

  const suggestions = weak.length
    ? weak.map((skill) => `Reforco em: ${skill}`)
    : ["Avance para trilha intermediaria", "Explore um monolito novo"];

  const difficulty = completedCourses.length < 3 ? "basico" : completedCourses.length < 8 ? "intermediario" : "avancado";

  const plan = {
    userId,
    analyzedAt: new Date().toISOString(),
    weakAreas: weak,
    suggestedActions: suggestions,
    recommendedDifficulty: difficulty,
    nextStep: suggestions[0]
  };

  emitAcademyEvent("academy.john_recommended", { userId, plan });
  return res.json(plan);
}));

// ─── ISSUE 5: Score cognitivo ────────────────────────────────────────────────

app.get("/academy/users/:userId/cognitive-score", ...withPermission("academy_domain", "read", (req, res) => {
  const { userId } = req.params;
  const score = cognitiveScores.find((s) => s.userId === userId);

  if (!score) {
    return res.status(404).json({ error: "Score cognitivo nao encontrado para este usuario." });
  }

  return res.json(score);
}));

app.post("/academy/users/:userId/cognitive-score", ...withPermission("academy_domain", "write", (req, res) => {
  const { userId } = req.params;
  const { skillMatrix = {}, specializationLevel, notes } = req.body;

  const existing = cognitiveScores.find((s) => s.userId === userId);

  if (existing) {
    Object.assign(existing, { skillMatrix, specializationLevel, notes, updatedAt: new Date().toISOString() });
    return res.json(existing);
  }

  const score = {
    id: cognitiveScores.length + 1,
    userId,
    skillMatrix,
    specializationLevel: specializationLevel || "junior",
    cognitive_score: Object.values(skillMatrix).reduce((sum, v) => sum + Number(v), 0) / Math.max(Object.keys(skillMatrix).length, 1),
    notes: notes || null,
    updatedAt: new Date().toISOString()
  };

  cognitiveScores.push(score);
  return res.status(201).json(score);
}));

// ─── ISSUE 6: Aprendizado baseado em erro ───────────────────────────────────

app.post("/academy/john/learn-from-error", ...withPermission("john_ai", "execute", (req, res) => {
  const { userId, errorType, sourceSystem, errorDescription } = req.body;

  if (!userId || !errorType || !sourceSystem) {
    return res.status(400).json({ error: "Campos obrigatorios: userId, errorType, sourceSystem." });
  }

  const domainMap = {
    deal: "vendas",
    contract: "juridico",
    financial: "financeiro",
    audit: "compliance",
    loss: "operacoes"
  };

  const domain = domainMap[String(errorType).toLowerCase()] || "geral";

  const lesson = {
    id: errorLessons.length + 1,
    userId,
    errorType,
    sourceSystem,
    errorDescription: errorDescription || null,
    generatedLesson: {
      title: `Licao automatica: ${errorType} em ${sourceSystem}`,
      domain,
      content: `Baseado no erro registrado em ${sourceSystem}, recomendamos revisao dos modulos de ${domain}.`,
      exercises: [`Simulacao de cenario real: ${errorType}`, "Revisao de conformidade", "Teste de absorcao de conteudo"],
      estimatedDuration: "45min"
    },
    createdAt: new Date().toISOString()
  };

  errorLessons.push(lesson);
  emitAcademyEvent("academy.john_recommended", { userId, lessonId: lesson.id, trigger: "error" });
  return res.status(201).json(lesson);
}));

// ─── ISSUE 7: Simulação real (sandbox) ──────────────────────────────────────

app.post("/academy/sandbox/simulate", ...withPermission("sandbox", "execute", (req, res) => {
  const { userId, simulationType, scenario } = req.body;

  if (!userId || !simulationType) {
    return res.status(400).json({ error: "Campos obrigatorios: userId e simulationType." });
  }

  const typeMap = {
    venda: { monolith: "archimedes", description: "Simulacao de fluxo de venda imobiliaria" },
    negociacao: { monolith: "sales_os", description: "Simulacao de negociacao avancada" },
    contrato: { monolith: "juridico", description: "Simulacao de assinatura e analise contratual" },
    financeiro: { monolith: "cea", description: "Simulacao de analise de credito e aprovacao" }
  };

  const meta = typeMap[String(simulationType).toLowerCase()] || { monolith: "geral", description: "Simulacao generica" };

  const scoreRaw = Math.floor(Math.random() * 31) + 70;

  const sim = {
    id: sandboxSimulations.length + 1,
    userId,
    simulationType,
    scenario: scenario || "padrao",
    monolith: meta.monolith,
    description: meta.description,
    score: scoreRaw,
    outcome: scoreRaw >= 75 ? "aprovado" : "em_reforco",
    feedback: scoreRaw >= 75
      ? "Excelente desempenho na simulacao. Pronto para operacao real."
      : "Revise os modulos relacionados antes de operar em producao.",
    createdAt: new Date().toISOString()
  };

  sandboxSimulations.push(sim);
  return res.status(201).json(sim);
}));

// ─── ISSUE 8: Replay de operações reais ─────────────────────────────────────

app.post("/academy/replay", ...withPermission("replay", "read", (req, res) => {
  const { userId, replayType, referenceId, sourceSystem } = req.body;

  if (!userId || !replayType || !referenceId) {
    return res.status(400).json({ error: "Campos obrigatorios: userId, replayType, referenceId." });
  }

  const replay = {
    id: replays.length + 1,
    userId,
    replayType,
    referenceId,
    sourceSystem: sourceSystem || "ecossistema",
    replayedAt: new Date().toISOString(),
    insights: [
      `Ponto critico identificado no ${replayType} #${referenceId}`,
      "Oportunidade de melhoria na tomada de decisao",
      "Recomendacao: revisar trilha correspondente"
    ]
  };

  replays.push(replay);
  return res.status(201).json(replay);
}));

app.get("/academy/replay", ...withPermission("replay", "read", (req, res) => {
  const { userId } = req.query;
  const result = userId ? replays.filter((r) => r.userId === userId) : replays;
  return res.json(result);
}));

// ─── ISSUE 9: Certificação por performance ──────────────────────────────────

app.post("/academy/certification/auto-certify", ...withPermission("perf_cert", "write", (req, res) => {
  const { userId, trackId, kpiScore, approvedByJohn = false, executionApproved = false } = req.body;

  if (!userId || !trackId) {
    return res.status(400).json({ error: "Campos obrigatorios: userId e trackId." });
  }

  const kpi = Number(kpiScore) || 0;
  const approved = kpi >= 75 || approvedByJohn || executionApproved;

  const cert = {
    id: performanceCertifications.length + 1,
    userId,
    trackId,
    kpiScore: kpi,
    approvedByJohn,
    executionApproved,
    status: approved ? "certificado" : "reprovado",
    issuedAt: approved ? new Date().toISOString() : null,
    reason: approved ? "Aprovado por performance real" : "KPI abaixo do minimo (75) sem aprovacao complementar"
  };

  performanceCertifications.push(cert);

  if (approved) {
    emitAcademyEvent("academy.certified", { userId, trackId, certId: cert.id });
  } else {
    emitAcademyEvent("academy.failed", { userId, trackId });
  }

  return res.status(201).json(cert);
}));

// ─── ISSUE 10: Integração com RH — onboarding automático ───────────────────

app.post("/academy/hr/onboarding", ...withPermission("hr_onboarding", "write", (req, res) => {
  const { userId, name, role, contractType } = req.body;

  if (!userId || !role || !contractType) {
    return res.status(400).json({ error: "Campos obrigatorios: userId, role, contractType." });
  }

  const roleTracks = mandatoryTracksByRole[String(role).toLowerCase()] || ["cultura_liceu"];
  const contractTracks_ = contractType === "pj"
    ? contractTracks.pj.mandatoryTracks
    : contractTracks.clt.mandatoryTracks;

  const allTracks = [...new Set([...roleTracks, ...contractTracks_])];

  const onboarding = {
    id: onboardings.length + 1,
    userId,
    name: name || userId,
    role,
    contractType,
    mandatoryTracks: allTracks,
    trainingStatus: "pending",
    completedTracks: [],
    startedAt: new Date().toISOString()
  };

  onboardings.push(onboarding);
  emitAcademyEvent("academy.enrolled", { userId, tracks: allTracks, source: "hr_onboarding" });
  return res.status(201).json(onboarding);
}));

app.get("/academy/hr/onboarding/:userId", ...withPermission("hr_onboarding", "read", (req, res) => {
  const { userId } = req.params;
  const record = onboardings.find((o) => o.userId === userId);

  if (!record) {
    return res.status(404).json({ error: "Onboarding nao encontrado para este usuario." });
  }

  return res.json(record);
}));

// ─── ISSUE 11: Trilha obrigatória por função ────────────────────────────────

app.get("/academy/hr/mandatory-tracks/:role", ...withPermission("hr_onboarding", "read", (req, res) => {
  const role = String(req.params.role).toLowerCase();
  const tracks = mandatoryTracksByRole[role];

  if (!tracks) {
    return res.status(404).json({
      error: "Funcao nao encontrada.",
      available: Object.keys(mandatoryTracksByRole)
    });
  }

  return res.json({ role, mandatoryTracks: tracks });
}));

// ─── ISSUE 12: Controle CLT + PJ ─────────────────────────────────────────────

app.get("/academy/hr/contract-tracks/:contractType", ...withPermission("hr_onboarding", "read", (req, res) => {
  const type = String(req.params.contractType).toLowerCase();
  const record = contractTracks[type];

  if (!record) {
    return res.status(404).json({ error: "Tipo de contrato invalido. Use: clt ou pj." });
  }

  return res.json(record);
}));

// ─── ISSUES 13-14: Compliance + Aceite jurídico ─────────────────────────────

app.get("/academy/legal/compliance-courses", ...withPermission("legal_compliance", "read", (_req, res) => {
  res.json(complianceCourses);
}));

app.post("/academy/legal/sign-acceptance", ...withPermission("legal_compliance", "read", (req, res) => {
  const { userId, courseId, acceptedAt } = req.body;

  if (!userId || !courseId) {
    return res.status(400).json({ error: "Campos obrigatorios: userId e courseId." });
  }

  const course = complianceCourses.find((c) => c.id === Number(courseId));
  if (!course) {
    return res.status(404).json({ error: "Curso de compliance nao encontrado." });
  }

  const acceptance = {
    id: legalAcceptances.length + 1,
    userId,
    courseId: Number(courseId),
    courseTitle: course.title,
    acceptedAt: acceptedAt || new Date().toISOString(),
    signature: `ACEITE-${userId}-${courseId}-${Date.now()}`
  };

  legalAcceptances.push(acceptance);
  emitAcademyEvent("academy.completed", { userId, courseId, type: "legal_acceptance" });
  return res.status(201).json(acceptance);
}));

// ─── ISSUE 15: Dashboard educacional ────────────────────────────────────────

app.get("/academy/metrics/dashboard", ...withPermission("metrics", "read", (_req, res) => {
  const totalEnrollments = onboardings.length;
  const completedCertifications = performanceCertifications.filter((c) => c.status === "certificado").length;
  const avgKpi = performanceCertifications.length
    ? Number((performanceCertifications.reduce((s, c) => s + c.kpiScore, 0) / performanceCertifications.length).toFixed(2))
    : 0;

  const trackCompletion = onboardings.reduce((acc, o) => {
    o.mandatoryTracks.forEach((t) => {
      acc[t] = acc[t] || { track: t, enrolled: 0, completed: 0 };
      acc[t].enrolled += 1;
      if (o.completedTracks.includes(t)) acc[t].completed += 1;
    });
    return acc;
  }, {});

  return res.json({
    kpis: {
      totalEnrollments,
      completedCertifications,
      averageKpiScore: avgKpi,
      totalCourses: courses.length,
      totalSandboxSimulations: sandboxSimulations.length,
      totalReplays: replays.length
    },
    trackCompletion: Object.values(trackCompletion),
    recentEvents: academyEvents.slice(-10)
  });
}));

// ─── ISSUE 16: Correlação com resultado real ─────────────────────────────────

app.get("/academy/metrics/correlation", ...withPermission("metrics", "read", (_req, res) => {
  const certifiedUsers = performanceCertifications
    .filter((c) => c.status === "certificado")
    .map((c) => c.userId);

  const correlations = certifiedUsers.map((userId) => {
    const userSandbox = sandboxSimulations.filter((s) => s.userId === userId);
    const avgSandbox = userSandbox.length
      ? userSandbox.reduce((s, sim) => s + sim.score, 0) / userSandbox.length
      : 0;
    const cert = performanceCertifications.find((c) => c.userId === userId && c.status === "certificado");

    return {
      userId,
      certified: true,
      averageSandboxScore: Number(avgSandbox.toFixed(2)),
      kpiScore: cert ? cert.kpiScore : null,
      insight: avgSandbox >= 80
        ? "Alta correlacao: treinamento intenso impacta resultado real"
        : "Treinamento basico: potencial de melhora com trilhas avancadas"
    };
  });

  return res.json({ correlations, analyzedAt: new Date().toISOString() });
}));

// ─── ISSUE 17: Academia como produto SaaS ───────────────────────────────────

app.get("/academy/saas/courses", ...withPermission("saas", "read", (_req, res) => {
  res.json(saasOffers);
}));

app.post("/academy/saas/courses", ...withPermission("saas", "write", (req, res) => {
  const { title, domain, price, level, targetAudience, certificationIncluded = false } = req.body;

  if (!title || !domain || price === undefined) {
    return res.status(400).json({ error: "Campos obrigatorios: title, domain e price." });
  }

  const offer = {
    id: saasOffers.length + 1,
    title,
    domain,
    price: Number(price),
    level: level || "intermediario",
    targetAudience: targetAudience || "mercado",
    certificationIncluded,
    type: "saas_externo",
    createdAt: new Date().toISOString()
  };

  saasOffers.push(offer);
  return res.status(201).json(offer);
}));

// ─── ISSUE 18: Marketplace de cursos ────────────────────────────────────────

app.get("/academy/marketplace/courses", ...withPermission("marketplace", "read", (_req, res) => {
  res.json(marketplaceCourses);
}));

app.post("/academy/marketplace/courses", ...withPermission("marketplace", "write", (req, res) => {
  const { title, domain, authorId, authorType, price, skillTags = [] } = req.body;

  if (!title || !domain || !authorId) {
    return res.status(400).json({ error: "Campos obrigatorios: title, domain, authorId." });
  }

  const course = {
    id: marketplaceCourses.length + 1,
    title,
    domain,
    authorId,
    authorType: authorType || "especialista",
    price: Number(price) || 0,
    skillTags,
    status: "pending_review",
    type: "marketplace",
    createdAt: new Date().toISOString()
  };

  marketplaceCourses.push(course);
  return res.status(201).json(course);
}));

// ─── ISSUE 19: White-label corporativo ──────────────────────────────────────

app.post("/academy/whitelabel/setup", ...withPermission("whitelabel", "write", (req, res) => {
  const { companyId, companyName, tracks = [], customBranding = {} } = req.body;

  if (!companyId || !companyName) {
    return res.status(400).json({ error: "Campos obrigatorios: companyId e companyName." });
  }

  const existing = whitelabels.find((w) => w.companyId === companyId);
  if (existing) {
    return res.status(409).json({ error: "White-label ja existe para esta empresa.", whitelabel: existing });
  }

  const wl = {
    id: whitelabels.length + 1,
    companyId,
    companyName,
    tracks,
    customBranding,
    status: "active",
    createdAt: new Date().toISOString()
  };

  whitelabels.push(wl);
  return res.status(201).json(wl);
}));

// ─── ISSUES 20-21: Eventos NATS educacionais ────────────────────────────────

app.get("/academy/events", ...withPermission("academy_events", "read", (req, res) => {
  const { type } = req.query;
  const result = type ? academyEvents.filter((e) => e.type === type) : academyEvents;
  return res.json(result);
}));

// ─── ISSUES 22-23: CEFEIDA — IA de aprendizado ──────────────────────────────

app.post("/academy/cefeida/analyze", ...withPermission("cefeida", "write", (req, res) => {
  const { userId, studyBehavior = {}, performanceHistory = [], errorPatterns = [] } = req.body;

  if (!userId) {
    return res.status(400).json({ error: "userId e obrigatorio." });
  }

  const avgPerf = performanceHistory.length
    ? performanceHistory.reduce((s, v) => s + Number(v), 0) / performanceHistory.length
    : 0;

  const topErrors = errorPatterns.slice(0, 3);

  const analysis = {
    id: cefeidaAnalyses.length + 1,
    userId,
    analyzedAt: new Date().toISOString(),
    studyBehavior,
    averagePerformance: Number(avgPerf.toFixed(2)),
    topErrorPatterns: topErrors,
    recommendations: topErrors.length
      ? topErrors.map((e) => `Reforcar area: ${e}`)
      : ["Manter ritmo atual", "Explorar trilha avancada"],
    adaptivePath: avgPerf >= 80 ? "avancado" : avgPerf >= 60 ? "intermediario" : "basico"
  };

  cefeidaAnalyses.push(analysis);
  return res.status(201).json(analysis);
}));

app.post("/academy/cefeida/generate-content", ...withPermission("cefeida", "write", (req, res) => {
  const { userId, domain, format, targetLevel } = req.body;

  if (!userId || !domain) {
    return res.status(400).json({ error: "Campos obrigatorios: userId e domain." });
  }

  const content = {
    id: dynamicContents.length + 1,
    userId,
    domain,
    format: format || "microlearning",
    targetLevel: targetLevel || "intermediario",
    generatedContent: {
      title: `${format === "microlearning" ? "Micro-aula" : "Trilha Adaptativa"}: ${domain}`,
      summary: `Conteudo dinamico gerado pela CEFEIDA para ${domain} — nivel ${targetLevel || "intermediario"}.`,
      steps: [
        `Introducao rapida ao tema: ${domain}`,
        "Exercicio pratico contextualizado",
        "Quiz de absorcao (5 questoes)",
        "Caso real do ecossistema LICEU",
        "Recomendacao proxima etapa"
      ],
      estimatedDuration: format === "microlearning" ? "15min" : "2h"
    },
    createdAt: new Date().toISOString()
  };

  dynamicContents.push(content);
  return res.status(201).json(content);
}));

// ─── ISSUE 24: Tela institucional (Trading Desk Educacional) ─────────────────

app.get("/academy/dashboard/institutional", ...withPermission("metrics", "read", (_req, res) => {
  const ranking = [...gamificationSessions]
    .sort((a, b) => b.score - a.score)
    .slice(0, 10)
    .map((s, i) => ({ position: i + 1, studentId: s.studentId, score: s.score }));

  const lateAlerts = onboardings
    .filter((o) => o.trainingStatus === "pending" && o.completedTracks.length === 0)
    .map((o) => ({ userId: o.userId, role: o.role, pendingTracks: o.mandatoryTracks.length }));

  const johnRecommendations = academyEvents
    .filter((e) => e.type === "academy.john_recommended")
    .slice(-5);

  return res.json({
    blocks: {
      totalTracks: Object.keys(monolithTracks).length,
      globalProgress: progress.length,
      rankingTop10: ranking,
      lateAlerts,
      johnRecommendations
    },
    updatedAt: new Date().toISOString()
  });
}));

// ─── ISSUE 25: Ranking gamificado ───────────────────────────────────────────

app.get("/academy/ranking/gamified", ...withPermission("academy_gamification", "read", (_req, res) => {
  const certMap = performanceCertifications.reduce((acc, c) => {
    if (!acc[c.userId]) acc[c.userId] = 0;
    if (c.status === "certificado") acc[c.userId] += 1;
    return acc;
  }, {});

  const sessionMap = gamificationSessions.reduce((acc, s) => {
    if (!acc[s.studentId]) acc[s.studentId] = { xp: 0, sessions: 0 };
    acc[s.studentId].xp += s.score;
    acc[s.studentId].sessions += 1;
    return acc;
  }, {});

  const ranking = Object.entries(sessionMap).map(([userId, data]) => {
    const certs = certMap[userId] || 0;
    const xp = data.xp + certs * 200;
    const level = xp < 500 ? "Aprendiz" : xp < 1500 ? "Praticante" : xp < 3000 ? "Especialista" : "Mestre";

    return { userId, xp, level, sessions: data.sessions, certifications: certs };
  });

  ranking.sort((a, b) => b.xp - a.xp).forEach((r, i) => { r.position = i + 1; });

  return res.json(ranking);
}));

// ─── ISSUES 26-27: RBAC educacional ─────────────────────────────────────────

app.get("/academy/rbac/roles", ...withPermission("rbac_edu", "read", (_req, res) => {
  res.json(educationalRoles);
}));

app.get("/academy/rbac/roles/:role", ...withPermission("rbac_edu", "read", (req, res) => {
  const role = String(req.params.role).toUpperCase();
  const roleData = educationalRoles[role];

  if (!roleData) {
    return res.status(404).json({
      error: "Papel educacional nao encontrado.",
      available: Object.keys(educationalRoles)
    });
  }

  return res.json({ role, ...roleData });
}));

// ─── ISSUE 28: Treinamento do próprio John (DNA) ─────────────────────────────

app.post("/academy/john/feed-dna", ...withPermission("john_dna", "write", (req, res) => {
  const { source, knowledge, domain, confidence = 0.8 } = req.body;

  if (!source || !knowledge || !domain) {
    return res.status(400).json({ error: "Campos obrigatorios: source, knowledge, domain." });
  }

  const entry = {
    id: johnDnaFeed.length + 1,
    source,
    knowledge,
    domain,
    confidence: Number(confidence),
    status: "absorbed",
    absorbedAt: new Date().toISOString()
  };

  johnDnaFeed.push(entry);
  return res.status(201).json({
    message: "Conhecimento absorvido pelo core_dna do John.",
    entry
  });
}));

// ─── ISSUE 29: John como professor ──────────────────────────────────────────

app.post("/academy/john/teach", ...withPermission("john_teach", "execute", (req, res) => {
  const { userId, topic, doubt } = req.body;

  if (!userId || !topic) {
    return res.status(400).json({ error: "Campos obrigatorios: userId e topic." });
  }

  const lesson = {
    teacher: "John Brasileiro — IA Pedagógico",
    userId,
    topic,
    answeredDoubt: doubt || null,
    lesson: {
      introduction: `Olá! Vou te ensinar sobre ${topic} de forma aplicada ao ecossistema LICEU.`,
      keyPoints: [
        `Conceito central de ${topic}`,
        `Aplicacao pratica no ecossistema`,
        `Caso real simulado`,
        `Exercicio rapido`
      ],
      scenario: `Imagine que voce esta operando no monolito correspondente a ${topic}. Como voce tomaria a decisao certa?`,
      challenge: `Resolva: dado um cenario real de ${topic}, qual seria o melhor passo seguinte?`,
      nextRecommendation: `Apos dominar ${topic}, explore a trilha avancada relacionada.`
    },
    generatedAt: new Date().toISOString()
  };

  return res.json(lesson);
}));

// ─── ISSUE 30: Kanban Global — Task como aprendizado ─────────────────────────

app.post("/academy/kanban/task-learning", ...withPermission("kanban_learning", "write", (req, res) => {
  const { taskId, userId, taskTitle, taskDomain, taskOutcome } = req.body;

  if (!taskId || !userId || !taskDomain) {
    return res.status(400).json({ error: "Campos obrigatorios: taskId, userId, taskDomain." });
  }

  const needsTraining = taskOutcome === "blocked" || taskOutcome === "failed";

  const record = {
    id: taskLearnings.length + 1,
    taskId,
    userId,
    taskTitle: taskTitle || `Task #${taskId}`,
    taskDomain,
    taskOutcome: taskOutcome || "completed",
    generatedTraining: needsTraining
      ? {
          title: `Treinamento gerado por task: ${taskTitle || taskId}`,
          domain: taskDomain,
          reason: `Task ${taskOutcome} — recomendacao automatica de reforco`,
          suggestedTrack: taskDomain,
          urgency: "alta"
        }
      : null,
    recommendation: needsTraining
      ? `Recomendamos trilha de reforco em ${taskDomain} antes de retomar tarefas similares.`
      : `Otima execucao! Continue evoluindo em ${taskDomain}.`,
    processedAt: new Date().toISOString()
  };

  taskLearnings.push(record);

  if (needsTraining) {
    emitAcademyEvent("academy.john_recommended", { userId, taskId, domain: taskDomain, trigger: "kanban_task" });
  }

  return res.status(201).json(record);
}));

module.exports = app;