CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    type VARCHAR(100),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password_hash TEXT,
    role VARCHAR(100),
    age INTEGER,
    phone VARCHAR(50),
    avatar_url TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE learning_tracks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255),
    slug VARCHAR(255),
    domain VARCHAR(100),
    level VARCHAR(100),
    estimated_hours INTEGER,
    holographic_enabled BOOLEAN DEFAULT false,
    simulation_enabled BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    track_id UUID REFERENCES learning_tracks(id),
    title VARCHAR(255),
    description TEXT,
    thumbnail_url TEXT,
    difficulty VARCHAR(100),
    duration_minutes INTEGER,
    ai_generated BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(id),
    title VARCHAR(255),
    content JSONB,
    holographic_scene JSONB,
    simulation_payload JSONB,
    order_index INTEGER,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE enrollments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    progress NUMERIC(5,2),
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    started_at TIMESTAMP DEFAULT now(),
    completed BOOLEAN DEFAULT false
);

CREATE TABLE certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    certificate_hash TEXT,
    issued_at TIMESTAMP DEFAULT now()
);

CREATE TABLE simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255),
    simulation_type VARCHAR(100),
    payload JSONB,
    ai_analysis JSONB,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE holographic_rooms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_name VARCHAR(255),
    active BOOLEAN DEFAULT true,
    scene_config JSONB,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE marketplace_courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    specialist_id UUID REFERENCES users(id),
    course_id UUID REFERENCES courses(id),
    price NUMERIC(18,2),
    published BOOLEAN DEFAULT false
);

CREATE TABLE academy_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    amount NUMERIC(18,2),
    reason TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- WAVE 86: cadeia causal de memoria institucional da academia
CREATE TABLE IF NOT EXISTS academia_memory_chain (
    knowledge_record_id TEXT PRIMARY KEY,
    lesson_learned_id TEXT NOT NULL,
    planetary_operational_state_id TEXT NOT NULL,
    wave INTEGER NOT NULL,
    recorded_at DOUBLE PRECISION NOT NULL,
    event TEXT NOT NULL,
    cause TEXT NOT NULL,
    context TEXT NOT NULL,
    decision TEXT NOT NULL,
    execution TEXT NOT NULL,
    impact TEXT NOT NULL,
    risk TEXT NOT NULL,
    mitigation TEXT NOT NULL,
    result TEXT NOT NULL,
    lesson_learned TEXT NOT NULL,
    source_artifacts JSONB NOT NULL,
    evidence JSONB NOT NULL,
    graph_nodes JSONB NOT NULL,
    graph_edges JSONB NOT NULL,
    scientific_memory JSONB NOT NULL,
    usable_for_future_decision BOOLEAN NOT NULL DEFAULT true
);

CREATE INDEX IF NOT EXISTS idx_academia_memory_chain_state
    ON academia_memory_chain (planetary_operational_state_id);

CREATE INDEX IF NOT EXISTS idx_academia_memory_chain_lesson
    ON academia_memory_chain (lesson_learned_id);
