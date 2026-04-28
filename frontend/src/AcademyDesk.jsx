import { useEffect, useState, useCallback } from 'react'

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
