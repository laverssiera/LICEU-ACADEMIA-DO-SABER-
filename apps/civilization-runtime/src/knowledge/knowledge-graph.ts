import neo4j, { type Driver } from "neo4j-driver"

interface LearningPathPayload {
  id: string
  name: string
  domain: string
  level: string
}

export class EducationalKnowledgeGraph {
  private driver: Driver

  constructor() {
    this.driver = neo4j.driver(
      process.env.NEO4J_URI!,
      neo4j.auth.basic(process.env.NEO4J_USER!, process.env.NEO4J_PASSWORD!)
    )
  }

  async registerLearningPath(payload: LearningPathPayload): Promise<void> {
    const session = this.driver.session()

    await session.run(
      `
      MERGE (p:LearningPath {
        id: $id
      })
      SET p.name = $name,
          p.domain = $domain,
          p.level = $level,
          p.created_at = datetime()
      `,
      payload
    )

    await session.close()
  }

  async connectResearchAndCourse(researchId: string, courseId: string): Promise<void> {
    const session = this.driver.session()

    await session.run(
      `
      MATCH (r:Research {id: $researchId})
      MATCH (c:LearningPath {id: $courseId})

      MERGE (c)-[:TEACHES]->(r)
      `,
      {
        researchId,
        courseId
      }
    )

    await session.close()
  }
}
