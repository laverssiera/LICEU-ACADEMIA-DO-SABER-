import express from "express";

const app = express();

app.get("/", (_req, res) => {
  res.json({ engine: "ai-engine", status: "running" });
});

app.listen(8140, () => {
  console.log("AI Engine running on 8140");
});
