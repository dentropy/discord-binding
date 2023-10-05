import sqlite from 'better-sqlite3';

export async function LIST_USERS(sqlite_path : string){
    let query = `
        SELECT
            DISTINCT( json_extract(raw_json, '$.id') ) as author_id,
            json_extract(raw_json, '$.name') as name,
            json_extract(raw_json, '$.is_bot') as is_bot
        FROM
            raw_authors_t
    `
    const db = new sqlite(sqlite_path)
    let result : any  = await db.prepare(query).all();
    await db.close()
    return result
}