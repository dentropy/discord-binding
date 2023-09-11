
import { LIST_GUILD } from "./queries/LIST_GUILDS";
import { LIST_USERS } from "./queries/LIST_USERS";
export async function perform_query(guild_id_to_path : any, query_json : any){
    if(query_json.QUERY_NAME == "LIST_GUILDS"){
        return(
          await LIST_GUILD(String(process.env.guild_directory_path))
        )
    }
    if(query_json.QUERY_NAME == "LIST_USERS"){
        return(
          await LIST_USERS(guild_id_to_path[query_json.QUERY_PARAMS.GUILD_ID])
        )
    }
}