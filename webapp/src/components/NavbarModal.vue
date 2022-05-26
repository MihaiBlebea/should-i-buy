<template>
    <div class="modal justify-content-start align-items-stretch p-4" v-bind:class="{'is-active': show}">
        <div class="modal-background"></div>

        <div class="row justify-content-center top mt-5">
            <div class="col-12 col-md-6 text-center">
        
                <h2 
                    class="menu-item pointer"
                    v-bind:class="{'menu-item-active': isActive(item)}"
                    v-on:click="navHandler(item)"
                    v-for="(item, index) in menu" 
                    :key="index"
                >
                    {{ item.title }}
                </h2>

            </div>
        </div>
        <button 
            class="modal-close is-large" 
            aria-label="close" 
            v-on:click="closeModalHandler"
        ></button>
    </div>
</template>

<script>

export default {
	props: {
        show: {
            type: Boolean,
            required: false,
            default: false
        },
        menu: {
            type: Array,
            required: true,
            validator(values) {
				let pass = true
				values.every(value => {
					if ("title" in value === false) {
						pass = false
					}

					if ("path" in value === false) {
						pass = false
					}
				})

				return pass
			}
        }
    },
    methods: {
        closeModalHandler() {
            this.$emit("close")
        },
        navHandler(navItem) {
            this.$emit("navigate", navItem.path)
            this.closeModalHandler()
        },
        isActive(navItem) {
            if (navItem.path === this.$route.path) {
                return true
            }
            return false
        }
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

.menu-item {
    border-radius: 6px;
    font-size: 1.25em;
    padding: 1em;
}

.menu-item-active {
    background-color: #00947e;
    color: #FFF;
}
</style>
