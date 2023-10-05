import { glob } from 'glob';
import sqlite from 'better-sqlite3';

function addSlashIfNotPresent(inputString : string) {
  if (inputString.charAt(inputString.length - 1) !== '/') {
    return inputString + '/';
  } else {
    return inputString;
  }
}

export async function GUILD_TO_PATH(guild_path : string){
    console.log("LIST_GUILD")
    guild_path = addSlashIfNotPresent(guild_path)
    guild_path += "*"
    let file_list : any = await glob(guild_path + "*", {nodir : true})
    let query = `
        SELECT
            json_extract(raw_json, '$.id') as guild_id,
            json_extract(raw_json, '$.name') as guild_name
        FROM
            raw_guilds_t
        LIMIT 1
    `
    let guild_to_path : any = {}
    guild_to_path.LIST_GUILDS = []
    // for(var i = 0; i < file_list.length; i++){
    //   // console.log("sqlite_path")
    //   // console.log(file_list[i])
    //   const db = new sqlite(file_list[i])
    //   let result : any  = await db.prepare(query).all();
    //   await db.close()
    //   // console.log(result)
    //   guilds_listed.push(result)
    // }
    file_list.forEach( async(sqlite_path : string) => {
        // console.log("sqlite_path")
        // console.log(sqlite_path)
        const db = new sqlite(sqlite_path)
        let result : any  = await db.prepare(query).all();
        await db.close()
        // console.log(result)
        guild_to_path[result[0].guild_id] = sqlite_path
        guild_to_path.LIST_GUILDS.push(result[0])
    });
    return guild_to_path
}