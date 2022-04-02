import * as React from 'react';
import { Provider } from 'react-redux'
 

import store from '../app/store'

export default function MyApp({Component, pageProps}:{Component:any, pageProps:any}) {
  return (
    <Provider store={store}>
      <Component {...pageProps} />
    </Provider>
  );
}