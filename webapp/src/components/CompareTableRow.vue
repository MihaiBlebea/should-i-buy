<template>
	<div class="row justify-content-between">
		<div class="col-md-6">{{ title }}</div>
		<div class="col-md-6 d-flex justify-content-between flex-row-reverse">
			<div v-for="(value, index) in values" :key="index">{{ value }}</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		title: {
			type: String,
			required: true
		},
		values: {
			type: Array,
			required: false,
			default: [],
			validator(values) {
				return values.length <= 3
			}
		}
	}
}
</script>
