import assert from 'assert';

describe('LIST GUILDS', async function () {
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
    // console.log(  JSON.stringify(response, null, 2)  )
  })
})