import express from "express";
import ViteExpress from "vite-express";
import 'dotenv/config'

const app = express();
app.use(express.json());

app.get("/hello", (_, res) => {
  res.send("Hello Vite + React + TypeScript!");
});

app.post("/QUERY", async (req, res) => {
  console.log(req.body)
  console.log(process.env.guild_directory_path)
  let resJSON : any = req.body
  resJSON.resolved = true
  res.json({
    resJSON
  });
});

ViteExpress.listen(app, 3000, () =>
  console.log("Server is listening on port 3000...")
);
