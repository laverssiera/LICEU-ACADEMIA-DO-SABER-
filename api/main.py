"""
ACADEMIA DO SABER — FASTAPI BACKEND COMPLETO
LICEU Ecossistema | Issues 1-30
"""

from __future__ import annotations

import json
import math
import random
import uuid
from datetime import datetime
from functools import wraps
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

# ──────────────────────────────────────────────────────────────────────────────
# App & CORS
# ──────────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Academia do Saber — LICEU",
    description="Motor educacional completo: cursos, trilhas, John, CEFEIDA, RH, compliance.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────────────────────────
# NATS Client (lazy connect)
# ──────────────────────────────────────────────────────────────────────────────
try:
    import nats
    NATS_AVAILABLE = True
except ImportError:
    NATS_AVAILABLE = False

_nc = None


async def get_nats():
    global _nc
    if not NATS_AVAILABLE:
        return None
    if _nc is None or not _nc.is_connected:
        try:
            import nats as nats_lib
            _nc = await nats_lib.connect("nats://nats:4222")
        except Exception:
            _nc = None
    return _nc


async def publish(subject: str, payload: dict) -> None:
    nc = await get_nats()
    if nc:
        try:
            await nc.publish(subject, json.dumps(payload).encode())
        except Exception:
            pass
    # also write to in-memory event log
    academy_events.append({
        "id": str(uuid.uuid4()),
        "type": subject,
        "payload": payload,
        "emitted_at": datetime.utcnow().isoformat(),
    })


# ──────────────────────────────────────────────────────────────────────────────
# In-Memory Data Stores (production: substituir por asyncpg + PostgreSQL)
# ──────────────────────────────────────────────────────────────────────────────
courses_db: list[dict] = []
modules_db: list[dict] = []
lessons_db: list[dict] = []
tracks_db: list[dict] = []
enrollments_db: list[dict] = []
lesson_progress_db: list[dict] = []
certifications_db: list[dict] = []
cognitive_profiles_db: dict[str, dict] = {}
error_lessons_db: list[dict] = []
sandbox_db: list[dict] = []
replays_db: list[dict] = []
onboardings_db: list[dict] = []
legal_acceptances_db: list[dict] = []
academy_events: list[dict] = []
john_dna_db: list[dict] = []
task_learnings_db: list[dict] = []
saas_offers_db: list[dict] = []
marketplace_db: list[dict] = []
whitelabels_db: list[dict] = []
cefeida_analyses_db: list[dict] = []
dynamic_contents_db: list[dict] = []
gamification_db: list[dict] = []

# Core LICEU Training seed
tracks_db = [
    {
        "id": str(uuid.uuid4()), "name": "CORE LICEU TRAINING",
        "monolith": None, "is_mandatory": True, "is_core_liceu": True,
        "modules": ["Cultura LICEU", "Uso do Kanban Global", "Uso do John",
                    "Governança do Ecossistema", "Compliance Jurídico Básico"],
    },
    {"id": str(uuid.uuid4()), "name": "Archimedes Track", "monolith": "archimedes", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["Fundamentos Imobiliários", "CRM Avançado", "Negociação Imobiliária", "Jurídico Imobiliário", "BIM para Incorporação"]},
    {"id": str(uuid.uuid4()), "name": "Game MKT Track", "monolith": "gameMkt", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["Marketing Digital", "Growth Hacking", "Funil de Vendas", "Conteúdo Estratégico", "Analytics"]},
    {"id": str(uuid.uuid4()), "name": "Jurídico Track", "monolith": "juridico", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["LGPD", "Contratos Imobiliários", "Não-Circunvenção", "Compliance Corporativo", "Regulatório"]},
    {"id": str(uuid.uuid4()), "name": "Finance Track", "monolith": "cea", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["CEA Básico", "Análise de Crédito", "Gestão de Caixa", "FIIs e Fundos", "Compliance Financeiro"]},
    {"id": str(uuid.uuid4()), "name": "OPERA Track", "monolith": "opera", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["Planejamento de Obras", "Gestão de Canteiro", "IoT Predial", "Microgrid", "Controle de Qualidade"]},
    {"id": str(uuid.uuid4()), "name": "CEFEIDA Data Track", "monolith": "cefeida", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["Python para Dados", "Machine Learning Aplicado", "Análise Preditiva", "ETL e Pipelines", "Dashboards"]},
    {"id": str(uuid.uuid4()), "name": "John Copilot Track", "monolith": "john", "is_mandatory": False, "is_core_liceu": False,
     "modules": ["Uso do John", "Prompts Avançados", "Tomada de Decisão com IA", "Governança de IA", "Integração John + Monólitos"]},
]

compliance_courses = [
    {"id": 1, "title": "LGPD — Lei Geral de Proteção de Dados", "duration": "4h", "mandatory": True, "domain": "juridico"},
    {"id": 2, "title": "Cláusula de Não-Circunvenção", "duration": "2h", "mandatory": True, "domain": "juridico"},
    {"id": 3, "title": "Contratos: fundamentos e boas práticas", "duration": "3h", "mandatory": True, "domain": "juridico"},
    {"id": 4, "title": "Compliance Corporativo", "duration": "3h", "mandatory": True, "domain": "compliance"},
    {"id": 5, "title": "Ética e Conduta no Ecossistema", "duration": "1h30", "mandatory": True, "domain": "compliance"},
]

mandatory_tracks_by_role = {
    "corretor": ["vendas", "juridico_basico", "crm", "cultura_liceu"],
    "financeiro": ["cea", "compliance", "cultura_liceu", "uso_john"],
    "gestor": ["governanca", "lideranca", "cultura_liceu", "kanban_global", "uso_john"],
    "tecnico": ["opera", "bim_basico", "cultura_liceu"],
    "analista_dados": ["cefeida_data", "python_basico", "cultura_liceu", "uso_john"],
    "juridico": ["lgpd", "contratos", "nao_circunvencao", "compliance", "cultura_liceu"],
}

contract_mandatory = {
    "clt": ["cultura_liceu", "compliance_trabalhista", "uso_john", "kanban_global", "governanca_ecossistema"],
    "pj": ["nao_circunvencao", "lgpd", "contratos_pj", "compliance_fiscal", "cultura_liceu"],
}

# ──────────────────────────────────────────────────────────────────────────────
# RBAC
# ──────────────────────────────────────────────────────────────────────────────
RBAC: dict[str, list[str]] = {
    "ADMIN":          ["*"],
    "INSTRUCTOR":     ["courses:create", "courses:read", "tracks:read", "users:read", "metrics:read"],
    "USER":           ["courses:read", "lessons:complete", "progress:write"],
    "CLIENTE_EXTERNO":["saas:read", "marketplace:read"],
}

HOLDING_RBAC: dict[str, list[str]] = {
    "holding_admin":    ["*"],
    "academy_director": ["courses:*", "tracks:*", "hr:*", "metrics:*", "john:*", "cefeida:*", "legal:*", "saas:*", "whitelabel:*"],
    "pd_ia_operator":   ["courses:read", "cefeida:*", "metrics:read"],
    "instructor":       ["courses:read", "courses:create", "tracks:read", "sandbox:execute", "replay:read", "john:execute"],
    "operations":       ["courses:read", "hr:read", "sandbox:execute", "metrics:read"],
    "auditor":          ["courses:read", "tracks:read", "metrics:read", "legal:read", "replay:read"],
}

holding_users = {
    "HLD-001": {"id": "HLD-001", "name": "Ana Souza",    "role": "holding_admin"},
    "HLD-002": {"id": "HLD-002", "name": "Bruno Lima",   "role": "academy_director"},
    "HLD-003": {"id": "HLD-003", "name": "Carla Mendes", "role": "pd_ia_operator"},
    "HLD-004": {"id": "HLD-004", "name": "Diego Rocha",  "role": "instructor"},
    "HLD-005": {"id": "HLD-005", "name": "Elisa Costa",  "role": "operations"},
    "HLD-006": {"id": "HLD-006", "name": "Fabio Nunes",  "role": "auditor"},
}


def require_permission(resource: str, action: str):
    """Dependency: valida x-holding-user-id e permissão RBAC."""
    def dependency(request: Request):
        user_id = request.headers.get("x-holding-user-id")
        if not user_id:
            raise HTTPException(401, "Header x-holding-user-id obrigatorio.")
        user = holding_users.get(user_id)
        if not user:
            raise HTTPException(401, "Usuário da Holding não encontrado.")
        perms = HOLDING_RBAC.get(user["role"], [])
        needed = f"{resource}:{action}"
        if "*" not in perms and needed not in perms and f"{resource}:*" not in perms:
            raise HTTPException(403, f"Acesso negado. Requerido: {needed}. Role: {user['role']}")
        return user
    return Depends(dependency)


# ──────────────────────────────────────────────────────────────────────────────
# Pydantic Models
# ──────────────────────────────────────────────────────────────────────────────
from pydantic import BaseModel, Field  # noqa: E402


class CourseCreate(BaseModel):
    title: str
    description: str | None = None
    monolith: str | None = None
    domain: str
    level: str = "basico"
    is_required: bool = False
    is_compliance: bool = False
    workload_hours: float | None = None
    skill_tags: list[str] = []


class EnrollRequest(BaseModel):
    user_id: str
    course_id: str
    source: str = "manual"


class CompleteLessonRequest(BaseModel):
    user_id: str
    lesson_id: str
    score: float = Field(ge=0, le=100)


class ProgressUpdate(BaseModel):
    user_id: str
    completed_modules: list[str] = []
    percentage_done: float = Field(default=0, ge=0, le=100)


class JohnTrainRequest(BaseModel):
    user_id: str
    current_scores: dict[str, float] = {}
    completed_courses: list[str] = []


class CognitiveScoreRequest(BaseModel):
    skill_matrix: dict[str, float] = {}
    specialization_level: str = "junior"
    notes: str | None = None


class ErrorLessonRequest(BaseModel):
    user_id: str
    error_type: str
    source_system: str
    error_description: str | None = None


class SandboxRequest(BaseModel):
    user_id: str
    simulation_type: str
    scenario: str | None = "padrao"


class ReplayRequest(BaseModel):
    user_id: str
    replay_type: str
    reference_id: str
    source_system: str | None = "ecossistema"


class AutoCertifyRequest(BaseModel):
    user_id: str
    track_id: str
    kpi_score: float = 0
    approved_by_john: bool = False
    execution_approved: bool = False


class OnboardingRequest(BaseModel):
    user_id: str
    name: str | None = None
    role: str
    contract_type: str


class LegalAcceptRequest(BaseModel):
    user_id: str
    course_id: int


class SaasOfferCreate(BaseModel):
    title: str
    domain: str
    price: float
    level: str = "intermediario"
    target_audience: str = "mercado"
    certification_included: bool = False


class MarketplaceCourseCreate(BaseModel):
    title: str
    domain: str
    author_id: str
    author_type: str = "especialista"
    price: float = 0
    skill_tags: list[str] = []


class WhitelabelCreate(BaseModel):
    company_id: str
    company_name: str
    tracks: list[str] = []
    custom_branding: dict = {}


class CefeidaAnalyzeRequest(BaseModel):
    user_id: str
    study_behavior: dict = {}
    performance_history: list[float] = []
    error_patterns: list[str] = []


class CefeidaContentRequest(BaseModel):
    user_id: str
    domain: str
    format: str = "microlearning"
    target_level: str = "intermediario"


class JohnTeachRequest(BaseModel):
    user_id: str
    topic: str
    doubt: str | None = None


class JohnDnaFeedRequest(BaseModel):
    source: str
    knowledge: str
    domain: str
    confidence: float = Field(default=0.8, ge=0, le=1)


class KanbanTaskRequest(BaseModel):
    task_id: str
    user_id: str
    task_title: str | None = None
    task_domain: str
    task_outcome: str | None = None


class ComplianceCheckRequest(BaseModel):
    user_id: str


class SimulateDealRequest(BaseModel):
    user_id: str
    context: str | None = None


class GenerateFromTaskRequest(BaseModel):
    task_id: str
    domain: str | None = None


# ──────────────────────────────────────────────────────────────────────────────
# Root
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Status"])
async def root():
    return {
        "project": "Academia do Saber — LICEU",
        "version": "1.0.0",
        "status": "online",
        "auth": "header x-holding-user-id (RBAC Holding)",
    }


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 1 — Domínio Educacional Unificado
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/courses", tags=["Issue 1 — Core Educacional"])
async def list_courses(
    domain: str | None = None,
    monolith: str | None = None,
    _user=require_permission("courses", "read"),
):
    result = courses_db
    if domain:
        result = [c for c in result if c.get("domain") == domain]
    if monolith:
        result = [c for c in result if c.get("monolith") == monolith]
    return result


@app.post("/academy/courses", status_code=201, tags=["Issue 1 — Core Educacional"])
async def create_course(body: CourseCreate, _user=require_permission("courses", "create")):
    course = {
        "id": str(uuid.uuid4()),
        **body.model_dump(),
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
    }
    courses_db.append(course)
    return course


@app.post("/academy/enroll", status_code=201, tags=["Issue 1 — Core Educacional"])
async def enroll(body: EnrollRequest, _user=require_permission("courses", "read")):
    existing = next((e for e in enrollments_db if e["user_id"] == body.user_id and e["course_id"] == body.course_id), None)
    if existing:
        raise HTTPException(409, "Usuário já matriculado neste curso.")

    record = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "course_id": body.course_id,
        "status": "in_progress",
        "progress": 0,
        "source": body.source,
        "enrolled_at": datetime.utcnow().isoformat(),
    }
    enrollments_db.append(record)
    await publish("academy.enrolled", {"user_id": body.user_id, "course_id": body.course_id})
    return record


@app.post("/academy/lesson/complete", tags=["Issue 1 — Core Educacional"])
async def complete_lesson(body: CompleteLessonRequest):
    record = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "lesson_id": body.lesson_id,
        "completed": True,
        "score": body.score,
        "completed_at": datetime.utcnow().isoformat(),
    }
    lesson_progress_db.append(record)

    await publish("academy.lesson.completed", {"user_id": body.user_id, "lesson_id": body.lesson_id, "score": body.score})
    # Trigger John learning
    await publish("john.learn", {"type": "lesson_feedback", "user": body.user_id, "score": body.score})
    return {"ok": True, "record": record}


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 2 — Trilhas por Monólito
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/tracks", tags=["Issue 2/3 — Trilhas"])
async def list_tracks(_user=require_permission("tracks", "read")):
    return tracks_db


@app.get("/academy/tracks/{monolith}", tags=["Issue 2/3 — Trilhas"])
async def get_track_by_monolith(monolith: str, _user=require_permission("tracks", "read")):
    track = next((t for t in tracks_db if t.get("monolith") == monolith), None)
    if not track:
        raise HTTPException(404, f"Trilha para monólito '{monolith}' não encontrada.")
    return track


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 3 — Core LICEU Training
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/training/core-liceu", tags=["Issue 2/3 — Trilhas"])
async def core_liceu_training(_user=require_permission("tracks", "read")):
    core = next((t for t in tracks_db if t.get("is_core_liceu")), None)
    if not core:
        raise HTTPException(404, "CORE LICEU TRAINING não encontrado.")
    return core


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 4 — John Training Engine
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/john/train", tags=["Issue 4/5/6 — John Engine"])
async def john_train(body: JohnTrainRequest, _user=require_permission("john", "execute")):
    weak = [skill for skill, score in body.current_scores.items() if score < 60]
    difficulty = (
        "basico" if len(body.completed_courses) < 3
        else "intermediario" if len(body.completed_courses) < 8
        else "avancado"
    )
    plan = {
        "user_id": body.user_id,
        "analyzed_at": datetime.utcnow().isoformat(),
        "weak_areas": weak,
        "suggested_actions": [f"Reforço em: {s}" for s in weak] or ["Avance para trilha intermediária"],
        "recommended_difficulty": difficulty,
        "next_step": (f"Reforço em: {weak[0]}" if weak else "Explorar trilha avançada"),
    }
    await publish("academy.john_recommended", {"user_id": body.user_id, "plan": plan})
    return plan


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 5 — Score Cognitivo
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/users/{user_id}/cognitive-score", tags=["Issue 4/5/6 — John Engine"])
async def get_cognitive_score(user_id: str, _user=require_permission("courses", "read")):
    profile = cognitive_profiles_db.get(user_id)
    if not profile:
        raise HTTPException(404, "Score cognitivo não encontrado.")
    return profile


@app.post("/academy/users/{user_id}/cognitive-score", status_code=201, tags=["Issue 4/5/6 — John Engine"])
async def upsert_cognitive_score(user_id: str, body: CognitiveScoreRequest, _user=require_permission("courses", "read")):
    vals = list(body.skill_matrix.values())
    avg = sum(vals) / len(vals) if vals else 0
    profile = {
        "user_id": user_id,
        "skill_matrix": body.skill_matrix,
        "specialization_level": body.specialization_level,
        "cognitive_score": round(avg, 2),
        "notes": body.notes,
        "updated_at": datetime.utcnow().isoformat(),
    }
    cognitive_profiles_db[user_id] = profile
    return profile


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 6 — Aprendizado Baseado em Erro
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/john/learn-from-error", status_code=201, tags=["Issue 4/5/6 — John Engine"])
async def learn_from_error(body: ErrorLessonRequest, _user=require_permission("john", "execute")):
    domain_map = {"deal": "vendas", "contract": "juridico", "financial": "financeiro", "audit": "compliance", "loss": "operacoes"}
    domain = domain_map.get(body.error_type.lower(), "geral")

    lesson = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "error_type": body.error_type,
        "source_system": body.source_system,
        "error_description": body.error_description,
        "generated_lesson": {
            "title": f"Lição automática: {body.error_type} em {body.source_system}",
            "domain": domain,
            "content": f"Baseado no erro registrado em {body.source_system}, recomendamos revisão dos módulos de {domain}.",
            "exercises": [f"Simulação de cenário real: {body.error_type}", "Revisão de conformidade", "Teste de absorção de conteúdo"],
            "estimated_duration": "45min",
        },
        "created_at": datetime.utcnow().isoformat(),
    }
    error_lessons_db.append(lesson)
    await publish("academy.john_recommended", {"user_id": body.user_id, "lesson_id": lesson["id"], "trigger": "error"})
    return lesson


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 7 — Simulação Real (Sandbox)
# ──────────────────────────────────────────────────────────────────────────────
SANDBOX_META = {
    "venda":      {"monolith": "archimedes", "desc": "Simulação de fluxo de venda imobiliária"},
    "negociacao": {"monolith": "sales_os",   "desc": "Simulação de negociação avançada"},
    "contrato":   {"monolith": "juridico",   "desc": "Simulação de assinatura e análise contratual"},
    "financeiro": {"monolith": "cea",        "desc": "Simulação de análise de crédito e aprovação"},
}


@app.post("/academy/sandbox/simulate", status_code=201, tags=["Issue 7/8/9 — Treinamento Operacional"])
async def sandbox_simulate(body: SandboxRequest, _user=require_permission("sandbox", "execute")):
    meta = SANDBOX_META.get(body.simulation_type.lower(), {"monolith": "geral", "desc": "Simulação genérica"})
    score = random.randint(70, 100)
    sim = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "simulation_type": body.simulation_type,
        "scenario": body.scenario,
        "monolith": meta["monolith"],
        "description": meta["desc"],
        "score": score,
        "outcome": "aprovado" if score >= 75 else "em_reforco",
        "feedback": (
            "Excelente desempenho na simulação. Pronto para operação real."
            if score >= 75
            else "Revise os módulos relacionados antes de operar em produção."
        ),
        "created_at": datetime.utcnow().isoformat(),
    }
    sandbox_db.append(sim)
    return sim


@app.post("/academy/simulate/deal", tags=["Issue 9 — Simulation Engine"])
async def simulate_deal(body: SimulateDealRequest, _user=require_permission("sandbox", "execute")):
    """Cenário de simulação de deal — engine de treino real."""
    return {
        "user_id": body.user_id,
        "scenario": body.context or "cliente indeciso",
        "options": ["pressionar", "educar", "oferecer desconto", "apresentar cases", "escalar para gestor"],
        "hint": "Identifique o perfil do cliente antes de escolher a abordagem.",
        "generated_at": datetime.utcnow().isoformat(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 8 — Replay de Operações Reais
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/replay", status_code=201, tags=["Issue 7/8/9 — Treinamento Operacional"])
async def create_replay(body: ReplayRequest, _user=require_permission("replay", "read")):
    replay = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "replay_type": body.replay_type,
        "reference_id": body.reference_id,
        "source_system": body.source_system,
        "insights": [
            f"Ponto crítico identificado no {body.replay_type} #{body.reference_id}",
            "Oportunidade de melhoria na tomada de decisão",
            "Recomendação: revisar trilha correspondente",
        ],
        "replayed_at": datetime.utcnow().isoformat(),
    }
    replays_db.append(replay)
    await publish("academy.replay.created", {"user_id": body.user_id, "reference_id": body.reference_id})
    return replay


@app.get("/academy/replay", tags=["Issue 7/8/9 — Treinamento Operacional"])
async def list_replays(user_id: str | None = Query(default=None), _user=require_permission("replay", "read")):
    result = [r for r in replays_db if r["user_id"] == user_id] if user_id else replays_db
    return result


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 9 — Certificação por Performance
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/certification/auto-certify", status_code=201, tags=["Issue 7/8/9 — Treinamento Operacional"])
async def auto_certify(body: AutoCertifyRequest, _user=require_permission("courses", "read")):
    approved = body.kpi_score >= 75 or body.approved_by_john or body.execution_approved
    cert = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "track_id": body.track_id,
        "kpi_score": body.kpi_score,
        "approved_by_john": body.approved_by_john,
        "execution_approved": body.execution_approved,
        "status": "certificado" if approved else "reprovado",
        "issued_at": datetime.utcnow().isoformat() if approved else None,
        "reason": "Aprovado por performance real" if approved else "KPI abaixo do mínimo (75) sem aprovação complementar",
    }
    certifications_db.append(cert)
    await publish("academy.certified" if approved else "academy.failed", {"user_id": body.user_id, "track_id": body.track_id})
    return cert


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 10-12 — RH + Onboarding + Contratos
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/onboarding", status_code=201, tags=["Issues 10-12 — RH / HubBackoffice"])
async def onboarding(body: OnboardingRequest, _user=require_permission("hr", "read")):
    role_tracks = mandatory_tracks_by_role.get(body.role.lower(), ["cultura_liceu"])
    contract_tracks_ = contract_mandatory.get(body.contract_type.lower(), [])
    all_tracks = list(set(role_tracks + contract_tracks_))

    record = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "name": body.name or body.user_id,
        "role": body.role,
        "contract_type": body.contract_type,
        "mandatory_tracks": all_tracks,
        "completed_tracks": [],
        "training_status": "pending",
        "started_at": datetime.utcnow().isoformat(),
    }
    onboardings_db.append(record)
    await publish("academy.onboarding.started", {"user_id": body.user_id, "tracks": all_tracks})
    # Sync to HubBackoffice
    await publish("hub.rh.training_required", {"user": body.user_id, "track": "core_liceu"})
    return record


@app.get("/academy/onboarding/{user_id}", tags=["Issues 10-12 — RH / HubBackoffice"])
async def get_onboarding(user_id: str, _user=require_permission("hr", "read")):
    record = next((o for o in onboardings_db if o["user_id"] == user_id), None)
    if not record:
        raise HTTPException(404, "Onboarding não encontrado.")
    return record


@app.get("/academy/hr/mandatory-tracks/{role}", tags=["Issues 10-12 — RH / HubBackoffice"])
async def mandatory_tracks(role: str, _user=require_permission("hr", "read")):
    tracks = mandatory_tracks_by_role.get(role.lower())
    if not tracks:
        raise HTTPException(404, f"Função '{role}' não encontrada. Disponíveis: {list(mandatory_tracks_by_role)}")
    return {"role": role, "mandatory_tracks": tracks}


@app.get("/academy/hr/contract-tracks/{contract_type}", tags=["Issues 10-12 — RH / HubBackoffice"])
async def contract_tracks_endpoint(contract_type: str, _user=require_permission("hr", "read")):
    tracks = contract_mandatory.get(contract_type.lower())
    if not tracks:
        raise HTTPException(404, "Use: clt ou pj")
    return {"contract_type": contract_type.upper(), "mandatory_tracks": tracks}


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 13-14 — JuridicoTech: Compliance + Aceite
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/legal/compliance-courses", tags=["Issues 13-14 — JuridicoTech"])
async def list_compliance(_user=require_permission("legal", "read")):
    return compliance_courses


@app.post("/academy/legal/sign-acceptance", status_code=201, tags=["Issues 13-14 — JuridicoTech"])
async def sign_acceptance(body: LegalAcceptRequest, _user=require_permission("legal", "read")):
    course = next((c for c in compliance_courses if c["id"] == body.course_id), None)
    if not course:
        raise HTTPException(404, "Curso de compliance não encontrado.")

    existing = next((a for a in legal_acceptances_db if a["user_id"] == body.user_id and a["course_id"] == body.course_id), None)
    if existing:
        return existing

    acceptance = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "course_id": body.course_id,
        "course_title": course["title"],
        "signature": f"ACEITE-{body.user_id}-{body.course_id}-{int(datetime.utcnow().timestamp())}",
        "accepted_at": datetime.utcnow().isoformat(),
    }
    legal_acceptances_db.append(acceptance)
    await publish("academy.compliance.accepted", {"user_id": body.user_id, "course_id": body.course_id})
    # Sync juridicotech validation
    await publish("juridico.validate_training", {"user": body.user_id})
    return acceptance


@app.post("/academy/compliance/check", tags=["Issues 13-14 — JuridicoTech"])
async def compliance_check(body: ComplianceCheckRequest, _user=require_permission("legal", "read")):
    accepted = [a["course_id"] for a in legal_acceptances_db if a["user_id"] == body.user_id]
    required = [c["id"] for c in compliance_courses if c["mandatory"]]
    pending = [c for c in required if c not in accepted]
    await publish("juridico.validate_training", {"user": body.user_id})
    return {
        "user_id": body.user_id,
        "required_courses": len(required),
        "completed_courses": len(accepted),
        "pending_courses": pending,
        "is_compliant": len(pending) == 0,
    }


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 15-16 — Metrics & Performance
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/dashboard", tags=["Issues 15-16 — Metrics"])
async def dashboard():
    """Endpoint público/leve para o frontend React."""
    return {
        "courses": courses_db[:20],
        "progress": {e["course_id"]: e["progress"] for e in enrollments_db},
        "recommendations": [
            {"id": 1, "title": "Treinar negociação"},
            {"id": 2, "title": "Revisar jurídico"},
            {"id": 3, "title": "Completar CORE LICEU"},
        ],
    }


@app.get("/academy/metrics", tags=["Issues 15-16 — Metrics"])
async def metrics(_user=require_permission("metrics", "read")):
    total = len(enrollments_db)
    completed = len([e for e in enrollments_db if e["status"] == "completed"])
    avg_score = (
        sum(l["score"] for l in lesson_progress_db if l.get("score")) / len(lesson_progress_db)
        if lesson_progress_db else 0
    )
    certified = len([c for c in certifications_db if c["status"] == "certificado"])
    return {
        "completion_rate": round((completed / total * 100), 1) if total else 0,
        "avg_score": round(avg_score / 100, 2),
        "total_enrollments": total,
        "total_certifications": certified,
        "impact_on_sales": 23,  # placeholder — correlação real com Archimedes
        "total_courses": len(courses_db),
        "total_sandbox_simulations": len(sandbox_db),
    }


@app.get("/academy/metrics/dashboard", tags=["Issues 15-16 — Metrics"])
async def metrics_dashboard(_user=require_permission("metrics", "read")):
    track_completion: dict[str, Any] = {}
    for o in onboardings_db:
        for t in o["mandatory_tracks"]:
            track_completion.setdefault(t, {"track": t, "enrolled": 0, "completed": 0})
            track_completion[t]["enrolled"] += 1
            if t in o["completed_tracks"]:
                track_completion[t]["completed"] += 1

    return {
        "kpis": {
            "total_enrollments": len(enrollments_db),
            "completed_certifications": len([c for c in certifications_db if c["status"] == "certificado"]),
            "average_kpi_score": (
                round(sum(c["kpi_score"] for c in certifications_db) / len(certifications_db), 2)
                if certifications_db else 0
            ),
            "total_courses": len(courses_db),
            "total_sandbox": len(sandbox_db),
            "total_replays": len(replays_db),
        },
        "track_completion": list(track_completion.values()),
        "recent_events": academy_events[-10:],
    }


@app.get("/academy/metrics/correlation", tags=["Issues 15-16 — Metrics"])
async def metrics_correlation(_user=require_permission("metrics", "read")):
    certified_users = {c["user_id"] for c in certifications_db if c["status"] == "certificado"}
    correlations = []
    for user_id in certified_users:
        user_sandbox = [s for s in sandbox_db if s["user_id"] == user_id]
        avg_sb = sum(s["score"] for s in user_sandbox) / len(user_sandbox) if user_sandbox else 0
        cert = next((c for c in certifications_db if c["user_id"] == user_id and c["status"] == "certificado"), None)
        correlations.append({
            "user_id": user_id,
            "certified": True,
            "average_sandbox_score": round(avg_sb, 2),
            "kpi_score": cert["kpi_score"] if cert else None,
            "insight": (
                "Alta correlação: treinamento intenso impacta resultado real"
                if avg_sb >= 80 else
                "Treinamento básico: potencial de melhora com trilhas avançadas"
            ),
        })
    return {"correlations": correlations, "analyzed_at": datetime.utcnow().isoformat()}


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 17-19 — EdTech Externo (SaaS, Marketplace, White-label)
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/saas/courses", tags=["Issues 17-19 — EdTech Externo"])
async def list_saas(_user=require_permission("saas", "read")):
    return saas_offers_db


@app.post("/academy/saas/courses", status_code=201, tags=["Issues 17-19 — EdTech Externo"])
async def create_saas(body: SaasOfferCreate, _user=require_permission("saas", "read")):
    offer = {"id": str(uuid.uuid4()), **body.model_dump(), "type": "saas_externo", "created_at": datetime.utcnow().isoformat()}
    saas_offers_db.append(offer)
    return offer


@app.get("/academy/marketplace/courses", tags=["Issues 17-19 — EdTech Externo"])
async def list_marketplace(_user=require_permission("marketplace", "read")):
    return marketplace_db


@app.post("/academy/marketplace/courses", status_code=201, tags=["Issues 17-19 — EdTech Externo"])
async def publish_marketplace(body: MarketplaceCourseCreate, _user=require_permission("marketplace", "read")):
    course = {"id": str(uuid.uuid4()), **body.model_dump(), "status": "pending_review", "type": "marketplace", "created_at": datetime.utcnow().isoformat()}
    marketplace_db.append(course)
    return course


@app.post("/academy/whitelabel/setup", status_code=201, tags=["Issues 17-19 — EdTech Externo"])
async def setup_whitelabel(body: WhitelabelCreate, _user=require_permission("courses", "read")):
    if any(w["company_id"] == body.company_id for w in whitelabels_db):
        raise HTTPException(409, "White-label já existe para esta empresa.")
    wl = {"id": str(uuid.uuid4()), **body.model_dump(), "status": "active", "created_at": datetime.utcnow().isoformat()}
    whitelabels_db.append(wl)
    return wl


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 20-21 — Eventos NATS / Ecossistema
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/events", tags=["Issues 20-21 — Eventos NATS"])
async def list_events(type: str | None = Query(default=None), _user=require_permission("courses", "read")):
    result = [e for e in academy_events if e["type"] == type] if type else academy_events
    return result


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 22-23 — CEFEIDA: IA de Aprendizado
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/cefeida/analyze", status_code=201, tags=["Issues 22-23 — CEFEIDA IA"])
async def cefeida_analyze(body: CefeidaAnalyzeRequest, _user=require_permission("cefeida", "read")):
    avg = sum(body.performance_history) / len(body.performance_history) if body.performance_history else 0
    analysis = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "analyzed_at": datetime.utcnow().isoformat(),
        "study_behavior": body.study_behavior,
        "average_performance": round(avg, 2),
        "top_error_patterns": body.error_patterns[:3],
        "recommendations": [f"Reforçar área: {e}" for e in body.error_patterns[:3]] or ["Manter ritmo atual"],
        "adaptive_path": "avancado" if avg >= 80 else "intermediario" if avg >= 60 else "basico",
    }
    cefeida_analyses_db.append(analysis)
    return analysis


@app.post("/academy/cefeida/generate-content", status_code=201, tags=["Issues 22-23 — CEFEIDA IA"])
async def cefeida_generate(body: CefeidaContentRequest, _user=require_permission("cefeida", "read")):
    is_micro = body.format == "microlearning"
    content = {
        "id": str(uuid.uuid4()),
        "user_id": body.user_id,
        "domain": body.domain,
        "format": body.format,
        "target_level": body.target_level,
        "generated_content": {
            "title": f"{'Micro-aula' if is_micro else 'Trilha Adaptativa'}: {body.domain}",
            "summary": f"Conteúdo dinâmico gerado pela CEFEIDA para {body.domain} — nível {body.target_level}.",
            "steps": [
                f"Introdução rápida ao tema: {body.domain}",
                "Exercício prático contextualizado",
                "Quiz de absorção (5 questões)",
                "Caso real do ecossistema LICEU",
                "Recomendação próxima etapa",
            ],
            "estimated_duration": "15min" if is_micro else "2h",
        },
        "created_at": datetime.utcnow().isoformat(),
    }
    dynamic_contents_db.append(content)
    return content


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 24-25 — Dashboard Institucional + Ranking
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/dashboard/institutional", tags=["Issues 24-25 — Trading Desk"])
async def institutional_dashboard(_user=require_permission("metrics", "read")):
    ranked = sorted(gamification_db, key=lambda s: s.get("score", 0), reverse=True)[:10]
    late = [o for o in onboardings_db if o["training_status"] == "pending" and not o["completed_tracks"]]
    return {
        "blocks": {
            "total_tracks": len(tracks_db),
            "global_progress": len(enrollments_db),
            "ranking_top_10": [{"position": i + 1, "user_id": s["user_id"], "score": s["score"]} for i, s in enumerate(ranked)],
            "late_alerts": [{"user_id": o["user_id"], "role": o["role"], "pending": len(o["mandatory_tracks"])} for o in late],
            "john_recommendations": [e for e in academy_events if e["type"] == "academy.john_recommended"][-5:],
        },
        "updated_at": datetime.utcnow().isoformat(),
    }


@app.get("/academy/ranking/gamified", tags=["Issues 24-25 — Trading Desk"])
async def gamified_ranking(_user=require_permission("courses", "read")):
    cert_map: dict[str, int] = {}
    for c in certifications_db:
        if c["status"] == "certificado":
            cert_map[c["user_id"]] = cert_map.get(c["user_id"], 0) + 1

    session_map: dict[str, dict] = {}
    for s in sandbox_db:
        uid = s["user_id"]
        session_map.setdefault(uid, {"xp": 0, "sessions": 0})
        session_map[uid]["xp"] += int(s.get("score", 0))
        session_map[uid]["sessions"] += 1

    ranking = []
    for user_id, data in session_map.items():
        xp = data["xp"] + cert_map.get(user_id, 0) * 200
        level = "Aprendiz" if xp < 500 else "Praticante" if xp < 1500 else "Especialista" if xp < 3000 else "Mestre"
        ranking.append({"user_id": user_id, "xp": xp, "level": level, "sessions": data["sessions"], "certifications": cert_map.get(user_id, 0)})

    ranking.sort(key=lambda r: r["xp"], reverse=True)
    for i, r in enumerate(ranking):
        r["position"] = i + 1
    return ranking


# ──────────────────────────────────────────────────────────────────────────────
# ISSUES 26-27 — RBAC Educacional
# ──────────────────────────────────────────────────────────────────────────────
@app.get("/academy/rbac/roles", tags=["Issues 26-27 — RBAC"])
async def list_edu_roles(_user=require_permission("courses", "read")):
    return RBAC


@app.get("/academy/rbac/roles/{role}", tags=["Issues 26-27 — RBAC"])
async def get_edu_role(role: str, _user=require_permission("courses", "read")):
    perms = RBAC.get(role.upper())
    if not perms:
        raise HTTPException(404, f"Role '{role}' não encontrada. Disponíveis: {list(RBAC)}")
    return {"role": role.upper(), "permissions": perms}


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 28 — John DNA Feed
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/john/feed-dna", status_code=201, tags=["Issues 28-29 — John Professor / DNA"])
async def john_feed_dna(body: JohnDnaFeedRequest, _user=require_permission("courses", "read")):
    entry = {
        "id": str(uuid.uuid4()),
        **body.model_dump(),
        "status": "absorbed",
        "absorbed_at": datetime.utcnow().isoformat(),
    }
    john_dna_db.append(entry)
    await publish("core_dna.update", {"user": "john", "skill": body.domain, "knowledge": body.knowledge})
    return {"message": "Conhecimento absorvido pelo core_dna do John.", "entry": entry}


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 29 — John como Professor
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/john/teach", tags=["Issues 28-29 — John Professor / DNA"])
async def john_teach(body: JohnTeachRequest, _user=require_permission("john", "execute")):
    return {
        "teacher": "John Brasileiro — IA Pedagógico",
        "user_id": body.user_id,
        "topic": body.topic,
        "answered_doubt": body.doubt,
        "lesson": {
            "introduction": f"Olá! Vou te ensinar sobre {body.topic} de forma aplicada ao ecossistema LICEU.",
            "key_points": [
                f"Conceito central de {body.topic}",
                "Aplicação prática no ecossistema",
                "Caso real simulado",
                "Exercício rápido",
            ],
            "scenario": f"Imagine que você está operando no monólito correspondente a {body.topic}. Como tomaria a decisão certa?",
            "challenge": f"Dado um cenário real de {body.topic}, qual seria o melhor passo seguinte?",
            "next_recommendation": f"Após dominar {body.topic}, explore a trilha avançada relacionada.",
        },
        "generated_at": datetime.utcnow().isoformat(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# ISSUE 30 — Kanban Global: Task como Aprendizado
# ──────────────────────────────────────────────────────────────────────────────
@app.post("/academy/from-task", status_code=201, tags=["Issue 30 — Kanban"])
async def generate_from_task(body: GenerateFromTaskRequest, _user=require_permission("courses", "read")):
    """Integração direta com Kanban — task dispara evento de treinamento."""
    await publish("academy.generate", {"source": "kanban", "task": body.task_id, "domain": body.domain})
    return {"ok": True, "task_id": body.task_id, "event": "academy.generate published"}


@app.post("/academy/kanban/task-learning", status_code=201, tags=["Issue 30 — Kanban"])
async def kanban_task_learning(body: KanbanTaskRequest, _user=require_permission("courses", "read")):
    needs_training = body.task_outcome in ("blocked", "failed")
    record = {
        "id": str(uuid.uuid4()),
        "task_id": body.task_id,
        "user_id": body.user_id,
        "task_title": body.task_title or f"Task #{body.task_id}",
        "task_domain": body.task_domain,
        "task_outcome": body.task_outcome or "completed",
        "generated_training": {
            "title": f"Treinamento gerado por task: {body.task_title or body.task_id}",
            "domain": body.task_domain,
            "reason": f"Task {body.task_outcome} — recomendação automática de reforço",
            "suggested_track": body.task_domain,
            "urgency": "alta",
        } if needs_training else None,
        "recommendation": (
            f"Recomendamos trilha de reforço em {body.task_domain} antes de retomar tarefas similares."
            if needs_training else
            f"Ótima execução! Continue evoluindo em {body.task_domain}."
        ),
        "processed_at": datetime.utcnow().isoformat(),
    }
    task_learnings_db.append(record)
    if needs_training:
        await publish("academy.task.learning_generated", {"user_id": body.user_id, "task_id": body.task_id, "domain": body.task_domain})
        await publish("academy.john_recommended", {"user_id": body.user_id, "trigger": "kanban_task", "domain": body.task_domain})
    return record
