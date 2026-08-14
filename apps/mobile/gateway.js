import express from "express";

const app = express();
app.get("/", (_req, res) => res.json({ service: "mobile-gateway", status: "ok" }));

app.listen(8090, () => {
  console.log("Mobile gateway running on 8090");
});
