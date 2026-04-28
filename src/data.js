const school = {
  fundamental: {
    title: "Ensino Fundamental (Base Cognitiva)",
    ageRange: "3-14",
    topics: [
      "matematica aplicada ao cotidiano",
      "logica e pensamento computacional",
      "ciencias com laboratorio virtual",
      "educacao financeira (ECONO)",
      "sustentabilidade (ANCHOR microgrid)",
      "introducao a engenharia"
    ]
  },
  highSchool: {
    title: "Ensino Medio Interdisciplinar Tecnico",
    ageRange: "15-17",
    topics: [
      "fisica aplicada a construcao",
      "quimica dos materiais",
      "programacao basica",
      "BIM introdutorio",
      "robotica construcao civil",
      "empreendedorismo tecnico"
    ]
  },
  technical: {
    title: "Ensino Tecnico Profissionalizante",
    ageRange: "18+",
    tracks: [
      "tecnico em edificacoes",
      "tecnico BIM",
      "tecnico em planejamento obra",
      "tecnico energia solar microgrid",
      "tecnico IoT construcao",
      "tecnico manutencao predial",
      "tecnico industrializacao construcao"
    ]
  }
};

const enrollments = [];
const gamificationSessions = [];
const labResults = [];
const evaluations = [];
const technologyEvents = [];
const certificationTracks = [];
const generatedCourses = [];

const holdingUsers = [
  { id: "HLD-001", name: "Ana Souza", role: "holding_admin" },
  { id: "HLD-002", name: "Bruno Lima", role: "academy_director" },
  { id: "HLD-003", name: "Carla Mendes", role: "pd_ia_operator" },
  { id: "HLD-004", name: "Diego Rocha", role: "instructor" },
  { id: "HLD-005", name: "Elisa Costa", role: "operations" },
  { id: "HLD-006", name: "Fabio Nunes", role: "auditor" }
];

const rolePermissions = {
  holding_admin: ["*"],
  academy_director: [
    "school:read",
    "school:enroll",
    "academy_gamification:read",
    "academy_gamification:write",
    "academy_lab:read",
    "academy_lab:write",
    "john_ai:execute",
    "certification_sdk:read",
    "certification_sdk:write",
    "pd_events:read",
    "academy_domain:read",
    "academy_domain:write",
    "academy_tracks:read",
    "academy_tracks:write",
    "hr_onboarding:read",
    "hr_onboarding:write",
    "legal_compliance:read",
    "metrics:read",
    "saas:read",
    "saas:write",
    "marketplace:read",
    "marketplace:write",
    "cefeida:read",
    "cefeida:write",
    "john_dna:write",
    "john_teach:execute",
    "kanban_learning:write",
    "academy_events:read",
    "sandbox:execute",
    "replay:read",
    "perf_cert:write",
    "whitelabel:write",
    "rbac_edu:read"
  ],
  pd_ia_operator: [
    "pd_events:publish",
    "pd_events:read",
    "certification_sdk:read",
    "cefeida:read",
    "cefeida:write",
    "academy_events:read",
    "metrics:read"
  ],
  instructor: [
    "school:read",
    "academy_gamification:write",
    "academy_gamification:read",
    "academy_lab:write",
    "academy_lab:read",
    "john_ai:execute",
    "certification_sdk:read",
    "academy_domain:read",
    "academy_domain:write",
    "academy_tracks:read",
    "legal_compliance:read",
    "metrics:read",
    "sandbox:execute",
    "replay:read",
    "john_teach:execute",
    "kanban_learning:write"
  ],
  operations: [
    "school:read",
    "school:enroll",
    "academy_gamification:write",
    "academy_gamification:read",
    "academy_lab:read",
    "certification_sdk:read",
    "academy_domain:read",
    "hr_onboarding:read",
    "hr_onboarding:write",
    "sandbox:execute",
    "academy_events:read"
  ],
  auditor: [
    "school:read",
    "academy_gamification:read",
    "academy_lab:read",
    "certification_sdk:read",
    "pd_events:read",
    "academy_domain:read",
    "academy_tracks:read",
    "metrics:read",
    "legal_compliance:read",
    "hr_onboarding:read",
    "academy_events:read",
    "rbac_edu:read",
    "replay:read"
  ]
};

// Issue 1 — Domínio educacional unificado
const courses = [];
const modules = [];
const lessons = [];
const progress = [];
const academyCertifications = [];

// Issue 2 — Trilhas por monólito
const monolithTracks = {
  archimedes: {
    name: "Archimedes Track",
    monolith: "Imob Tech",
    description: "Trilha completa para o ecossistema imobiliário",
    modules: ["Fundamentos Imobiliários", "CRM Avançado", "Negociação Imobiliária", "Jurídico Imobiliário", "BIM para Incorporação"]
  },
  gameMkt: {
    name: "Game MKT Track",
    monolith: "Marketing",
    description: "Trilha de marketing gamificado e digital",
    modules: ["Marketing Digital", "Growth Hacking", "Funil de Vendas", "Conteúdo Estratégico", "Analytics"]
  },
  juridico: {
    name: "Jurídico Track",
    monolith: "JurídicoTech",
    description: "Trilha jurídica do ecossistema",
    modules: ["LGPD", "Contratos Imobiliários", "Não-Circunvenção", "Compliance Corporativo", "Regulatório"]
  },
  finance: {
    name: "Finance Track",
    monolith: "CEA / Hub Financeiro",
    description: "Trilha financeira e de investimentos",
    modules: ["CEA Básico", "Análise de Crédito", "Gestão de Caixa", "FIIs e Fundos", "Compliance Financeiro"]
  },
  opera: {
    name: "OPERA Track",
    monolith: "OPERA",
    description: "Trilha de operações e execução",
    modules: ["Planejamento de Obras", "Gestão de Canteiro", "IoT Predial", "Microgrid", "Controle de Qualidade"]
  },
  cefeida: {
    name: "CEFEIDA Data Track",
    monolith: "CEFEIDA",
    description: "Trilha de dados, IA e análise preditiva",
    modules: ["Python para Dados", "Machine Learning Aplicado", "Análise Preditiva", "ETL e Pipelines", "Dashboards Inteligentes"]
  },
  johnCopilot: {
    name: "John Copilot Track",
    monolith: "John AI",
    description: "Trilha de uso e co-pilotagem com o John",
    modules: ["Uso do John", "Prompts Avançados", "Tomada de Decisão com IA", "Governança de IA", "Integração John + Monólitos"]
  }
};

// Issue 3 — Core LICEU Training (trilha transversal obrigatória)
const coreLiceuTraining = {
  name: "CORE LICEU TRAINING",
  type: "transversal_obrigatoria",
  description: "Trilha obrigatória para todos os colaboradores do ecossistema LICEU",
  modules: [
    { id: 1, title: "Cultura LICEU", duration: "2h", mandatory: true },
    { id: 2, title: "Uso do Kanban Global", duration: "1h30", mandatory: true },
    { id: 3, title: "Uso do John", duration: "2h", mandatory: true },
    { id: 4, title: "Governança do Ecossistema", duration: "1h", mandatory: true },
    { id: 5, title: "Compliance Jurídico Básico", duration: "2h", mandatory: true }
  ],
  totalWorkload: "8h30",
  requiredForOnboarding: true
};

// Issues 5-6 — Score cognitivo + Aprendizado por erro
const cognitiveScores = [];
const errorLessons = [];

// Issue 7 — Sandbox simulações reais
const sandboxSimulations = [];

// Issue 8 — Replay de operações reais
const replays = [];

// Issue 9 — Certificações por performance
const performanceCertifications = [];

// Issues 10-12 — RH + Onboarding + Contratos
const onboardings = [];

const mandatoryTracksByRole = {
  corretor: ["vendas", "juridico_basico", "crm", "cultura_liceu"],
  financeiro: ["cea", "compliance", "cultura_liceu", "uso_john"],
  gestor: ["governanca", "lideranca", "cultura_liceu", "kanban_global", "uso_john"],
  tecnico: ["opera", "bim_basico", "cultura_liceu"],
  analista_dados: ["cefeida_data", "python_basico", "cultura_liceu", "uso_john"],
  juridico: ["lgpd", "contratos", "nao_circunvencao", "compliance", "cultura_liceu"]
};

const contractTracks = {
  clt: {
    contractType: "CLT",
    mandatoryTracks: ["cultura_liceu", "compliance_trabalhista", "uso_john", "kanban_global", "governanca_ecossistema"]
  },
  pj: {
    contractType: "PJ",
    mandatoryTracks: ["nao_circunvencao", "lgpd", "contratos_pj", "compliance_fiscal", "cultura_liceu"]
  }
};

// Issues 13-14 — Compliance + Aceite jurídico
const complianceCourses = [
  { id: 1, title: "LGPD — Lei Geral de Proteção de Dados", duration: "4h", mandatory: true, domain: "juridico" },
  { id: 2, title: "Cláusula de Não-Circunvenção", duration: "2h", mandatory: true, domain: "juridico" },
  { id: 3, title: "Contratos: fundamentos e boas práticas", duration: "3h", mandatory: true, domain: "juridico" },
  { id: 4, title: "Compliance Corporativo", duration: "3h", mandatory: true, domain: "compliance" },
  { id: 5, title: "Ética e Conduta no Ecossistema", duration: "1h30", mandatory: true, domain: "compliance" }
];
const legalAcceptances = [];

// Issues 20-21 — Eventos NATS (academia)
const academyEvents = [];

function emitAcademyEvent(type, payload) {
  academyEvents.push({ type, payload, emittedAt: new Date().toISOString() });
}

// Issues 22-23 — CEFEIDA IA
const cefeidaAnalyses = [];
const dynamicContents = [];

// Issues 17-19 — EdTech Externo (SaaS, Marketplace, White-label)
const saasOffers = [];
const marketplaceCourses = [];
const whitelabels = [];

// Issues 26-27 — RBAC educacional
const educationalRoles = {
  ADMIN: {
    permissions: ["courses:*", "tracks:*", "users:*", "certifications:*", "metrics:*", "rbac:*", "john:*", "cefeida:*"]
  },
  INSTRUTOR: {
    permissions: ["courses:read", "courses:write", "tracks:read", "users:read", "certifications:read", "metrics:read", "john:read"]
  },
  COLABORADOR: {
    permissions: ["courses:read", "tracks:read", "certifications:read", "progress:write", "progress:read"]
  },
  CLIENTE_EXTERNO: {
    permissions: ["saas:read", "marketplace:read", "certifications:read"]
  }
};

// Issue 28 — John DNA Feed
const johnDnaFeed = [];

// Issue 30 — Kanban task learning
const taskLearnings = [];

module.exports = {
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
  // Issue 1
  courses,
  modules,
  lessons,
  progress,
  academyCertifications,
  // Issue 2
  monolithTracks,
  // Issue 3
  coreLiceuTraining,
  // Issues 5-6
  cognitiveScores,
  errorLessons,
  // Issue 7
  sandboxSimulations,
  // Issue 8
  replays,
  // Issue 9
  performanceCertifications,
  // Issues 10-12
  onboardings,
  mandatoryTracksByRole,
  contractTracks,
  // Issues 13-14
  complianceCourses,
  legalAcceptances,
  // Issues 20-21
  academyEvents,
  emitAcademyEvent,
  // Issues 22-23
  cefeidaAnalyses,
  dynamicContents,
  // Issues 17-19
  saasOffers,
  marketplaceCourses,
  whitelabels,
  // Issues 26-27
  educationalRoles,
  // Issue 28
  johnDnaFeed,
  // Issue 30
  taskLearnings
};