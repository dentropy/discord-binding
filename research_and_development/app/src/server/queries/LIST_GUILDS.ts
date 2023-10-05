import { glob, GlobOptions } from 'glob';
import sqlite from 'better-sqlite3';

function addSlashIfNotPresent(inputString : string) {
  if (inputString.charAt(inputString.length - 1) !== '/') {
    return inputString + '/';
  } else {
    return inputString;
  }
}

export async function LIST_GUILD(guild_path : string){
    console.log("RUNNING LIST_GUILD")
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
    let guilds_listed : any= []
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
        guilds_listed.push(result[0])
    });
    return guilds_listed
}