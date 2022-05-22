var env = process.env.NODE_ENV || "development"

var config = {
	development: {
		baseUrl: "http://localhost:8081"
	},
	production: {
		baseUrl: "https://shouldibuy.cap-rover.purpletreetech.com/"
	}
}

export default config[env]