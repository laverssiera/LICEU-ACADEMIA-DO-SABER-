-- ============================================================
-- ACADEMIA DO SABER — SCHEMA SQL ENTERPRISE
-- LICEU Ecossistema | PostgreSQL 15+
-- ============================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ──────────────────────────────────────────────────────────
-- Enum Types
-- ──────────────────────────────────────────────────────────
CREATE TYPE course_level       AS ENUM ('basico', 'intermediario', 'avancado');
CREATE TYPE lesson_type        AS ENUM ('video', 'text', 'simulation', 'quiz', 'sandbox');
CREATE TYPE enrollment_status  AS ENUM ('in_progress', 'completed', 'abandoned', 'blocked');
CREATE TYPE cert_source        AS ENUM ('kpi', 'john_approval', 'execution', 'manual');
CREATE TYPE contract_type      AS ENUM ('clt', 'pj', 'estagio', 'autonomo');
CREATE TYPE edu_role           AS ENUM ('ADMIN', 'INSTRUTOR', 'COLABORADOR', 'CLIENTE_EXTERNO');
CREATE TYPE event_type_enum    AS ENUM (
  'academy.enrolled',
  'academy.lesson.completed',
  'academy.course.completed',
  'academy.certified',
  'academy.failed',
  'academy.john_recommended',
  'academy.compliance.accepted',
  'academy.onboarding.started',
  'academy.sandbox.executed',
  'academy.replay.created',
  'academy.task.learning_generated'
);

-- ──────────────────────────────────────────────────────────
-- 1. USERS — espelhado do core (ISSUE 1, 10, 12, 26)
-- ──────────────────────────────────────────────────────────
CREATE TABLE academy_users (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    external_id     TEXT        UNIQUE,                  -- id vindo do core / holding
    email           TEXT        NOT NULL,
    name            TEXT,
    edu_role        edu_role    NOT NULL DEFAULT 'COLABORADOR',
    holding_role    TEXT,                                -- role no RBAC da holding
    monolith        TEXT,                                -- archimedes | opera | cea | juridico | cefeida ...
    contract_type   contract_type,
    is_active       BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_academy_users_external ON academy_users(external_id);
CREATE INDEX idx_academy_users_monolith ON academy_users(monolith);

-- ──────────────────────────────────────────────────────────
-- 2. COURSES (ISSUE 1, 2, 3, 17, 18)
-- ──────────────────────────────────────────────────────────
CREATE TABLE courses (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    title           TEXT        NOT NULL,
    description     TEXT,
    monolith        TEXT,                                -- trilha de qual monólito
    domain          TEXT,
    level           course_level NOT NULL DEFAULT 'basico',
    is_required     BOOLEAN     NOT NULL DEFAULT FALSE,  -- obrigatório por função
    is_compliance   BOOLEAN     NOT NULL DEFAULT FALSE,  -- compliance jurídico
    is_saas         BOOLEAN     NOT NULL DEFAULT FALSE,  -- produto externo (EdTech)
    is_marketplace  BOOLEAN     NOT NULL DEFAULT FALSE,  -- publicado por especialista
    price           NUMERIC(10,2) DEFAULT 0,
    skill_tags      TEXT[]      DEFAULT '{}',
    workload_hours  NUMERIC(5,1),
    author_id       UUID        REFERENCES academy_users(id) ON DELETE SET NULL,
    status          TEXT        NOT NULL DEFAULT 'active',
    created_at      TIMESTAMP   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_courses_monolith ON courses(monolith);
CREATE INDEX idx_courses_domain   ON courses(domain);
CREATE INDEX idx_courses_tags     ON courses USING GIN(skill_tags);

-- ──────────────────────────────────────────────────────────
-- 3. MODULES (ISSUE 1)
-- ──────────────────────────────────────────────────────────
CREATE TABLE modules (
    id          UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id   UUID    NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title       TEXT    NOT NULL,
    description TEXT,
    position    INT     NOT NULL DEFAULT 0
);

CREATE INDEX idx_modules_course ON modules(course_id);

-- ──────────────────────────────────────────────────────────
-- 4. LESSONS (ISSUE 1)
-- ──────────────────────────────────────────────────────────
CREATE TABLE lessons (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    module_id   UUID        NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title       TEXT        NOT NULL,
    content     TEXT,
    type        lesson_type NOT NULL DEFAULT 'text',
    video_url   TEXT,
    duration_min INT,
    position    INT         NOT NULL DEFAULT 0
);

CREATE INDEX idx_lessons_module ON lessons(module_id);

-- ──────────────────────────────────────────────────────────
-- 5. TRACKS — Trilhas por monólito e transversal (ISSUE 2, 3)
-- ──────────────────────────────────────────────────────────
CREATE TABLE tracks (
    id          UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT    NOT NULL UNIQUE,
    monolith    TEXT,                                -- null = transversal
    description TEXT,
    is_mandatory BOOLEAN NOT NULL DEFAULT FALSE,
    is_core_liceu BOOLEAN NOT NULL DEFAULT FALSE,   -- CORE LICEU TRAINING
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE track_courses (
    track_id    UUID NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    course_id   UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    position    INT  NOT NULL DEFAULT 0,
    PRIMARY KEY (track_id, course_id)
);

-- ──────────────────────────────────────────────────────────
-- 6. ENROLLMENTS (ISSUE 1, 10)
-- ──────────────────────────────────────────────────────────
CREATE TABLE enrollments (
    id          UUID                PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID                NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    course_id   UUID                NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    status      enrollment_status   NOT NULL DEFAULT 'in_progress',
    progress    FLOAT               NOT NULL DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    source      TEXT                DEFAULT 'manual',  -- hr_onboarding | john | kanban | manual
    enrolled_at TIMESTAMP           NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    UNIQUE (user_id, course_id)
);

CREATE INDEX idx_enrollments_user   ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_enrollments_status ON enrollments(status);

-- ──────────────────────────────────────────────────────────
-- 7. LESSON PROGRESS (ISSUE 1)
-- ──────────────────────────────────────────────────────────
CREATE TABLE lesson_progress (
    id           UUID      PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id      UUID      NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    lesson_id    UUID      NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    completed    BOOLEAN   NOT NULL DEFAULT FALSE,
    score        FLOAT     CHECK (score >= 0 AND score <= 100),
    attempts     INT       NOT NULL DEFAULT 1,
    completed_at TIMESTAMP,
    UNIQUE (user_id, lesson_id)
);

CREATE INDEX idx_lesson_progress_user   ON lesson_progress(user_id);
CREATE INDEX idx_lesson_progress_lesson ON lesson_progress(lesson_id);

-- ──────────────────────────────────────────────────────────
-- 8. CERTIFICATIONS (ISSUE 9)
-- ──────────────────────────────────────────────────────────
CREATE TABLE certifications (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID        NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    course_id       UUID        REFERENCES courses(id) ON DELETE SET NULL,
    track_id        UUID        REFERENCES tracks(id) ON DELETE SET NULL,
    score           FLOAT,
    kpi_score       FLOAT,
    source          cert_source NOT NULL DEFAULT 'kpi',
    approved_by_john BOOLEAN    DEFAULT FALSE,
    execution_approved BOOLEAN  DEFAULT FALSE,
    issued_at       TIMESTAMP   NOT NULL DEFAULT NOW(),
    expires_at      TIMESTAMP,
    UNIQUE (user_id, course_id)
);

CREATE INDEX idx_certifications_user ON certifications(user_id);

-- ──────────────────────────────────────────────────────────
-- 9. COGNITIVE PROFILES (ISSUE 5)
-- ──────────────────────────────────────────────────────────
CREATE TABLE cognitive_profiles (
    user_id             UUID      PRIMARY KEY REFERENCES academy_users(id) ON DELETE CASCADE,
    cognitive_score     FLOAT     DEFAULT 0,
    skill_matrix        JSONB     NOT NULL DEFAULT '{}',
    specialization_level TEXT     DEFAULT 'junior',
    weak_areas          TEXT[]    DEFAULT '{}',
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- 10. ERROR-BASED LESSONS (ISSUE 6)
-- ──────────────────────────────────────────────────────────
CREATE TABLE error_lessons (
    id                  UUID      PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID      NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    error_type          TEXT      NOT NULL,
    source_system       TEXT      NOT NULL,
    error_description   TEXT,
    generated_lesson    JSONB,
    resolved            BOOLEAN   DEFAULT FALSE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_error_lessons_user ON error_lessons(user_id);

-- ──────────────────────────────────────────────────────────
-- 11. SANDBOX SIMULATIONS (ISSUE 7)
-- ──────────────────────────────────────────────────────────
CREATE TABLE sandbox_simulations (
    id              UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    simulation_type TEXT    NOT NULL,
    scenario        TEXT,
    monolith        TEXT,
    score           FLOAT,
    outcome         TEXT,
    feedback        TEXT,
    payload         JSONB,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sandbox_user ON sandbox_simulations(user_id);

-- ──────────────────────────────────────────────────────────
-- 12. REPLAYS (ISSUE 8)
-- ──────────────────────────────────────────────────────────
CREATE TABLE replays (
    id              UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    replay_type     TEXT    NOT NULL,
    reference_id    TEXT    NOT NULL,
    source_system   TEXT,
    insights        JSONB,
    replayed_at     TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- 13. ONBOARDINGS (ISSUE 10)
-- ──────────────────────────────────────────────────────────
CREATE TABLE onboardings (
    id                  UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    role                TEXT    NOT NULL,
    contract_type       contract_type NOT NULL,
    mandatory_tracks    TEXT[]  NOT NULL DEFAULT '{}',
    completed_tracks    TEXT[]  NOT NULL DEFAULT '{}',
    training_status     TEXT    NOT NULL DEFAULT 'pending',
    started_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMP,
    UNIQUE (user_id)
);

-- ──────────────────────────────────────────────────────────
-- 14. LEGAL ACCEPTANCES (ISSUE 14)
-- ──────────────────────────────────────────────────────────
CREATE TABLE legal_acceptances (
    id              UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    course_id       UUID    NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    signature       TEXT    NOT NULL,
    accepted_at     TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, course_id)
);

-- ──────────────────────────────────────────────────────────
-- 15. ACADEMY EVENTS — audit log (ISSUES 20-21)
-- ──────────────────────────────────────────────────────────
CREATE TABLE academy_events (
    id          UUID                PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type  event_type_enum     NOT NULL,
    user_id     UUID                REFERENCES academy_users(id) ON DELETE SET NULL,
    payload     JSONB               NOT NULL DEFAULT '{}',
    published   BOOLEAN             NOT NULL DEFAULT FALSE, -- publicado no NATS
    created_at  TIMESTAMP           NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_academy_events_type    ON academy_events(event_type);
CREATE INDEX idx_academy_events_user    ON academy_events(user_id);
CREATE INDEX idx_academy_events_created ON academy_events(created_at DESC);

-- ──────────────────────────────────────────────────────────
-- 16. JOHN DNA FEED (ISSUE 28)
-- ──────────────────────────────────────────────────────────
CREATE TABLE john_dna_feed (
    id          UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    source      TEXT    NOT NULL,
    domain      TEXT    NOT NULL,
    knowledge   TEXT    NOT NULL,
    confidence  FLOAT   DEFAULT 0.8 CHECK (confidence >= 0 AND confidence <= 1),
    status      TEXT    NOT NULL DEFAULT 'absorbed',
    absorbed_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- 17. KANBAN TASK LEARNINGS (ISSUE 30)
-- ──────────────────────────────────────────────────────────
CREATE TABLE task_learnings (
    id                  UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id             TEXT    NOT NULL,
    user_id             UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    task_title          TEXT,
    task_domain         TEXT    NOT NULL,
    task_outcome        TEXT,
    generated_training  JSONB,
    recommendation      TEXT,
    processed_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- 18. SAAS OFFERS & MARKETPLACE (ISSUES 17-19)
-- ──────────────────────────────────────────────────────────
CREATE TABLE saas_offers (
    id              UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    title           TEXT    NOT NULL,
    domain          TEXT    NOT NULL,
    price           NUMERIC(10,2) NOT NULL DEFAULT 0,
    level           course_level DEFAULT 'intermediario',
    target_audience TEXT    DEFAULT 'mercado',
    cert_included   BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE whitelabels (
    id              UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id      TEXT    NOT NULL UNIQUE,
    company_name    TEXT    NOT NULL,
    tracks          TEXT[]  DEFAULT '{}',
    custom_branding JSONB   DEFAULT '{}',
    status          TEXT    NOT NULL DEFAULT 'active',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- CEFEIDA ANALYSES (ISSUES 22-23)
-- ──────────────────────────────────────────────────────────
CREATE TABLE cefeida_analyses (
    id                  UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    average_performance FLOAT,
    top_error_patterns  TEXT[]  DEFAULT '{}',
    recommendations     TEXT[]  DEFAULT '{}',
    adaptive_path       TEXT,
    study_behavior      JSONB   DEFAULT '{}',
    analyzed_at         TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE dynamic_contents (
    id              UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID    NOT NULL REFERENCES academy_users(id) ON DELETE CASCADE,
    domain          TEXT    NOT NULL,
    format          TEXT    NOT NULL DEFAULT 'microlearning',
    target_level    TEXT    NOT NULL DEFAULT 'intermediario',
    content         JSONB   NOT NULL DEFAULT '{}',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- HELPER: updated_at auto trigger
-- ──────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_academy_users_updated
    BEFORE UPDATE ON academy_users
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_cognitive_profiles_updated
    BEFORE UPDATE ON cognitive_profiles
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- ──────────────────────────────────────────────────────────
-- SEED: Trilha CORE LICEU (ISSUE 3)
-- ──────────────────────────────────────────────────────────
INSERT INTO tracks (name, monolith, description, is_mandatory, is_core_liceu)
VALUES
  ('CORE LICEU TRAINING', NULL, 'Trilha transversal obrigatoria para todos colaboradores', TRUE, TRUE),
  ('Archimedes Track', 'archimedes', 'Trilha completa para o ecossistema imobiliario', FALSE, FALSE),
  ('Game MKT Track', 'gameMkt', 'Trilha de marketing gamificado e digital', FALSE, FALSE),
  ('Juridico Track', 'juridico', 'Trilha juridica do ecossistema', FALSE, FALSE),
  ('Finance Track', 'cea', 'Trilha financeira e de investimentos', FALSE, FALSE),
  ('OPERA Track', 'opera', 'Trilha de operacoes e execucao', FALSE, FALSE),
  ('CEFEIDA Data Track', 'cefeida', 'Trilha de dados, IA e analise preditiva', FALSE, FALSE),
  ('John Copilot Track', 'john', 'Trilha de uso e co-pilotagem com o John', FALSE, FALSE);
