import { connect, StringCodec, type Msg, type NatsConnection, type Subscription } from "nats"

export class FederationAuthority {
  private nc: NatsConnection | null = null
  private readonly codec = StringCodec()

  async connect(): Promise<void> {
    this.nc = await connect({
      servers: process.env.NATS_SERVERS
    })
  }

  async registerAcademy(): Promise<void> {
    if (!this.nc) {
      throw new Error("NATS connection not initialized")
    }

    this.nc.publish(
      "federation.monolith.registered",
      this.codec.encode(
        JSON.stringify({
          monolith: "ACADEMIA_DO_SABER",
          type: "civilization-education-runtime"
        })
      )
    )
  }

  async synchronizeKnowledge(): Promise<void> {
    if (!this.nc) {
      throw new Error("NATS connection not initialized")
    }

    this.nc.publish(
      "education.federation.sync",
      this.codec.encode(
        JSON.stringify({
          timestamp: Date.now()
        })
      )
    )
  }

  publish(subject: string, payload: unknown): void {
    if (!this.nc) {
      throw new Error("NATS connection not initialized")
    }

    this.nc.publish(subject, this.codec.encode(JSON.stringify(payload)))
  }

  subscribe(subject: string): Subscription {
    if (!this.nc) {
      throw new Error("NATS connection not initialized")
    }

    return this.nc.subscribe(subject)
  }

  decode(msg: Msg): string {
    return this.codec.decode(msg.data)
  }

  async close(): Promise<void> {
    if (!this.nc) {
      return
    }

    await this.nc.drain()
    this.nc = null
  }

  isConnected(): boolean {
    return this.nc !== null && !this.nc.isClosed()
  }
}
