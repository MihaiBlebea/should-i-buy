const cacheName = "v2"

const cacheAssets = [
	// "/public/index.html",
	// "/js/app.js",
	// "/js/chunk-vendors.js",
	// "/main.js"
]

self.addEventListener("register", event => {
	console.log("Service worker registered")
})

self.addEventListener("install", event => {
	// event.waitUntil(
	// 	caches
	// 		.open(cacheName)
	// 		.then(cache => {
	// 			console.log("caching files")
	// 			cache.addAll(cacheAssets)
	// 				.catch(err => {
	// 					console.error(err)
	// 				})
	// 		})
	// 		.then(() => self.skipWaiting())
	// )
	console.log("Service worker installed")
})

self.addEventListener("activate", event => {
	event.waitUntil(
		caches.keys().then(cacheNames => {
			return Promise.all(
				cacheNames.map(cache => {
					if (cache !== cacheName) {
						console.log("deleting cache " + cache)
						return caches.delete(cache)
					}
				})
			)
		})
	)
	console.log("Service worker activated")
})

self.addEventListener("fetch", event => {
	console.log("Service worker fetched req")
	if (event.request.url.includes("chrome-extension")) {
		return
	}
	event.respondWith(
		fetch(event.request)
			.then(response => {
				const clone = response.clone()
				
				caches
					.open(cacheName)
					.then(cache => {
						console.log("caching files")
						cache.put(event.request, clone)
					})

				return response
			})
	)
})