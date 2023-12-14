

function getValuesForKey(list, key) {
  return list.map(item => item[key]);
}

export default function reducer(state, action) {
    switch (action.type) {
      case 'SELECT_GUILD':
        return { ...state, select_guild: action.payload };
      case 'SELECT_CHANNEL':
        return { ...state, select_channel: action.payload };
      case 'SELECT_AUTHOR':
        return { ...state, select_author: action.payload };
      case 'SELECT_QUERY':
        return { ...state, select_query: action.payload };
      case 'SELECT_DATA_VISUALIZATION':
        return { ...state, select_data_visualization: action.payload };
      case 'SET_DATA_VISUALIZATIONS':
        return { ...state, data_visualizations: action.payload };
      case 'INCREMENT':
        return { ...state, count: state.count + action.payload };
      case 'DECREMENT':
        return { ...state, count: state.count - action.payload };
      case 'SET_QUERIES':
        return { ...state, queries: action.payload };
      case 'SET_GUILDS':
        return { ...state, guilds: action.payload };
      case 'SET_AND_SELECT_CHANNELS':
        console.log("SET_AND_SELECT_CHANNELS")
        console.log(state.channels)
        state.channels.options = action.payload
        state.channels.selected_value = state.channels.options[0]
        state.channels.value = state.channels.selected_value.label
        console.log(state.channels)
        return state;
      case 'SET_AND_SELECT_AUTHORS':
        console.log("SET_AND_SELECT_AUTHORS")
        console.log(state.authors)
        state.authors.options = action.payload
        state.authors.selected_value = state.channels.options[0]
        state.authors.value = state.channels.options[0].label
        console.log(state.authors)
        return state;
      case 'SET_DATA_VISUALIZATION_DATA':
        return { ...state, data_visualization_data: action.payload };
      case 'RENDER_NOW':
        return { ...state, render_now: action.payload };
      case 'RENDER_NOW':
        return { ...state, render_now: action.payload };
      case 'ADD_MESSAGE_ID':
        console.log(action.payload)
        if(!state.selected_messages.includes(action.payload.id)){
          state.selected_messages.push(action.payload) 
          return { ...state, selected_messages: state.selected_messages }
        }
        return { ...state };
      case 'REMOVE_MESSAGE_ID':
        for(var i = 0; i < state.selected_messages.length; i++){
          if( state.selected_messages[i].id == action.payload.id)
          {
            state.selected_messages.splice(i, 1)
          }
        }
        return { ...state,  selected_messages : state.selected_messages};
      default:
        throw new Error();
    }
  }