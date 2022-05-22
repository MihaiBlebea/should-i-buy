import { createRouter, createWebHashHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import CompareStocks from "../views/CompareStocks.vue"

const routes = [
	// {
	// 	path: "/",
	// 	name: "home",
	// 	component: HomeView
	// },
	{
		path: "/",
		name: "Compare",
		// route level code-splitting
		// this generates a separate chunk (about.[hash].js) for this route
		// which is lazy-loaded when the route is visited.
		component: CompareStocks
	}
]

const router = createRouter({
	history: createWebHashHistory(),
	routes
})

export default router
