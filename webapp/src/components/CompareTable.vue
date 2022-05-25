<template>
	<div v-if="showTable">
		<CompareTableRow class="mb-3" title="" :values="tableHeaders" />
		<div v-for="(indicator, index) in indicators" :key="index">
			<CompareTableRow class="mb-3" :title="indicator" :values="getValues(index)" />
			<hr v-if="index < indicators.length - 1"/>
		</div>
	</div>
</template>

<script>
import CompareTableRow from "./CompareTableRow.vue"

export default {
	components: {
		CompareTableRow
	},
	props: {
		symbols: {
			required: true,
			type: Array,
			validator(values) {
				let pass = true
				values.every(value => {
					if ("symbol" in value === false) {
						pass = false
					}

					if ("title" in value === false) {
						pass = false
					}

					if ("indicators" in value === false) {
						pass = false
					}
				})

				return pass
			}
		},
		indicators: {
			required: true,
			type: Array,
		}
	},
	computed: {
		showTable() {
			return this.symbols.length > 0
		},
		tableHeaders() {
			return this.symbols.map(symbol => symbol.symbol)
		}
	},
	methods: {
		getValues(index) {
			return this.symbols.map(symbol => symbol.indicators[index].fmt)
		}
	}
}
</script>
