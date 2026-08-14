import { randomUUID } from "node:crypto"
import { createServer } from "node:http"
import { FederationAuthority } from "./federation/federation-authority.js"
import { EducationalKnowledgeGraph } from "./knowledge/knowledge-graph.js"
import { EcosystemMemory } from "./memory/ecosystem-memory.js"
import { UnifiedObservability } from "./observability/unified-observability.js"
import { CONSUMED_EVENTS, type ConsumedEvent } from "./runtime/event-router.js"
import { bridgeAcademyCivilizationBrain } from "./runtime/academy-brain-bridge.js"
import { processConsumedEvent } from "./runtime/process-consumed-event.js"

const startupTs = Date.now()

async function bootstrap(): Promise<void> {
  const federation = new FederationAuthority()
  const graph = new EducationalKnowledgeGraph()
  const memory = new EcosystemMemory()
  const observability = new UnifiedObservability()
  const consumedCounters: Partial<Record<ConsumedEvent, number>> = {}
  let publishedCount = 0
  const academyBrainSyncEnabled = (process.env.ACADEMY_BRAIN_SYNC_ENABLED ?? "true").toLowerCase() === "true"
  const academyBrainSyncUrl = process.env.ACADEMY_BRAIN_SYNC_URL ?? "http://localhost:8000/education/civilization-brain/sync"
  const academyBrainPollMs = Number.parseInt(process.env.ACADEMY_BRAIN_SYNC_POLL_MS ?? "30000", 10)
  let academyBrainInterval: NodeJS.Timeout | null = null
  const port = Number.parseInt(process.env.PORT ?? "8910", 10)

  await federation.connect()
  await federation.registerAcademy()

  try {
    await graph.registerLearningPath({
      id: randomUUID(),
      name: "Planetary Engineering",
      domain: "interplanetary-science",
      level: "doctorate"
    })
  } catch (error) {
    console.warn("Knowledge graph unavailable during startup, continuing runtime", error)
  }

  await memory.storeLearningMemory("mars-habitat-program", {
    active: true
  })

  observability.setStudents(1000)

  for (const subject of CONSUMED_EVENTS) {
    const subscription = federation.subscribe(subject)

    ;(async () => {
      for await (const msg of subscription) {
        const received = federation.decode(msg)

        console.log(`ACADEMIA RECEIVED [${subject}]: ${received}`)
        consumedCounters[subject] = (consumedCounters[subject] ?? 0) + 1
        const published = await processConsumedEvent({
          subject,
          received,
          publish: (emissionSubject, payload) => {
            federation.publish(emissionSubject, payload)
          },
          memory,
          observability
        })
        publishedCount += published
      }
    })().catch((error) => {
      console.error(`Subscription failure for ${subject}`, error)
    })
  }

  if (academyBrainSyncEnabled) {
    const syncAcademyBrain = async (): Promise<void> => {
      try {
        const result = await bridgeAcademyCivilizationBrain({
          syncUrl: academyBrainSyncUrl,
          limit: 20,
          publish: (subject, payload) => {
            federation.publish(subject, payload)
          },
          memory
        })

        observability.registerAcademyBrainSyncSuccess(
          result.signalsPublished,
          result.collectiveIntelligenceScore,
          result.globalEvents
        )
        publishedCount += result.signalsPublished + (result.statePublished ? 1 : 0)
      } catch (error) {
        observability.registerAcademyBrainSyncFailure()
        console.warn("Academia civilization brain sync unavailable, continuing runtime", error)
      }
    }

    await syncAcademyBrain()
    academyBrainInterval = setInterval(() => {
      void syncAcademyBrain()
    }, academyBrainPollMs)
  }

  const server = createServer(async (req, res) => {
    const url = req.url ?? "/"

    if (url === "/healthz") {
      res.writeHead(200, { "content-type": "application/json" })
      res.end(JSON.stringify({ status: "ok", service: "academia-runtime" }))
      return
    }

    if (url === "/readyz") {
      const ready = federation.isConnected()
      res.writeHead(ready ? 200 : 503, { "content-type": "application/json" })
      res.end(JSON.stringify({ ready, nats_connected: ready }))
      return
    }

    if (url === "/metrics") {
      const metrics = await observability.metrics()
      res.writeHead(200, { "content-type": observability.metricsContentType() })
      res.end(metrics)
      return
    }

    if (url === "/runtime/stats") {
      const redisPublishedWorkforce = await memory.getLearningCounter("events:published:academy.workforce.generated")
      const redisPublishedCognitionSignals = await memory.getLearningCounter("events:published:civilization.education.signal.propagated")
      const redisPublishedGlobalState = await memory.getLearningCounter("events:published:civilization.education.global-state.updated")

      res.writeHead(200, { "content-type": "application/json" })
      res.end(
        JSON.stringify({
          uptime_ms: Date.now() - startupTs,
          consumed: consumedCounters,
          published_total: publishedCount,
          redis_workforce_generated: redisPublishedWorkforce,
          redis_civilization_signals_published: redisPublishedCognitionSignals,
          redis_global_state_published: redisPublishedGlobalState
        })
      )
      return
    }

    res.writeHead(404, { "content-type": "application/json" })
    res.end(JSON.stringify({ error: "not_found" }))
  })

  await new Promise<void>((resolve) => {
    server.listen(port, () => {
      console.log(`ACADEMIA DO SABER ONLINE - EVENT BRIDGE ACTIVE - PORT ${port}`)
      resolve()
    })
  })

  const shutdown = async (signal: string): Promise<void> => {
    console.log(`Shutting down civilization runtime due to ${signal}`)
    if (academyBrainInterval) {
      clearInterval(academyBrainInterval)
      academyBrainInterval = null
    }
    await new Promise<void>((resolve, reject) => {
      server.close((error) => {
        if (error) {
          reject(error)
          return
        }

        resolve()
      })
    })
    await federation.close()
    process.exit(0)
  }

  process.on("SIGINT", () => {
    void shutdown("SIGINT")
  })

  process.on("SIGTERM", () => {
    void shutdown("SIGTERM")
  })

  await new Promise<void>(() => {
    // Keep runtime alive to process the education event mesh.
  })
}

bootstrap().catch((error) => {
  console.error("Failed to bootstrap civilization runtime", error)
  process.exitCode = 1
})
