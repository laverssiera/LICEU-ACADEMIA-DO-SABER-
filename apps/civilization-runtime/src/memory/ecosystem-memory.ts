import { Redis } from "ioredis"

export class EcosystemMemory {
  private redis: Redis

  constructor() {
    this.redis = new Redis(process.env.REDIS_URL!)
  }

  async storeLearningMemory<T>(key: string, payload: T): Promise<void> {
    await this.redis.set(`education:${key}`, JSON.stringify(payload))
  }

  async recoverLearningMemory<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(`education:${key}`)

    if (!data) {
      return null
    }

    return JSON.parse(data) as T
  }

  async incrementLearningCounter(key: string): Promise<number> {
    return this.redis.incr(`education:${key}`)
  }

  async getLearningCounter(key: string): Promise<number> {
    const data = await this.redis.get(`education:${key}`)

    if (!data) {
      return 0
    }

    const parsed = Number.parseInt(data, 10)
    return Number.isNaN(parsed) ? 0 : parsed
  }
}
