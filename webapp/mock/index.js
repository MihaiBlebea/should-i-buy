const fs = require("fs")
var cors = require("cors")

const loadData = (path) => JSON.parse(fs.readFileSync(path))

const routes = {
	compare: loadData("./mock/compare.json")
}


const jsonServer = require("json-server")
const server = jsonServer.create()
const router = jsonServer.router(routes)
const middlewares = jsonServer.defaults()

server.use(cors())
server.use(jsonServer.bodyParser)
server.use(middlewares)

server.use((req, res, next) => {
	console.log(req.url)
	// if (req.method !== "POST") {
	// 	next()
	// }

	if (req.path === "/compare") {
		res.status(200).json(loadData("./mock/compare.json")) 
	}

	if (req.path === "/stocks") {
		res.status(200).json(loadData("./mock/stocks.json")) 
	}
})

server.use(router)

server.listen(8081, ()=> { console.log("JSON Server is running") })