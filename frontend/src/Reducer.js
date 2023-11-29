export default function reducer(state, action) {
    switch (action.type) {
      case 'INCREMENT':
        return { ...state, count: state.count + action.payload };
      case 'DECREMENT':
        return { ...state, count: state.count - action.payload };
      case 'SET_GUILDS':
        return { ...state, guilds: action.payload };
      case 'SET_CHANNELS':
        return { ...state, channels: action.payload };
      case 'SET_AUTHORS':
        return { ...state, authors: tmp_metadata };
      case 'SELECT_GUILD':
        return { ...state, select_guild: action.payload };
      case 'SELECT_CHANNEL':
        return { ...state, select_channel: action.payload };
      case 'SELECT_AUTHOR':
        return { ...state, select_author: action.payload };
      default:
        throw new Error();
    }
  }