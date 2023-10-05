import assert from 'assert';

describe('GET GUILD USERS', async function () {
  let guild_id : string = ""
  it('Perform Example Get Request', async function () {
    let requestData :any = {
      QUERY_NAME : "LIST_GUILDS",
      QUERY_PARAMS : {}
    }
    let requestOptions : any = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    }
    let response : any= await fetch("http://localhost:3000/QUERY", requestOptions)
    response = await response.json()
    console.log(  JSON.stringify(response, null, 2)  )
    guild_id = response[0].guild_id
  })
  it('Perform Example Get Request', async function () {
    console.log(guild_id)
    let requestData :any = {
      QUERY_NAME : "LIST_USERS",
      QUERY_PARAMS : {
        "GUILD_ID" : guild_id
      }
    }
    let requestOptions : any = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    }
    let response : any= await fetch("http://localhost:3000/QUERY", requestOptions)
    response = await response.json()
    console.log(  JSON.stringify(response, null, 2)  )
  })
})