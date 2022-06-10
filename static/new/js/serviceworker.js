// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
	'/new/css/bootstrap.min.css',
	'/new/css/slick.css',
	'/new/css/slick-theme.css',
	'/new/css/nouislider.min.css',
	'/new/css/font-awesome.min.css',
	'/new/css/style.css',
	'/new/css/mystyle.css',

	'/new/js/bootstrap.min.js',
	'/new/js/cart.js',
	'/new/js/countdown.js',
	'/new/js/jquery.min.js',
	'/new/js/jquery.zoo.min.js',
	'/new/js/main.js',

    '/images/loading/loading.gif',
    '/images/logo.png',
    '/images/no-image.png',
    '/images/icon.ico',

];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});