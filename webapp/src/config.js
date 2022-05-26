var env = process.env.NODE_ENV || "development"

var config = {
	development: {
		baseUrl: "http://192.168.1.17:8081"
	},
	production: {
		baseUrl: "https://shouldibuy.cap-rover.purpletreetech.com/api/v1"
	}
}

export default config[env]