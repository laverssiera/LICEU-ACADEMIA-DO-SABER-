import express from "express";

const app = express();

app.get("/", (_req, res) => {
  res.json({ service: "admin", status: "running", panel: "enterprise" });
});

app.listen(8160, () => {
  console.log("Admin service running on 8160");
});
