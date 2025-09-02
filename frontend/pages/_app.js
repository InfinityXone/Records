import '../styles/globals.css';
import { useEffect } from 'react';
import Head from 'next/head';

/**
 * Custom App component that registers the service worker and injects
 * meta tags required for Progressive Web App support. The service
 * worker is registered only in the browser after the page has
 * finished loading.  Meta tags such as theme-color and manifest
 * declaration ensure that browsers treat the application as a PWA.
 */
export default function App({ Component, pageProps }) {
  // Register service worker once after initial mount
  useEffect(() => {
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      const onLoad = () => {
        navigator.serviceWorker
          .register('/service-worker.js')
          .catch((err) => {
            console.error('ServiceWorker registration failed', err);
          });
      };
      window.addEventListener('load', onLoad);
      return () => window.removeEventListener('load', onLoad);
    }
  }, []);

  return (
    <>
      <Head>
        {/* Link the web app manifest */}
        <link rel="manifest" href="/manifest.json" />
        {/* Specify theme color for the browser UI */}
        <meta name="theme-color" content="#050a19" />
        {/* Enable standalone display on iOS */}
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta
          name="apple-mobile-web-app-status-bar-style"
          content="black-translucent"
        />
      </Head>
      <Component {...pageProps} />
    </>
  );
}