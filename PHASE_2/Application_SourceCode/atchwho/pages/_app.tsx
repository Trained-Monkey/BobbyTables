import * as React from 'react';

export default function MyApp({Component, pageProps}:{Component:any, pageProps:any}) {
  return <Component {...pageProps} />;
}