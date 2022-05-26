<template>
    <div>
        <nav class="navbar" role="navigation" aria-label="main navigation">
            <div class="navbar-brand">
                <a class="navbar-item" href="https://bulma.io">
                    <img
                        src="https://bulma.io/images/bulma-logo.png"
                        width="112"
                        height="28"
                    />
                </a>

                <div
                    role="button"
                    class="navbar-burger"
                    v-on:click="toggleModal"
                >
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </div>
            </div>
        </nav>
        <NavbarModal 
            :show="showModal"
            :menu="menuList"
            v-on:close="toggleModal"
            v-on:navigate="navigateTo"
        />
    </div>
</template>

<script>
import NavbarModal from "./NavbarModal.vue"

export default {
    components: {
        NavbarModal
    },
    data: () => {
        return {
            showModal: false,
            menuList: [
                {
                    title: "Home",
                    path: "/"
                },
                {
                    title: "Compare",
                    path: "/compare"
                }
            ]
        }
    },
    methods: {
        toggleModal() {
            this.showModal = !this.showModal
        },
        navigateTo(path) {
            this.$router.push(path)
        }
    }
}
</script>


<style scoped>
.navbar {
	all: initial;
}
</style>