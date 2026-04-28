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
    ["overview", "◼ Overview"],
    ["courses",  "📖 Cursos"],
    ["tracks",   "🗺 Trilhas"],
    ["cognitive","🧠 Cognitivo"],
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
          {tab === "courses"   && <CourseList courses={courses} progress={progress} />}
          {tab === "tracks"    && <TrackList tracks={tracks} />}
          {tab === "cognitive" && <CognitiveHeatmap profile={cogProfile} />}
          {tab === "compliance"&& <ComplianceList courses={compliance} />}
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


const API_BASE = '/academy'
const HOLDING_HEADER = { 'x-holding-user-id': 'HLD-002', 'Content-Type': 'application/json' }

// ─── Helpers ────────────────────────────────────────────────────────────────
function apiFetch(path, opts = {}) {
  return fetch(`${API_BASE}${path}`, { headers: HOLDING_HEADER, ...opts }).then((r) => r.json())
}

// ─── Sub-components ─────────────────────────────────────────────────────────

function StatCard({ label, value, accent = 'green' }) {
  const colors = { green: 'border-green-500 text-green-400', blue: 'border-blue-500 text-blue-400', yellow: 'border-yellow-500 text-yellow-400', red: 'border-red-500 text-red-400' }
  return (
    <div className={`bg-gray-900 border-l-4 ${colors[accent]} p-4 rounded`}>
      <p className="text-xs text-gray-400 uppercase tracking-widest mb-1">{label}</p>
      <p className="text-3xl font-bold">{value ?? '—'}</p>
    </div>
  )
}

function ProgressBar({ pct = 0, color = 'bg-green-500' }) {
  return (
    <div className="h-2 w-full bg-gray-700 rounded overflow-hidden mt-2">
      <div className={`${color} h-2 transition-all duration-500`} style={{ width: `${Math.min(pct, 100)}%` }} />
    </div>
  )
}

function Badge({ text, color = 'gray' }) {
  const map = { gray: 'bg-gray-700 text-gray-300', green: 'bg-green-900 text-green-300', red: 'bg-red-900 text-red-300', blue: 'bg-blue-900 text-blue-300', yellow: 'bg-yellow-900 text-yellow-300' }
  return <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${map[color]}`}>{text}</span>
}

function SectionTitle({ children }) {
  return <h2 className="text-lg font-semibold text-gray-100 mb-3 border-b border-gray-700 pb-1">{children}</h2>
}

// ─── Panel: Courses ──────────────────────────────────────────────────────────
function PanelCourses({ courses, progress }) {
  if (!courses.length) return <p className="text-gray-500 text-sm">Nenhum curso cadastrado.</p>
  return (
    <ul className="space-y-3">
      {courses.map((c) => (
        <li key={c.id} className="bg-gray-800 p-3 rounded hover:bg-gray-750 transition">
          <div className="flex items-center justify-between">
            <span className="font-medium text-sm">{c.title}</span>
            <div className="flex gap-2 items-center">
              <Badge text={c.level || 'basico'} color="blue" />
              {c.monolith && <Badge text={c.monolith} color="gray" />}
            </div>
          </div>
          <ProgressBar pct={progress[c.id] || 0} />
          <p className="text-xs text-gray-500 mt-1">{progress[c.id] || 0}% concluído</p>
        </li>
      ))}
    </ul>
  )
}

// ─── Panel: Tracks ───────────────────────────────────────────────────────────
function PanelTracks({ tracks }) {
  return (
    <ul className="space-y-2">
      {tracks.map((t) => (
        <li key={t.id} className="bg-gray-800 p-3 rounded">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold">{t.name}</span>
            <div className="flex gap-1">
              {t.is_core_liceu && <Badge text="CORE" color="yellow" />}
              {t.is_mandatory && <Badge text="obrigatório" color="red" />}
            </div>
          </div>
          <p className="text-xs text-gray-400 mt-1">{t.monolith ? `Monólito: ${t.monolith}` : 'Trilha transversal'}</p>
          {t.modules && <p className="text-xs text-gray-500 mt-0.5">{t.modules.length} módulos</p>}
        </li>
      ))}
    </ul>
  )
}

// ─── Panel: John Recomenda ───────────────────────────────────────────────────
function PanelJohn({ recommendations }) {
  return (
    <ul className="space-y-2">
      {recommendations.map((r) => (
        <li key={r.id} className="flex items-start gap-2">
          <span className="mt-0.5 text-green-400">▶</span>
          <span className="text-sm text-gray-200">{r.title}</span>
        </li>
      ))}
    </ul>
  )
}

// ─── Panel: Ranking ──────────────────────────────────────────────────────────
function PanelRanking({ ranking }) {
  const medalColors = ['text-yellow-400', 'text-gray-300', 'text-amber-600']
  if (!ranking.length) return <p className="text-gray-500 text-sm">Nenhum dado de ranking ainda.</p>
  return (
    <ol className="space-y-2">
      {ranking.map((r) => (
        <li key={r.user_id} className="flex items-center justify-between bg-gray-800 px-3 py-2 rounded">
          <div className="flex items-center gap-2">
            <span className={`font-bold text-lg w-6 ${medalColors[r.position - 1] || 'text-gray-400'}`}>{r.position}</span>
            <div>
              <p className="text-sm font-medium">{r.user_id}</p>
              <p className="text-xs text-gray-400">{r.level}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-green-400 font-bold text-sm">{r.xp} XP</p>
            <p className="text-xs text-gray-400">{r.certifications} cert.</p>
          </div>
        </li>
      ))}
    </ol>
  )
}

// ─── Panel: Eventos ──────────────────────────────────────────────────────────
function PanelEvents({ events }) {
  if (!events.length) return <p className="text-gray-500 text-sm">Nenhum evento registrado.</p>
  return (
    <ul className="space-y-2 max-h-48 overflow-y-auto">
      {[...events].reverse().map((e, i) => (
        <li key={i} className="flex items-start gap-2 text-xs text-gray-300">
          <span className="text-blue-400 shrink-0">{e.type || e.event_type}</span>
          <span className="text-gray-500">{e.emitted_at || e.created_at}</span>
        </li>
      ))}
    </ul>
  )
}

// ─── Panel: Compliance ───────────────────────────────────────────────────────
function PanelCompliance({ courses: complianceCourses }) {
  return (
    <ul className="space-y-2">
      {complianceCourses.map((c) => (
        <li key={c.id} className="flex items-center gap-2 text-sm">
          <span className="text-red-400">⚖</span>
          <span>{c.title}</span>
          <Badge text={c.duration} color="gray" />
        </li>
      ))}
    </ul>
  )
}

// ─── Panel: KPI Cards ────────────────────────────────────────────────────────
function PanelKPIs({ kpis }) {
  if (!kpis) return null
  return (
    <div className="grid grid-cols-2 gap-3">
      <StatCard label="Matrículas" value={kpis.total_enrollments ?? kpis.totalEnrollments} accent="blue" />
      <StatCard label="Certificações" value={kpis.completed_certifications ?? kpis.completedCertifications} accent="green" />
      <StatCard label="Cursos" value={kpis.total_courses ?? kpis.totalCourses} accent="yellow" />
      <StatCard label="Sandboxes" value={kpis.total_sandbox ?? kpis.totalSandboxSimulations} accent="red" />
    </div>
  )
}

// ─── Main AcademyDesk ────────────────────────────────────────────────────────
export default function AcademyDesk() {
  const [tab, setTab] = useState('cursos')
  const [courses, setCourses] = useState([])
  const [progress, setProgress] = useState({})
  const [recommendations, setRecommendations] = useState([])
  const [tracks, setTracks] = useState([])
  const [ranking, setRanking] = useState([])
  const [events, setEvents] = useState([])
  const [kpis, setKpis] = useState(null)
  const [complianceCourses, setComplianceCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [metrics, setMetrics] = useState(null)

  const loadAll = useCallback(async () => {
    setLoading(true)
    try {
      const [dash, tracksData, rankingData, eventsData, metricsData, legalData] = await Promise.all([
        apiFetch('/dashboard'),
        apiFetch('/tracks'),
        apiFetch('/ranking/gamified'),
        apiFetch('/events'),
        apiFetch('/metrics/dashboard'),
        apiFetch('/legal/compliance-courses'),
      ])

      setCourses(Array.isArray(dash.courses) ? dash.courses : [])
      setProgress(dash.progress || {})
      setRecommendations(Array.isArray(dash.recommendations) ? dash.recommendations : [])
      setTracks(Array.isArray(tracksData) ? tracksData : [])
      setRanking(Array.isArray(rankingData) ? rankingData : [])
      setEvents(Array.isArray(eventsData) ? eventsData : [])
      setKpis(metricsData?.kpis || null)
      setMetrics(metricsData)
      setComplianceCourses(Array.isArray(legalData) ? legalData : [])
    } catch {
      // API offline — show empty state
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadAll()
    const interval = setInterval(loadAll, 30_000)
    return () => clearInterval(interval)
  }, [loadAll])

  const TABS = ['cursos', 'trilhas', 'ranking', 'compliance', 'eventos', 'métricas']

  return (
    <div className="min-h-screen bg-black text-white font-sans">
      {/* ── Header ── */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-gray-800 bg-gray-950">
        <div className="flex items-center gap-3">
          <span className="text-2xl">📚</span>
          <div>
            <h1 className="text-xl font-bold tracking-wide">Academia do Saber</h1>
            <p className="text-xs text-gray-400">LICEU Ecossistema — Motor Educacional</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-xs text-gray-500">HLD-002 — academy_director</span>
          <button onClick={loadAll} className="text-xs bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded transition">
            ↻ Atualizar
          </button>
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" title="Online" />
        </div>
      </header>

      <div className="grid grid-cols-12 gap-0 min-h-[calc(100vh-65px)]">
        {/* ── Sidebar ── */}
        <nav className="col-span-1 border-r border-gray-800 bg-gray-950 flex flex-col items-center py-6 gap-6">
          {[
            ['cursos', '📖'],
            ['trilhas', '🗺️'],
            ['ranking', '🏆'],
            ['compliance', '⚖️'],
            ['eventos', '📡'],
            ['métricas', '📊'],
          ].map(([key, icon]) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              title={key}
              className={`text-2xl p-2 rounded-lg transition ${tab === key ? 'bg-gray-800 ring-1 ring-green-500' : 'hover:bg-gray-800'}`}
            >
              {icon}
            </button>
          ))}
        </nav>

        {/* ── Main Content ── */}
        <main className="col-span-8 p-6 overflow-y-auto">
          {loading && <div className="flex items-center justify-center h-40 text-gray-500">Carregando...</div>}

          {!loading && tab === 'cursos' && (
            <>
              <SectionTitle>Cursos — Domínio Educacional</SectionTitle>
              <PanelCourses courses={courses} progress={progress} />
              {!courses.length && (
                <div className="mt-6 bg-gray-900 rounded p-4 text-gray-400 text-sm">
                  <p>Nenhum curso cadastrado ainda.</p>
                  <p className="mt-1">Use <code className="text-green-400">POST /academy/courses</code> para começar.</p>
                </div>
              )}
            </>
          )}

          {!loading && tab === 'trilhas' && (
            <>
              <SectionTitle>Trilhas por Monólito</SectionTitle>
              <PanelTracks tracks={tracks} />
            </>
          )}

          {!loading && tab === 'ranking' && (
            <>
              <SectionTitle>Ranking Gamificado — XP & Nível</SectionTitle>
              <PanelRanking ranking={ranking.slice(0, 15)} />
            </>
          )}

          {!loading && tab === 'compliance' && (
            <>
              <SectionTitle>Compliance Jurídico Obrigatório</SectionTitle>
              <PanelCompliance courses={complianceCourses} />
            </>
          )}

          {!loading && tab === 'eventos' && (
            <>
              <SectionTitle>Eventos NATS (academy.*)</SectionTitle>
              <PanelEvents events={events} />
            </>
          )}

          {!loading && tab === 'métricas' && (
            <>
              <SectionTitle>KPIs Educacionais</SectionTitle>
              <PanelKPIs kpis={kpis} />
              {metrics?.track_completion?.length > 0 && (
                <div className="mt-6">
                  <SectionTitle>Conclusão por Trilha</SectionTitle>
                  <ul className="space-y-3">
                    {metrics.track_completion.map((tc) => {
                      const pct = tc.enrolled > 0 ? Math.round((tc.completed / tc.enrolled) * 100) : 0
                      return (
                        <li key={tc.track} className="bg-gray-900 p-3 rounded">
                          <div className="flex justify-between text-sm mb-1">
                            <span>{tc.track}</span>
                            <span className="text-gray-400">{tc.completed}/{tc.enrolled} — {pct}%</span>
                          </div>
                          <ProgressBar pct={pct} color={pct >= 80 ? 'bg-green-500' : pct >= 50 ? 'bg-yellow-500' : 'bg-red-500'} />
                        </li>
                      )
                    })}
                  </ul>
                </div>
              )}
            </>
          )}
        </main>

        {/* ── Right Panel: John + Alertas ── */}
        <aside className="col-span-3 border-l border-gray-800 bg-gray-950 p-5 flex flex-col gap-6 overflow-y-auto">
          {/* John AI */}
          <div>
            <SectionTitle>🤖 John Recomenda</SectionTitle>
            <PanelJohn recommendations={recommendations} />
            <div className="mt-4 bg-gray-800 rounded p-3">
              <p className="text-xs text-gray-400 mb-2">Treinar com John</p>
              <JohnTrainWidget />
            </div>
          </div>

          {/* Alertas de atraso */}
          <div>
            <SectionTitle>⚠️ Alertas</SectionTitle>
            <LateAlertsWidget />
          </div>

          {/* Eventos recentes */}
          <div>
            <SectionTitle>📡 Eventos Recentes</SectionTitle>
            <PanelEvents events={events.slice(-6)} />
          </div>
        </aside>
      </div>
    </div>
  )
}

// ─── Widget: John Quick Train ────────────────────────────────────────────────
function JohnTrainWidget() {
  const [userId, setUserId] = useState('USR-001')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleTrain() {
    setLoading(true)
    try {
      const res = await apiFetch('/john/train', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, current_scores: { bim: 45, juridico: 55 }, completed_courses: [] }),
      })
      setResult(res)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-2">
      <input
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="w-full bg-gray-700 text-white text-xs px-2 py-1.5 rounded border border-gray-600 focus:outline-none focus:border-green-500"
        placeholder="User ID"
      />
      <button
        onClick={handleTrain}
        disabled={loading}
        className="w-full text-xs bg-green-700 hover:bg-green-600 disabled:opacity-50 py-1.5 rounded transition font-medium"
      >
        {loading ? 'Analisando...' : '▶ Analisar Performance'}
      </button>
      {result && (
        <div className="text-xs text-gray-300 mt-2 space-y-1">
          <p className="text-green-400 font-semibold">Plano gerado:</p>
          <p>Dificuldade: <span className="text-white">{result.recommended_difficulty}</span></p>
          {result.weak_areas?.length > 0 && (
            <p>Pontos fracos: <span className="text-red-300">{result.weak_areas.join(', ')}</span></p>
          )}
          <p>Próximo passo: <span className="text-yellow-300">{result.next_step}</span></p>
        </div>
      )}
    </div>
  )
}

// ─── Widget: Late Alerts ─────────────────────────────────────────────────────
function LateAlertsWidget() {
  const [data, setData] = useState(null)

  useEffect(() => {
    apiFetch('/dashboard/institutional')
      .then((d) => setData(d?.blocks?.late_alerts || []))
      .catch(() => setData([]))
  }, [])

  if (!data) return <p className="text-xs text-gray-500">Carregando...</p>
  if (!data.length) return <p className="text-xs text-green-400">✓ Nenhum atraso crítico.</p>

  return (
    <ul className="space-y-2">
      {data.map((a, i) => (
        <li key={i} className="text-xs bg-red-950 border border-red-800 rounded p-2">
          <p className="font-semibold text-red-300">{a.user_id}</p>
          <p className="text-gray-400">Cargo: {a.role} — {a.pending} trilha(s) pendente(s)</p>
        </li>
      ))}
    </ul>
  )
}
