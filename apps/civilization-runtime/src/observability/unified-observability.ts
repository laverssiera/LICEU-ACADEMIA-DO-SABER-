import client from "prom-client"

export class UnifiedObservability {
  private readonly registry: client.Registry
  readonly activeStudents: client.Gauge
  readonly completedResearchPrograms: client.Counter
  readonly academyBrainSyncs: client.Counter<"status">
  readonly civilizationEducationSignalsPublished: client.Counter
  readonly civilizationGlobalIntelligenceScore: client.Gauge
  readonly civilizationGlobalEvents: client.Gauge
  readonly civilizationLastSyncTimestampSeconds: client.Gauge

  constructor() {
    this.registry = new client.Registry()

    this.activeStudents = new client.Gauge({
      name: "academy_active_students",
      help: "Students online",
      registers: [this.registry]
    })

    this.completedResearchPrograms = new client.Counter({
      name: "academy_completed_research_programs",
      help: "Research programs completed",
      registers: [this.registry]
    })

    this.academyBrainSyncs = new client.Counter({
      name: "civilization_education_brain_sync_total",
      help: "Total academy brain sync attempts by status",
      labelNames: ["status"],
      registers: [this.registry]
    })

    this.civilizationEducationSignalsPublished = new client.Counter({
      name: "civilization_education_signals_published_total",
      help: "Total civilization education signals published",
      registers: [this.registry]
    })

    this.civilizationGlobalIntelligenceScore = new client.Gauge({
      name: "civilization_education_global_intelligence_score",
      help: "Global collective educational intelligence score",
      registers: [this.registry]
    })

    this.civilizationGlobalEvents = new client.Gauge({
      name: "civilization_education_global_events",
      help: "Total global educational events in civilization memory",
      registers: [this.registry]
    })

    this.civilizationLastSyncTimestampSeconds = new client.Gauge({
      name: "civilization_education_last_sync_timestamp_seconds",
      help: "Last successful civilization education sync timestamp",
      registers: [this.registry]
    })
  }

  setStudents(value: number): void {
    this.activeStudents.set(value)
  }

  registerResearchProgram(): void {
    this.completedResearchPrograms.inc()
  }

  registerAcademyBrainSyncSuccess(signalsPublished: number, intelligenceScore: number, globalEvents: number): void {
    this.academyBrainSyncs.labels("success").inc()
    if (signalsPublished > 0) {
      this.civilizationEducationSignalsPublished.inc(signalsPublished)
    }
    this.civilizationGlobalIntelligenceScore.set(intelligenceScore)
    this.civilizationGlobalEvents.set(globalEvents)
    this.civilizationLastSyncTimestampSeconds.set(Math.floor(Date.now() / 1000))
  }

  registerAcademyBrainSyncFailure(): void {
    this.academyBrainSyncs.labels("failure").inc()
  }

  async metrics(): Promise<string> {
    return this.registry.metrics()
  }

  metricsContentType(): string {
    return this.registry.contentType
  }
}
