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
    '/static/images/imagen-inicio.png',
    '/static/images/icon.ico',
    '/static/images/tarjetas/tarjeta-banco-metropolitano.jpg',
    '/static/images/tarjetas/tarjeta-bandec.jpg',
    '/static/images/tarjetas/tarjeta-bpa.jpg',
    '/static/images/enzona/enzona.png',
    '/static/images/enzona/logo.png',

	'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',

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
				alert("No tienes conexion a internet :(")
                return caches.match('/offline/');
            })
    )
});



// SERVER FROM FULL CACHE
// self.addEventListener("fetch", function(event){
// 	event.respondWith(
// 		fetch(event.request)
// 		.then(function(result){
// 			return caches.open(staticCacheName)
// 			.then(function(c){
// 				c.put(event.request.url, result.clone())
// 				return result
// 			})
// 		})
// 		.catch(function(e){
// 			return caches.match(event.request)
// 		})
// 	)
// })