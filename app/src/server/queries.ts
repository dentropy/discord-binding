
import { LIST_GUILD } from "./queries/LIST_GUILDS";

export async function perform_query(query_json : any){
  return(await LIST_GUILD(query_json.guild_path))
}