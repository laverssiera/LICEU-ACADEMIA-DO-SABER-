import express from "express";

const app = express();
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({ platform: "LICEU API Node", version: "7.0", status: "running" });
});

app.listen(3000, () => {
  console.log("API Node running on 3000");
});
