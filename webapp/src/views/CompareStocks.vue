<template>
	<div class="container mt-5">
		<div class="row justify-content-center">
			<div class="col-md-6">
				<h1 class="mb-3">Compare stocks</h1>

				<CompareTableStockSelector 
					class="mb-3" 
					v-on:selected="selectedStockHandler"
				/>

				<CompareTable 
					:indicators="indicators" 
					:symbols="selectedSymbols" 
				/>

			</div>
		</div>
	</div>
</template>

<script>
import axios from "axios"
import Navbar from "./../components/Navbar.vue"
import CompareTable from "./../components/CompareTable.vue"
import CompareTableStockSelector from "./../components/CompareTableStockSelector.vue"

export default {
	components: {
		CompareTable,
		CompareTableStockSelector,
		Navbar
	},
	data: ()=> {
		return {
			selected: [],
			indicators: [],
			symbols: []
		}
	},
	computed: {
		selectedSymbols() {
			return this.symbols.filter(symbol => {
				return this.selected.includes(symbol.symbol)
			})
		}
	},
	methods: {
		getCompareData() {
			axios.get("http://localhost:8081/compare").then(result => {
				this.symbols = result.data.symbols
				this.indicators = result.data.indictors
			}).catch(err => {
				console.error(err)
			})
		},
		selectedStockHandler(selected) {
			console.log(selected)
			this.selected = selected
		}
	},
	mounted() {
		this.getCompareData()
	}
}
</script>

