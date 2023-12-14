import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Messages from './Messages.jsx';
import Homepage from './Homepage.jsx';
// import './index.css'

import Provider from './Provider';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Homepage />,
  },
  {
    path: "/graph-ui",
    element: <App />,
  },
  {
    path: "/messages",
    element: <Provider><Messages /></Provider>,
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  // <React.StrictMode>
    // <Provider>
    <>
      <RouterProvider router={router} />
    </>
    // </Provider>
  // </React.StrictMode>,
)
