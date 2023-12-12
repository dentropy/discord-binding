import * as React from 'react';
import { Context } from './Provider';
import SelectDiscordData from './SelectDiscordData'
import DisplayMessages from './DisplayMessages'
function Messages() {
    const [context, setContext] = React.useContext(Context);

    return (
      <>
        <h1>Messages</h1>
        <DisplayMessages />
        {/* <SelectDiscordData /> */}
      </>
    )
  }
  
  export default Messages
  