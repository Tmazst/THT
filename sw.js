
self.addEventListener('install', function(event) {
  console.log('[Service Worker] Installing Service Worker ...', event);
});
self.addEventListener('activate', function(event) {
  console.log('[Service Worker] Activating Service Worker ...', event);
});
self.addEventListener('fetch', function(event) {
  // console.log('[Service Worker] Fetching something ...', event);
});


self.addEventListener("push", event => {
  const data = event.data.json();
  self.registration.showNotification(data.title, {
      body: data.body,
      icon: "/static/icons/icon_192x192.png"
  });
});