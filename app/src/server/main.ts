import express from "express";
import ViteExpress from "vite-express";
import 'dotenv/config'

import { GUILD_TO_PATH } from "./queries/GUILD_TO_PATH";
import { perform_query } from "./queries";
const app = express();
app.use(express.json());

let guild_id_to_path : any ;
async function main(){
  guild_id_to_path = await GUILD_TO_PATH(String(process.env.guild_directory_path))
}
main()

app.get("/hello", (_, res) => {
  res.send("Hello Vite + React + TypeScript!");
});

app.post("/QUERY", async (req, res) => {
  // console.log(req.body)
  let resJSON = await perform_query(guild_id_to_path, req.body)
  // let resJSON : any = req.body
  // resJSON.resolved = true

  res.json(resJSON);
});

app.post("/QUERY2", async (req, res) => {
  res.json(guild_id_to_path);
});

ViteExpress.listen(app, 3000, () =>
  console.log("Server is listening on port 3000...")
);
