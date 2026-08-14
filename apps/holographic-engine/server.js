import express from "express";

const app = express();
app.use(express.json());

app.post("/holography/render", async (req, res) => {
  return res.json({
    rendered: true,
    scene: "steel_structure_room",
    fps: 60,
    xr_ready: true,
  });
});

app.listen(8120, () => {
  console.log("Holographic Engine Running");
});
