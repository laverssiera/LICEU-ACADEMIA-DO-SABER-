import express from "express";

const app = express();

app.get("/", (_req, res) => {
  res.json({ engine: "streaming", protocol: "realtime", status: "running" });
});

app.listen(8130, () => {
  console.log("Streaming Engine Running");
});
