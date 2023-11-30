export default function reducer(state, action) {
    switch (action.type) {
      case 'INCREMENT':
        return { ...state, count: state.count + action.payload };
      case 'DECREMENT':
        return { ...state, count: state.count - action.payload };
      case 'SET_QUERIES':
        return { ...state, queries: action.payload };
      case 'SET_GUILDS':
        return { ...state, guilds: action.payload };
      case 'SET_CHANNELS':
        return { ...state, channels: action.payload };
      case 'SET_AUTHORS':
        return { ...state, authors: action.payload };
      case 'SET_DATA_VISUALIZATIONS':
        return { ...state, data_visualizations: action.payload };
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
      case 'SET_DATA_VISUALIZATION_DATA':
        return { ...state, data_visualization_data: action.payload };
      case 'RENDER_NOW':
        return { ...state, render_now: action.payload };
      default:
        throw new Error();
    }
  }