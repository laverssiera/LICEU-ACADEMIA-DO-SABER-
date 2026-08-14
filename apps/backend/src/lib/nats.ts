import { connect } from "nats";

export async function publishEvent(subject: string, payload: any) {
  const nc = await connect({ servers: "nats://localhost:4222" });
  nc.publish(subject, Buffer.from(JSON.stringify(payload)));
}
