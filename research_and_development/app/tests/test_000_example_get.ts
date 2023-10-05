import assert from 'assert';

describe('Connection test', async function () {
  it('Perform Example Get Request', async function () {
    let response : any= await fetch("http://localhost:3000/hello")
    response = await response.text()
    assert.equal(response, "Hello Vite + React + TypeScript!", "Response string is wrong")
  })
})