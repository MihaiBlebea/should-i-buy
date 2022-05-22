<template>
	<div>
		<Navbar />
		<!-- <nav>
			<router-link to="/">Home</router-link> |
			<router-link to="/compare">Compare</router-link>
		</nav> -->
		<router-view />
	</div>
</template>

<script>
import Navbar from "./components/Navbar.vue"

export default {
	components: {
		Navbar
	}
}
</script>


