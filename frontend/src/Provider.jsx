// Provider.js
import { createContext, useReducer } from 'react';
import reducer from './Reducer';

export const Context = createContext();

const initialState = {
  count          : 0,
  queries         : [
    { label : "Fetching Data", id : 0 }
  ],
  guilds         : [
    { label : "Fetching Data", id : 0 }
  ],
  channels       : {
    selected_value : { label : "Fetching Data", id : 0 },
    value : "Fetching Data",
    options : [{ label : "Fetching Data", id : 0 }]
  },
  authors       : {
    selected_value : { label : "Fetching Data", id : 0 },
    value : "Fetching Data",
    options : [{ label : "Fetching Data", id : 0 }]
  },
  data_visualizations  : [
    { label : "Fetching Data", id : 0 }
  ],
  select_query   : {
    label : "Getting Data"
  },
  select_guild   : {
    label : "Getting Data"
  },
  select_channel : {
    label : "Getting Data"
  },
  select_author  : {
    label : "Getting Data"
  },
  select_data_visualization  : {
    label : "Getting Data",
    description : "Loading...",
    query_data : {
      description : "Loading...."
    }
  },
  data_visualization_data : {
    label : "Getting Data"
  },
  render_now : false,
  selected_messages : []
};

export default function Provider(props) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <Context.Provider value={[state, dispatch]}>
      {props.children}
    </Context.Provider>
  );
}