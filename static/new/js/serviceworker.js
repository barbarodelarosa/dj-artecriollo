// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
	'/static/new/css/bootstrap.min.css',
	'/static/new/css/slick.css',
	'/static/new/css/slick-theme.css',
	'/static/new/css/nouislider.min.css',
	'/static/new/css/font-awesome.min.css',
	'/static/new/css/style.css',
	'/static/new/css/mystyle.css',
    '/static/new/css/ajax-loader.gif',

	'/static/new/js/bootstrap.min.js',
	'/static/new/js/cart.js',
	'/static/new/js/countdown.js',
	'/static/new/js/jquery.min.js',
	'/static/new/js/jquery.zoom.min.js',
	'/static/new/js/main.js',
	'/static/new/js/mycode.js',

    '/static/images/logo.png',
    '/static/images/no-image.png',
    '/static/images/icon.ico',

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