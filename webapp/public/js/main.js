if ("serviceWorker" in navigator) {
	window.addEventListener("load", () => {
		navigator.serviceWorker.register("../sw_offline.js").then(reg => {
			// registration.pushManager.subscribe({ userVisibleOnly: true, 
			//   applicationServerKey: key });
			console.log("SW registered: ", reg);
		}).catch(err => {
			console.log("SW registration failed: ", err);
		})
	})
}