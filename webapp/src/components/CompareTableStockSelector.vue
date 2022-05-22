<template>
	<div>
		<button class="button is-primary" v-on:click="toggleModal">Add stock</button>
		<div class="modal justify-content-start align-items-stretch p-4" v-bind:class="{'is-active': showModal}">
			<div class="modal-background"></div>

			<div class="row justify-content-center top mt-5">
				<div class="col-6">
			
					<div class="field">
						<p class="control is-expanded has-icons-left">
							<input 
								class="input" 
								type="search" 
								placeholder="Stock search" 
								v-model="search"
							/>
							<span class="icon is-small is-left"><i class="fa fa-search"></i></span>
						</p>
					</div>

					<div class="tags" v-if="showTags">
						<span 
							class="tag is-warning is-medium" 
							v-for="(stock, index) in selected" 
							:key="index"
							v-on:click="removeStock(stock)"
						>
							{{ stock }}
							<button class="delete is-small"></button>
						</span>
					</div>
					<div v-else class="mb-3 mt-2 text-muted">
						<i>No stock selected</i>
					</div>

					<div>
						<div
							class="d-flex justify-content-between mb-3 pointer"
							v-for="(stock, index) in found" 
							:key="index"
							v-on:click="selectStockHandler(stock)"
						>
							<span>{{ stock.title }}</span>
							<span>{{ stock.symbol }}</span>
						</div>
					</div>

				</div>
			</div>
			<button 
				class="modal-close is-large" 
				aria-label="close" 
				v-on:click="toggleModal"
			></button>
		</div>
	</div>
</template>

<script>
import config from "./../config"
import axios from "axios"

export default {
	data: ()=> {
		return {
			showModal: false,
			found: [],
			search: "",
			stocks: [],
			selected: []
		}
	},
	watch: {
		search(val, old) {
			if (val === "") {
				this.found = []
				return
			}
			let found = []
			this.stocks.forEach(stock => {
				if (stock.symbol.startsWith(val.toUpperCase())
					|| stock.title.toUpperCase().startsWith(val.toUpperCase())
				) {
					found.push(stock)
				}
			})
			this.found = found
		}
	},
	computed: {
		showTags() {
			return this.selected.length > 0
		}
	},
	methods: {
		getStockData() {
			axios.get(config.baseUrl + "/stocks").then(result => {
				this.stocks = result.data.stocks
			}).catch(err => {
				console.error(err)
			})
		},
		toggleModal() {
			if (this.showModal === true) {
				this.$emit("selected", this.selected)
			} else {
				this.search = ""
			}
			this.showModal = !this.showModal

		},
		selectStockHandler(stock) {
			if (this.selected.length === 3) {
				return
			}

			if (this.selected.includes(stock.symbol)) {
				return
			}

			this.selected.push(stock.symbol)
		},
		removeStock(stock) {
			this.selected = this.selected.filter(sel => {
				return sel !== stock 
			})
		}
	},
	mounted() {
		this.getStockData()
	}
}
</script>

<style scoped>
.top {
	z-index: 1000;
	color: #FFF;
}

.pointer {
	cursor: pointer;
}
</style>
