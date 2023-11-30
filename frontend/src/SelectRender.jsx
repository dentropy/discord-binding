import * as React from 'react';
import { Context } from './Provider';
import Button from '@mui/material/Button';

export default function SelectRender() {
  const [context, setContext] = React.useContext(Context);

  function update_context() {
    // console.log("UDPATE RENDER_NOW")
    setContext({
        type: 'RENDER_NOW',
        payload: true
    })
  }
  return (
    <>
        <Button variant="outlined" onClick={update_context}>Render Data Visualization</Button>
    </>
  );
}
