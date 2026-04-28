import { useEffect, useRef, useState, useCallback } from "react"

// ─── Config ──────────────────────────────────────────────────────────────────
const API_BASE = "/academy"
const WS_URL   = `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/events/ws`
const HEADERS  = { "Content-Type": "application/json", "x-holding-user-id": "HLD-002" }

const ACADEMY_EVENTS = new Set([
  "academy.enrolled",
  "academy.lesson.completed",
  "academy.certified",
  "academy.failed",
  "academy.john_recommended",
  "academy.compliance.accepted",
  "academy.onboarding.started",
  "academy.sandbox.executed",
  "academy.replay.created",
  "academy.task.learning_generated",
  "academy.course.completed",
])

function apiFetch(path, opts = {}) {
  return fetch(`${API_BASE}${path}`, { headers: HEADERS, ...opts }).then((r) => {
    if (!r.ok) throw new Error(r.status)
    return r.json()
  })
}

// ─── Primitives ──────────────────────────────────────────────────────────────
function Bar({ pct = 0, color = "#F5C542" }) {
  return (
    <div className="relative h-1.5 w-full rounded-full overflow-hidden" style={{ background: "#1e1e2e" }}>
      <div
        className="absolute left-0 top-0 h-full rounded-full transition-all duration-700"
        style={{ width: `${Math.min(Math.max(pct, 0), 100)}%`, background: color }}
      />
    </div>
  )
}

function Pill({ children, color = "#334155" }) {
  return (
    <span
      className="text-[10px] font-semibold px-1.5 py-0.5 rounded-full uppercase tracking-wider leading-none"
      style={{ background: color, color: "#fff" }}
    >
      {children}
    </span>
  )
}

function PanelBox({ title, icon, children, className = "", toolbar }) {
  return (
    <div
      className={`flex flex-col rounded-lg overflow-hidden ${className}`}
      style={{ background: "#111118", border: "1px solid #1e1e2e" }}
    >
      <div
        className="flex items-center justify-between px-3 py-2 shrink-0"
        style={{ borderBottom: "1px solid #1e1e2e", background: "#0d0d14" }}
      >
        <span className="text-xs font-bold tracking-widest uppercase text-gray-300 flex items-center gap-1">
          <span>{icon}</span> {title}
        </span>
        {toolbar}
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2 scrollbar-thin scrollbar-thumb-gray-700">
        {children}
      </div>
    </div>
  )
}

function Metric({ label, value, accent = "#22d3ee", sub }) {
  return (
    <div className="flex flex-col" style={{ background: "#0d0d14", border: "1px solid #1e1e2e", borderRadius: 6, padding: "8px 12px" }}>
      <span className="text-[10px] uppercase tracking-widest text-gray-500">{label}</span>
      <span className="text-2xl font-extrabold leading-tight" style={{ color: accent }}>{value ?? "—"}</span>
      {sub && <span className="text-[10px] text-gray-600 mt-0.5">{sub}</span>}
    </div>
  )
}

// ─── Top Bar ─────────────────────────────────────────────────────────────────
function TopBar({ kpis, wsState, onRefresh }) {
  const dot = wsState === "open" ? "#22c55e" : wsState === "connecting" ? "#eab308" : "#ef4444"
  return (
    <div
      className="col-span-12 flex items-center justify-between px-5 py-2 rounded-lg"
      style={{ background: "#0d0d14", border: "1px solid #1e1e2e" }}
    >
      {/* Brand */}
      <div className="flex items-center gap-3">
        <span className="text-xl">📚</span>
        <div>
          <p className="text-sm font-extrabold tracking-wider text-white leading-none">ACADEMIA DO SABER</p>
          <p className="text-[10px] text-gray-500 tracking-widest uppercase leading-none">LICEU Cognitive Training System</p>
        </div>
      </div>

      {/* Live KPIs */}
      <div className="flex items-center gap-6 text-xs">
        <span className="text-gray-400">
          Usuários: <strong className="text-white">{kpis?.total_enrollments ?? "—"}</strong>
        </span>
        <span className="text-gray-400">
          Conclusão: <strong className="text-[#22d3ee]">{kpis?.completion_rate != null ? `${Math.round(kpis.completion_rate * 10) / 10}%` : "—"}</strong>
        </span>
        <span className="text-gray-400">
          Cert.: <strong className="text-[#F5C542]">{kpis?.total_certifications ?? "—"}</strong>
        </span>
        <span className="text-gray-400">
          Impacto: <strong className="text-[#4ade80]">+23% revenue</strong>
        </span>
      </div>

      {/* Status */}
      <div className="flex items-center gap-3">
        <span className="text-[10px] text-gray-500">HLD-002 · academy_director</span>
        <button
          onClick={onRefresh}
          className="text-[10px] px-2 py-1 rounded transition"
          style={{ background: "#1e1e2e", color: "#94a3b8" }}
        >
          ↻ Sync
        </button>
        <span className="flex items-center gap-1 text-[10px]" style={{ color: dot }}>
          <span className="w-1.5 h-1.5 rounded-full inline-block" style={{ background: dot }} />
          {wsState === "open" ? "Live" : wsState === "connecting" ? "..." : "Offline"}
        </span>
      </div>
    </div>
  )
}

// ─── Courses + Tracks (centre-left) ──────────────────────────────────────────
function CourseList({ courses, progress }) {
  if (!courses.length)
    return <p className="text-xs text-gray-600">Nenhum curso cadastrado. <code className="text-[#4ade80]">POST /academy/courses</code></p>

  return courses.map((c) => {
    const pct = progress[c.id] || 0
    const color = pct >= 80 ? "#4ade80" : pct >= 40 ? "#F5C542" : "#f87171"
    return (
      <div key={c.id} style={{ background: "#0d0d14", borderRadius: 6, padding: "8px 10px" }}>
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium text-gray-200 truncate max-w-[70%]">{c.title}</span>
          <span className="text-xs font-bold" style={{ color }}>{pct}%</span>
        </div>
        <Bar pct={pct} color={color} />
        <div className="flex gap-1 mt-1.5">
          {c.level && <Pill color="#1e3a5f">{c.level}</Pill>}
          {c.monolith && <Pill color="#1e2a1e">{c.monolith}</Pill>}
        </div>
      </div>
    )
  })
}

function TrackList({ tracks }) {
  if (!tracks.length) return <p className="text-xs text-gray-600">Nenhuma trilha cadastrada.</p>
  return tracks.map((t) => (
    <div key={t.id} style={{ background: "#0d0d14", borderRadius: 6, padding: "8px 10px" }}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-gray-200">{t.name}</span>
        <div className="flex gap-1">
          {t.is_core_liceu && <Pill color="#78350f">CORE</Pill>}
          {t.is_mandatory && <Pill color="#7f1d1d">obrig.</Pill>}
        </div>
      </div>
      <p className="text-[10px] text-gray-500 mt-0.5">{t.monolith ? `Monólito: ${t.monolith}` : "Transversal"}</p>
    </div>
  ))
}

// ─── Ranking ─────────────────────────────────────────────────────────────────
function RankingRow({ item }) {
  const medals = ["#F5C542", "#94a3b8", "#cd7f32"]
  const medal = medals[item.position - 1]
  const levels = { Mestre: "#a78bfa", Especialista: "#22d3ee", Praticante: "#4ade80", Aprendiz: "#94a3b8" }
  const levelColor = levels[item.level] || "#94a3b8"
  return (
    <div className="flex items-center gap-2" style={{ background: "#0d0d14", borderRadius: 6, padding: "6px 10px" }}>
      <span className="w-5 text-center text-sm font-extrabold" style={{ color: medal || "#4b5563" }}>{item.position}</span>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium text-gray-200 truncate">{item.user_id}</p>
        <p className="text-[10px]" style={{ color: levelColor }}>{item.level}</p>
      </div>
      <div className="text-right">
        <p className="text-xs font-bold text-[#F5C542]">{item.xp} XP</p>
        <p className="text-[10px] text-gray-500">{item.certifications} cert.</p>
      </div>
    </div>
  )
}

// ─── John Panel ──────────────────────────────────────────────────────────────
function JohnPanel({ recommendations, liveJohn }) {
  const all = [...liveJohn.slice(0, 5), ...recommendations].slice(0, 10)

  if (!all.length)
    return <p className="text-xs text-gray-600">Aguardando recomendações do John…</p>

  return all.map((r, i) => {
    const confidence = r.confidence ?? r.score ?? null
    const isLive = i < liveJohn.length
    return (
      <div
        key={i}
        style={{
          background: isLive ? "#0c1a0c" : "#0d0d14",
          border: isLive ? "1px solid #166534" : "1px solid #1e1e2e",
          borderRadius: 6,
          padding: "8px 10px",
        }}
      >
        {isLive && <span className="text-[9px] text-[#4ade80] font-bold uppercase tracking-widest">● live</span>}
        <p className="text-xs text-gray-200 leading-snug">{r.message || r.title || r.next_step || JSON.stringify(r)}</p>
        {confidence != null && (
          <div className="mt-1.5">
            <Bar pct={confidence * 100} color="#4ade80" />
            <p className="text-[10px] text-gray-500 mt-0.5">Confiança: {(confidence * 100).toFixed(0)}%</p>
          </div>
        )}
      </div>
    )
  })
}

function JohnTrainWidget() {
  const [userId, setUserId] = useState("USR-001")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function run() {
    setLoading(true)
    try {
      const res = await apiFetch("/john/train", {
        method: "POST",
        body: JSON.stringify({ user_id: userId, current_scores: { bim: 45, juridico: 55 }, completed_courses: [] }),
      })
      setResult(res)
    } catch {
      setResult({ error: "API offline" })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-2">
      <input
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="w-full text-xs px-2 py-1.5 rounded"
        style={{ background: "#1e1e2e", color: "#e2e8f0", border: "1px solid #334155" }}
        placeholder="User ID"
      />
      <button
        onClick={run}
        disabled={loading}
        className="w-full text-xs py-1.5 rounded font-semibold transition disabled:opacity-40"
        style={{ background: "#166534", color: "#bbf7d0" }}
      >
        {loading ? "Analisando…" : "▶ Analisar com John"}
      </button>
      {result && !result.error && (
        <div className="text-[10px] space-y-1 mt-1">
          <p className="text-[#4ade80] font-semibold">Plano gerado</p>
          <p className="text-gray-400">Dificuldade: <span className="text-white">{result.recommended_difficulty}</span></p>
          {result.weak_areas?.length > 0 && (
            <p className="text-gray-400">Pontos fracos: <span className="text-red-300">{result.weak_areas.join(", ")}</span></p>
          )}
          {result.next_step && (
            <p className="text-gray-400">Próximo passo: <span className="text-[#F5C542]">{result.next_step}</span></p>
          )}
        </div>
      )}
    </div>
  )
}

// ─── Events Feed ─────────────────────────────────────────────────────────────
const EVENT_COLORS = {
  "academy.certified": "#4ade80",
  "academy.failed": "#f87171",
  "academy.enrolled": "#22d3ee",
  "academy.john_recommended": "#a78bfa",
  "academy.compliance.accepted": "#fb923c",
  "academy.sandbox.executed": "#F5C542",
  "academy.lesson.completed": "#38bdf8",
  "academy.task.learning_generated": "#f472b6",
}

function LiveFeed({ events }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [events.length])

  if (!events.length) return <p className="text-xs text-gray-600">Aguardando eventos…</p>

  return (
    <>
      {events.map((e, i) => {
        if (e.type === "ping") return null
        const color = EVENT_COLORS[e.type] || "#94a3b8"
        return (
          <div key={i} style={{ borderBottom: "1px solid #1e1e2e", paddingBottom: 6 }}>
            <div className="flex items-center gap-1.5 mb-0.5">
              <span className="w-1.5 h-1.5 rounded-full shrink-0" style={{ background: color }} />
              <span className="text-[10px] font-bold" style={{ color }}>{e.type}</span>
              <span className="text-[9px] text-gray-600 ml-auto shrink-0">{e.emitted_at?.slice(11, 19)}</span>
            </div>
            {e.payload && (
              <pre className="text-[9px] text-gray-500 leading-relaxed whitespace-pre-wrap break-all">
                {JSON.stringify(e.payload, null, 1)}
              </pre>
            )}
          </div>
        )
      })}
      <div ref={bottomRef} />
    </>
  )
}

// ─── Compliance ───────────────────────────────────────────────────────────────
function ComplianceList({ courses }) {
  if (!courses.length) return <p className="text-xs text-gray-600">Nenhum curso de compliance cadastrado.</p>
  return courses.map((c) => (
    <div key={c.id} className="flex items-center justify-between" style={{ background: "#0d0d14", borderRadius: 6, padding: "6px 10px" }}>
      <div className="flex items-center gap-2">
        <span className="text-red-400 text-xs">⚖</span>
        <span className="text-xs text-gray-200">{c.title}</span>
      </div>
      <div className="flex gap-1 shrink-0">
        {c.mandatory && <Pill color="#7f1d1d">obrig.</Pill>}
        <Pill color="#1e293b">{c.duration}</Pill>
      </div>
    </div>
  ))
}

// ─── Cognitive Heatmap ────────────────────────────────────────────────────────
function CognitiveHeatmap({ profile }) {
  if (!profile || !profile.skill_matrix) return <p className="text-xs text-gray-600">Perfil cognitivo não disponível.</p>
  const skills = Object.entries(profile.skill_matrix)
  return (
    <div className="grid grid-cols-3 gap-1.5">
      {skills.map(([skill, score]) => {
        const pct = Number(score) || 0
        const bg = pct >= 75 ? "#14532d" : pct >= 50 ? "#713f12" : "#450a0a"
        const fg = pct >= 75 ? "#4ade80" : pct >= 50 ? "#F5C542" : "#f87171"
        return (
          <div key={skill} style={{ background: bg, borderRadius: 5, padding: "6px 8px" }}>
            <p className="text-[9px] uppercase tracking-widest text-gray-400 truncate">{skill}</p>
            <p className="text-sm font-extrabold" style={{ color: fg }}>{pct}</p>
            <Bar pct={pct} color={fg} />
          </div>
        )
      })}
    </div>
  )
}

// ─── Main ─────────────────────────────────────────────────────────────────────
export default function AcademyDesk() {
  const [courses, setCourses]       = useState([])
  const [progress, setProgress]     = useState({})
  const [tracks, setTracks]         = useState([])
  const [ranking, setRanking]       = useState([])
  const [events, setEvents]         = useState([])
  const [liveJohn, setLiveJohn]     = useState([])
  const [recommendations, setRecs] = useState([])
  const [kpis, setKpis]             = useState(null)
  const [compliance, setCompliance] = useState([])
  const [cogProfile, setCogProfile] = useState(null)
  const [wsState, setWsState]       = useState("connecting")
  const [tab, setTab]               = useState("overview")
  const wsRef = useRef(null)

  // ── REST polling ──
  const loadAll = useCallback(async () => {
    try {
      const [dash, tracksData, rankData, evData, metData, legalData, cogData] = await Promise.allSettled([
        apiFetch("/dashboard"),
        apiFetch("/tracks"),
        apiFetch("/ranking/gamified"),
        apiFetch("/events"),
        apiFetch("/metrics/dashboard"),
        apiFetch("/legal/compliance-courses"),
        apiFetch("/users/USR-001/cognitive-score"),
      ])

      if (dash.status === "fulfilled") {
        setCourses(dash.value.courses || [])
        setProgress(dash.value.progress || {})
        setRecs(dash.value.recommendations || [])
      }
      if (tracksData.status === "fulfilled") setTracks(Array.isArray(tracksData.value) ? tracksData.value : [])
      if (rankData.status === "fulfilled")   setRanking(Array.isArray(rankData.value) ? rankData.value : [])
      if (evData.status === "fulfilled")     setEvents(Array.isArray(evData.value) ? evData.value.slice(-30) : [])
      if (metData.status === "fulfilled")    setKpis(metData.value?.kpis ?? null)
      if (legalData.status === "fulfilled")  setCompliance(Array.isArray(legalData.value) ? legalData.value : [])
      if (cogData.status === "fulfilled")    setCogProfile(cogData.value || null)
    } catch { /* silenciado */ }
  }, [])

  // ── WebSocket live feed ──
  useEffect(() => {
    function connect() {
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws
      setWsState("connecting")

      ws.onopen  = () => setWsState("open")
      ws.onclose = () => {
        setWsState("closed")
        // reconnect after 4s
        setTimeout(connect, 4000)
      }
      ws.onerror = () => ws.close()

      ws.onmessage = (msg) => {
        try {
          const ev = JSON.parse(msg.data)
          if (ev.type === "ping") return

          setEvents((prev) => [...prev.slice(-29), ev])

          if (ev.type === "academy.john_recommended") {
            const payload = ev.payload || {}
            setLiveJohn((prev) => [{
              message: payload.recommendation || payload.next_step || "Nova recomendação do John",
              confidence: payload.confidence ?? 0.85,
            }, ...prev.slice(0, 4)])
          }
        } catch { /* silenciado */ }
      }
    }
    connect()
    return () => wsRef.current?.close()
  }, [])

  // ── Boot + polling ──
  useEffect(() => {
    loadAll()
    const id = setInterval(loadAll, 30_000)
    return () => clearInterval(id)
  }, [loadAll])

  // ── Helpers ──
  const completionRate = kpis?.completion_rate ?? 0
  const completionColor = completionRate >= 70 ? "#4ade80" : completionRate >= 40 ? "#F5C542" : "#f87171"

  // ── Tabs para o painel central ──
  const TABS = [
    ["overview",  "◼ Overview"],
    ["courses",   "📖 Cursos"],
    ["tracks",    "🗺 Trilhas"],
    ["cognitive", "🧠 Cognitivo"],
    ["equipe",    "🔥 Equipe"],
    ["replay",    "🎬 Replay"],
    ["sandbox",   "⚡ Sandbox"],
    ["kanban",    "🔗 Kanban"],
    ["compliance","⚖ Compliance"],
  ]

  return (
    <div
      className="h-screen w-full grid overflow-hidden"
      style={{ background: "#0B0B0F", color: "#e2e8f0", fontFamily: "'Inter', system-ui, sans-serif",
        gridTemplateColumns: "1fr",
        gridTemplateRows: "48px 1fr 200px",
        gap: 6,
        padding: 6,
      }}
    >
      {/* ── ROW 1: Top Bar ── */}
      <TopBar kpis={kpis} wsState={wsState} onRefresh={loadAll} />

      {/* ── ROW 2: Main Grid ── */}
      <div
        className="w-full overflow-hidden"
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 2.5fr 1.8fr",
          gap: 6,
        }}
      >
        {/* COL A: KPIs + Ranking */}
        <div className="flex flex-col gap-2 overflow-hidden">
          {/* KPI strip */}
          <div className="grid grid-cols-2 gap-2 shrink-0">
            <Metric label="Matrículas"   value={kpis?.total_enrollments ?? "—"}    accent="#22d3ee" />
            <Metric label="Certificações" value={kpis?.total_certifications ?? "—"} accent="#4ade80" />
            <Metric label="Cursos"        value={kpis?.total_courses ?? "—"}        accent="#F5C542" />
            <Metric
              label="Conclusão"
              value={completionRate ? `${Math.round(completionRate * 10) / 10}%` : "—"}
              accent={completionColor}
            />
          </div>

          {/* Completion bar */}
          <div className="shrink-0 px-1">
            <div className="flex justify-between text-[10px] text-gray-500 mb-1">
              <span>Progresso geral</span>
              <span style={{ color: completionColor }}>{completionRate ? `${Math.round(completionRate * 10) / 10}%` : "—"}</span>
            </div>
            <Bar pct={completionRate} color={completionColor} />
          </div>

          {/* Ranking */}
          <PanelBox title="Ranking Global" icon="🏆" className="flex-1 min-h-0">
            {ranking.length
              ? ranking.slice(0, 12).map((r) => <RankingRow key={r.user_id} item={r} />)
              : <p className="text-xs text-gray-600">Nenhum dado de ranking.</p>
            }
          </PanelBox>
        </div>

        {/* COL B: Tabbed content (cursos / trilhas / cognitivo / compliance) */}
        <PanelBox
          title={tab.charAt(0).toUpperCase() + tab.slice(1)}
          icon="◼"
          className="flex-1 min-h-0"
          toolbar={
            <div className="flex gap-1">
              {TABS.map(([key, label]) => (
                <button
                  key={key}
                  onClick={() => setTab(key)}
                  className="text-[10px] px-2 py-0.5 rounded transition"
                  style={{
                    background: tab === key ? "#1e3a5f" : "#0d0d14",
                    color: tab === key ? "#7dd3fc" : "#64748b",
                    border: `1px solid ${tab === key ? "#1d4ed8" : "#1e1e2e"}`,
                  }}
                >
                  {label}
                </button>
              ))}
            </div>
          }
        >
          {tab === "overview" && (
            <div className="space-y-3">
              <p className="text-[11px] text-gray-400 leading-relaxed">
                Visão consolidada do Motor Educacional — Academia do Saber.
              </p>
              <div className="grid grid-cols-2 gap-2">
                <Metric label="Sandboxes"   value={kpis?.total_sandbox ?? "—"}     accent="#a78bfa" />
                <Metric label="Cursos ativos" value={kpis?.total_courses ?? "—"}   accent="#22d3ee" />
              </div>
              <div className="mt-2">
                <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-2">Trilhas ativas</p>
                <TrackList tracks={tracks.slice(0, 5)} />
              </div>
            </div>
          )}
          {tab === "courses"    && <CourseList courses={courses} progress={progress} />}
          {tab === "tracks"     && <TrackList tracks={tracks} />}
          {tab === "cognitive"  && <CognitiveHeatmap profile={cogProfile} />}
          {tab === "equipe"     && <TeamHeatmap />}
          {tab === "replay"     && <ReplayViewer />}
          {tab === "sandbox"    && <SandboxGame />}
          {tab === "kanban"     && <KanbanLearning />}
          {tab === "compliance" && <ComplianceList courses={compliance} />}
        </PanelBox>

        {/* COL C: John + Train Widget */}
        <div className="flex flex-col gap-2 overflow-hidden">
          <PanelBox title="John Recomenda" icon="🤖" className="flex-1 min-h-0">
            <JohnPanel recommendations={recommendations} liveJohn={liveJohn} />
          </PanelBox>

          <PanelBox title="Treinar com John" icon="⚡" className="shrink-0">
            <JohnTrainWidget />
          </PanelBox>
        </div>
      </div>

      {/* ── ROW 3: Live Event Feed ── */}
      <PanelBox
        title="Eventos em Tempo Real"
        icon="📡"
        className="overflow-hidden"
        toolbar={
          <div className="flex items-center gap-2">
            <span className="text-[10px] text-gray-500">{events.filter((e) => e.type !== "ping").length} eventos</span>
            <span
              className="text-[10px] font-bold px-2 py-0.5 rounded-full"
              style={{ background: wsState === "open" ? "#14532d" : "#7f1d1d", color: wsState === "open" ? "#4ade80" : "#f87171" }}
            >
              {wsState === "open" ? "● WS Connected" : wsState === "connecting" ? "● Connecting…" : "● Disconnected"}
            </span>
          </div>
        }
      >
        {/* horizontal scroll for the feed */}
        <div
          className="flex gap-3 overflow-x-auto pb-1"
          style={{ flexDirection: "row", alignItems: "flex-start" }}
        >
          {events.filter((e) => e.type !== "ping").slice(-20).reverse().map((e, i) => {
            const color = EVENT_COLORS[e.type] || "#94a3b8"
            return (
              <div
                key={i}
                className="shrink-0"
                style={{
                  width: 200,
                  background: "#0d0d14",
                  border: `1px solid ${color}33`,
                  borderTop: `2px solid ${color}`,
                  borderRadius: 6,
                  padding: "6px 8px",
                }}
              >
                <p className="text-[10px] font-bold truncate" style={{ color }}>{e.type}</p>
                <p className="text-[9px] text-gray-600 mb-1">{e.emitted_at?.slice(11, 19)}</p>
                {e.payload && (
                  <pre className="text-[9px] text-gray-500 whitespace-pre-wrap break-all leading-relaxed">
                    {JSON.stringify(e.payload, null, 1).slice(0, 120)}
                  </pre>
                )}
              </div>
            )
          })}
          {!events.filter((e) => e.type !== "ping").length && (
            <p className="text-xs text-gray-600">Aguardando eventos WebSocket…</p>
          )}
        </div>
      </PanelBox>
    </div>
  )
}


// ╔══════════════════════════════════════════════════════════════════╗
// ║  EXTENSÕES — PRÓXIMO NÍVEL                                       ║
// ╚══════════════════════════════════════════════════════════════════╝

// ─── 1. Team Cognitive Heatmap ────────────────────────────────────────────────
function TeamHeatmap() {
  const TEAM = ["USR-001", "USR-002", "USR-003", "USR-004", "USR-005"]
  const [profiles, setProfiles] = useState({})
  const [loading, setLoading]   = useState(false)

  async function load() {
    setLoading(true)
    const results = await Promise.allSettled(
      TEAM.map((uid) =>
        apiFetch("/cefeida/analyze", {
          method: "POST",
          body: JSON.stringify({ user_id: uid, context: "team_heatmap" }),
        }).then((r) => ({ uid, matrix: r.skill_profile?.skill_matrix || {} }))
      )
    )
    const map = {}
    results.forEach((r) => { if (r.status === "fulfilled") map[r.value.uid] = r.value.matrix })
    setProfiles(map)
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  const allSkills = [...new Set(Object.values(profiles).flatMap(Object.keys))]

  if (loading) return <p className="text-xs text-gray-500">Carregando heatmap de equipe…</p>
  if (!allSkills.length) return (
    <div className="text-center text-gray-600 text-xs py-4">
      <p>Heatmap cognitivo por equipe</p>
      <p className="mt-1 text-[10px]">Conecte a API CEFEIDA para visualizar</p>
      <button onClick={load} className="mt-2 text-[10px] bg-purple-900 text-purple-300 px-3 py-1 rounded hover:bg-purple-800 transition">↺ Tentar novamente</button>
    </div>
  )

  const USERS = Object.keys(profiles)
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-[10px] border-collapse">
        <thead>
          <tr>
            <th className="text-left text-gray-500 pb-2 pr-3 font-normal uppercase tracking-widest">Usuário</th>
            {allSkills.map((s) => (
              <th key={s} className="text-gray-500 pb-2 px-1 font-normal uppercase tracking-widest whitespace-nowrap">
                {s.replace(/_/g, " ")}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {USERS.map((uid) => (
            <tr key={uid} className="border-t border-gray-800">
              <td className="py-1.5 pr-3 text-gray-400 font-medium">{uid}</td>
              {allSkills.map((skill) => {
                const pct = Number(profiles[uid]?.[skill]) || 0
                const bg = pct >= 75 ? "#14532d" : pct >= 50 ? "#713f12" : pct > 0 ? "#450a0a" : "#0d0d14"
                const fg = pct >= 75 ? "#4ade80" : pct >= 50 ? "#F5C542" : pct > 0 ? "#f87171" : "#374151"
                return (
                  <td key={skill} className="px-1 py-1.5 text-center">
                    <div style={{ background: bg, borderRadius: 4, padding: "3px 6px" }}>
                      <span style={{ color: fg, fontWeight: 700 }}>{pct || "—"}</span>
                    </div>
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={load} className="mt-3 text-[10px] bg-purple-900 text-purple-300 px-3 py-1 rounded hover:bg-purple-800 transition">↺ Atualizar</button>
    </div>
  )
}

// ─── 2. Replay Visual (Netflix-style) ────────────────────────────────────────
const REPLAY_TYPES = ["negociacao", "objecao", "fechamento", "prospeccao"]

function ReplayViewer() {
  const [replays, setReplays]     = useState([])
  const [active, setActive]       = useState(null)
  const [creating, setCreating]   = useState(false)
  const [form, setForm]           = useState({ reference_id: "NEG-001", replay_type: "negociacao" })

  useEffect(() => {
    apiFetch("/events?type=academy.replay.created")
      .then((ev) => setReplays(Array.isArray(ev) ? ev.slice(0, 12) : []))
      .catch(() => setReplays([]))
  }, [])

  async function createReplay() {
    setCreating(true)
    try {
      const res = await apiFetch("/replay", {
        method: "POST",
        body: JSON.stringify({ ...form, notes: "Revisão automática via UI" }),
      })
      setReplays((p) => [{ type: "academy.replay.created", payload: res, emitted_at: new Date().toISOString() }, ...p])
      setActive(res)
    } finally { setCreating(false) }
  }

  return (
    <div className="space-y-3">
      {/* Criar replay */}
      <div className="flex gap-2 items-end">
        <div className="flex-1">
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Referência</p>
          <input
            value={form.reference_id}
            onChange={(e) => setForm((f) => ({ ...f, reference_id: e.target.value }))}
            className="w-full bg-[#0d0d14] border border-[#1e1e2e] text-white text-xs px-2 py-1.5 rounded focus:outline-none focus:border-cyan-700"
            placeholder="ID da negociação"
          />
        </div>
        <div>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Tipo</p>
          <select
            value={form.replay_type}
            onChange={(e) => setForm((f) => ({ ...f, replay_type: e.target.value }))}
            className="bg-[#0d0d14] border border-[#1e1e2e] text-white text-xs px-2 py-1.5 rounded focus:outline-none"
          >
            {REPLAY_TYPES.map((t) => <option key={t}>{t}</option>)}
          </select>
        </div>
        <button
          onClick={createReplay}
          disabled={creating}
          className="text-xs bg-cyan-900 hover:bg-cyan-800 disabled:opacity-50 text-cyan-300 px-3 py-1.5 rounded transition"
        >
          {creating ? "…" : "▶ Criar Replay"}
        </button>
      </div>

      {/* Replay ativo */}
      {active && (
        <div style={{ background: "#0d0d14", border: "1px solid #164e63", borderRadius: 8, padding: "10px 14px" }}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-cyan-300">▶ REPLAY ATIVO</span>
            <button onClick={() => setActive(null)} className="text-[10px] text-gray-600 hover:text-gray-400">✕</button>
          </div>
          <p className="text-[11px] text-white font-semibold">{active.reference_id} — {active.replay_type}</p>
          {active.insights?.length > 0 && (
            <ul className="mt-2 space-y-1">
              {active.insights.map((ins, i) => (
                <li key={i} className="text-[10px] text-gray-400 flex gap-1.5">
                  <span className="text-cyan-500 shrink-0">›</span>{ins}
                </li>
              ))}
            </ul>
          )}
          <div className="mt-3 h-1.5 rounded-full overflow-hidden" style={{ background: "#1e293b" }}>
            <div className="h-full bg-cyan-500 animate-pulse" style={{ width: "60%" }} />
          </div>
          <p className="text-[10px] text-gray-600 mt-1">Reproduzindo análise…</p>
        </div>
      )}

      {/* Grid de replays */}
      <div className="grid grid-cols-2 gap-2">
        {replays.map((ev, i) => {
          const p = ev.payload || {}
          return (
            <button
              key={i}
              onClick={() => setActive(p)}
              className="text-left rounded overflow-hidden transition hover:ring-1 hover:ring-cyan-700"
              style={{ background: "#0d0d14", border: "1px solid #1e1e2e" }}
            >
              <div style={{ background: "#0e3a4a", padding: "20px 8px", textAlign: "center", fontSize: 22 }}>🎬</div>
              <div className="p-2">
                <p className="text-[10px] font-bold text-white truncate">{p.reference_id || `Replay #${i + 1}`}</p>
                <p className="text-[10px] text-gray-600">{p.replay_type || "—"}</p>
                <p className="text-[9px] text-gray-700 mt-0.5">{ev.emitted_at?.slice(0, 10)}</p>
              </div>
            </button>
          )
        })}
        {!replays.length && (
          <p className="col-span-2 text-xs text-gray-600 py-4 text-center">Nenhum replay gerado ainda.</p>
        )}
      </div>
    </div>
  )
}

// ─── 3. Sandbox Game (decisão → consequência) ─────────────────────────────────
const SCENARIOS = [
  { id: "S1", label: "Negociação BIM — Desconto agressivo", skill: "negociacao", difficulty: "hard" },
  { id: "S2", label: "Objeção jurídica — Contrato SaaS",   skill: "juridico",   difficulty: "medium" },
  { id: "S3", label: "Prospecção fria — Industria 4.0",    skill: "prospeccao", difficulty: "easy" },
  { id: "S4", label: "Fechamento premium — C-Level",       skill: "fechamento", difficulty: "hard" },
]
const DIFF_COLOR = { easy: "#166534", medium: "#713f12", hard: "#7f1d1d" }
const DIFF_TEXT  = { easy: "#4ade80",  medium: "#F5C542",  hard: "#f87171"  }

function SandboxGame() {
  const [scenario, setScenario] = useState(SCENARIOS[0])
  const [userId, setUserId]     = useState("USR-001")
  const [result, setResult]     = useState(null)
  const [running, setRunning]   = useState(false)
  const [history, setHistory]   = useState([])

  async function simulate() {
    setRunning(true)
    setResult(null)
    try {
      const res = await apiFetch("/sandbox/simulate", {
        method: "POST",
        body: JSON.stringify({
          user_id: userId,
          scenario_id: scenario.id,
          skill_focus: scenario.skill,
          difficulty: scenario.difficulty,
        }),
      })
      setResult(res)
      setHistory((h) => [{ scenario: scenario.label, outcome: res.outcome, score: res.score }, ...h.slice(0, 4)])
    } finally { setRunning(false) }
  }

  return (
    <div className="space-y-3">
      {/* Seletor de cenário */}
      <div className="grid grid-cols-2 gap-2">
        {SCENARIOS.map((sc) => (
          <button
            key={sc.id}
            onClick={() => { setScenario(sc); setResult(null) }}
            className="text-left p-2 rounded transition"
            style={{
              background: scenario.id === sc.id ? "#1a1440" : "#0d0d14",
              border: `1px solid ${scenario.id === sc.id ? "#6d28d9" : "#1e1e2e"}`,
            }}
          >
            <p className="text-[10px] font-semibold text-white leading-tight">{sc.label}</p>
            <span
              className="text-[9px] font-bold px-1.5 py-0.5 rounded-full mt-1 inline-block"
              style={{ background: DIFF_COLOR[sc.difficulty], color: DIFF_TEXT[sc.difficulty] }}
            >
              {sc.difficulty}
            </span>
          </button>
        ))}
      </div>

      {/* Controles */}
      <div className="flex gap-2 items-center">
        <input
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="flex-1 bg-[#0d0d14] border border-[#1e1e2e] text-white text-xs px-2 py-1.5 rounded focus:outline-none focus:border-purple-700"
          placeholder="User ID"
        />
        <button
          onClick={simulate}
          disabled={running}
          className="text-xs bg-purple-900 hover:bg-purple-800 disabled:opacity-50 text-purple-200 px-4 py-1.5 rounded transition font-bold"
        >
          {running ? "⚡ Simulando…" : "▶ Simular"}
        </button>
      </div>

      {/* Resultado */}
      {result && (
        <div
          style={{
            background: "#0d0d14",
            border: `1px solid ${result.outcome === "success" ? "#166534" : result.outcome === "partial" ? "#713f12" : "#7f1d1d"}`,
            borderRadius: 8,
            padding: "12px 14px",
          }}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-extrabold" style={{ color: result.outcome === "success" ? "#4ade80" : result.outcome === "partial" ? "#F5C542" : "#f87171" }}>
              {result.outcome === "success" ? "✓ SUCESSO" : result.outcome === "partial" ? "◑ PARCIAL" : "✗ FALHOU"}
            </span>
            <span className="text-xs text-gray-400">Score: <b className="text-white">{result.score ?? "—"}</b></span>
          </div>
          {result.feedback && <p className="text-[11px] text-gray-300 leading-relaxed">{result.feedback}</p>}
          {result.next_recommended_course && (
            <p className="mt-2 text-[10px] text-purple-400">
              📚 Recomendado: <span className="text-white">{result.next_recommended_course}</span>
            </p>
          )}
        </div>
      )}

      {/* Histórico */}
      {history.length > 0 && (
        <div>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1.5">Histórico de simulações</p>
          <div className="space-y-1">
            {history.map((h, i) => (
              <div key={i} className="flex justify-between text-[10px] py-1 border-b border-gray-800">
                <span className="text-gray-400 truncate max-w-[60%]">{h.scenario}</span>
                <span style={{ color: h.outcome === "success" ? "#4ade80" : h.outcome === "partial" ? "#F5C542" : "#f87171" }}>
                  {h.outcome} {h.score != null ? `· ${h.score}pts` : ""}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// ─── 4. Kanban → Treinamento Automático ──────────────────────────────────────
function KanbanLearning() {
  const [taskId, setTaskId]         = useState("TASK-001")
  const [taskTitle, setTaskTitle]   = useState("Implementar módulo de negociação B2B")
  const [result, setResult]         = useState(null)
  const [loading, setLoading]       = useState(false)
  const [history, setHistory]       = useState([])

  async function generate() {
    setLoading(true)
    setResult(null)
    try {
      const res = await apiFetch("/kanban/task-learning", {
        method: "POST",
        body: JSON.stringify({ task_id: taskId, title: taskTitle, tags: ["negociacao", "b2b"] }),
      })
      setResult(res)
      setHistory((h) => [{ task_id: taskId, title: taskTitle, courses: res.generated_courses?.length ?? 0 }, ...h.slice(0, 4)])
    } finally { setLoading(false) }
  }

  return (
    <div className="space-y-3">
      <div className="space-y-2">
        <div>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Task ID</p>
          <input
            value={taskId}
            onChange={(e) => setTaskId(e.target.value)}
            className="w-full bg-[#0d0d14] border border-[#1e1e2e] text-white text-xs px-2 py-1.5 rounded focus:outline-none focus:border-yellow-700"
            placeholder="ID da task no Kanban"
          />
        </div>
        <div>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1">Descrição da Task</p>
          <input
            value={taskTitle}
            onChange={(e) => setTaskTitle(e.target.value)}
            className="w-full bg-[#0d0d14] border border-[#1e1e2e] text-white text-xs px-2 py-1.5 rounded focus:outline-none focus:border-yellow-700"
            placeholder="O que a task envolve?"
          />
        </div>
        <button
          onClick={generate}
          disabled={loading}
          className="w-full text-xs bg-yellow-900 hover:bg-yellow-800 disabled:opacity-50 text-yellow-200 py-1.5 rounded transition font-bold"
        >
          {loading ? "⚡ Gerando treinamentos…" : "🔗 Conectar Task → Treinamento"}
        </button>
      </div>

      {/* Resultado */}
      {result && (
        <div style={{ background: "#0d0d14", border: "1px solid #713f12", borderRadius: 8, padding: "12px 14px" }}>
          <p className="text-xs font-bold text-yellow-400 mb-2">
            ✓ {result.generated_courses?.length ?? 0} treinamento(s) gerado(s)
          </p>
          {result.generated_courses?.map((c, i) => (
            <div key={i} className="flex justify-between text-[10px] py-1 border-b border-gray-800">
              <span className="text-gray-300 truncate max-w-[70%]">{c.title || c}</span>
              <Pill color="#451a03">{c.level || "obrigatório"}</Pill>
            </div>
          ))}
          {result.rationale && (
            <p className="mt-3 text-[10px] text-gray-500 leading-relaxed">{result.rationale}</p>
          )}
        </div>
      )}

      {/* Histórico de tasks */}
      {history.length > 0 && (
        <div>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mb-1.5">Tasks processadas</p>
          <div className="space-y-1">
            {history.map((h, i) => (
              <div key={i} className="flex justify-between text-[10px] py-1 border-b border-gray-800">
                <span className="text-gray-400 truncate max-w-[70%]">{h.task_id} — {h.title}</span>
                <span className="text-yellow-500">{h.courses} cursos</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
