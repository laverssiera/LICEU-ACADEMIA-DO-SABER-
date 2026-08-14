export type ConsumedEvent =
  | "research.breakthrough"
  | "research.material.discovered"
  | "research.agi.generated"
  | "archimedes.housing.problem"
  | "econotech.market.signal"
  | "cea.scholarship.created"
  | "fornecedor.new-composite.created"
  | "hub.workforce.shortage"

export interface Emission {
  subject: string
  payload: Record<string, unknown>
}

export const CONSUMED_EVENTS: readonly ConsumedEvent[] = [
  "research.breakthrough",
  "research.material.discovered",
  "research.agi.generated",
  "archimedes.housing.problem",
  "econotech.market.signal",
  "cea.scholarship.created",
  "fornecedor.new-composite.created",
  "hub.workforce.shortage"
] as const

export function routeEvent(subject: ConsumedEvent, payload: Record<string, unknown>, timestamp = Date.now()): Emission[] {
  switch (subject) {
    case "research.breakthrough":
      return [
        {
          subject: "academy.research.program.created",
          payload: {
            track: "applied-breakthrough-program",
            source: payload,
            generated_at: timestamp
          }
        },
        {
          subject: "academy.knowledge.sync",
          payload: {
            source_event: "research.breakthrough",
            synchronized_at: timestamp
          }
        }
      ]
    case "research.material.discovered":
      return [
        {
          subject: "academy.path.created",
          payload: {
            path: "advanced-materials-engineering",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
    case "research.agi.generated":
      return [
        {
          subject: "academy.talent.detected",
          payload: {
            domain: "agi",
            source: payload,
            generated_at: timestamp
          }
        },
        {
          subject: "academy.research.program.created",
          payload: {
            track: "agi-safety-and-systems",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
    case "archimedes.housing.problem":
      return [
        {
          subject: "academy.path.created",
          payload: {
            path: "housing-infrastructure-optimization",
            source: payload,
            generated_at: timestamp
          }
        },
        {
          subject: "academy.workforce.generated",
          payload: {
            role: "housing-systems-engineer",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
    case "econotech.market.signal":
      return [
        {
          subject: "academy.path.created",
          payload: {
            path: "market-responsive-technology",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
    case "cea.scholarship.created":
      return [
        {
          subject: "academy.student.certified",
          payload: {
            certification: "foundation-readiness",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
    case "fornecedor.new-composite.created":
      return [
        {
          subject: "academy.research.program.created",
          payload: {
            track: "composite-materials-application",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
    case "hub.workforce.shortage":
      return [
        {
          subject: "academy.workforce.generated",
          payload: {
            response: "accelerated-workforce-pipeline",
            source: payload,
            generated_at: timestamp
          }
        }
      ]
  }
}
