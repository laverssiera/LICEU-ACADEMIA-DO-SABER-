import express from "express";

const app = express();

app.get("/", (_req, res) => {
  res.json({ service: "realtime", protocol: "websocket", status: "ready" });
});

app.listen(8150, () => {
  console.log("Realtime service running on 8150");
});
