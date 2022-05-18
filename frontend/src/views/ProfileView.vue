<template>
  <main>
    <div class="container">
      <div
        class="loader"
        style="display: flex; justify-content: center"
        v-if="
          (!maybeIsOwner && userIsLoading) || (maybeIsOwner && ownerIsLoading)
        "
      >
        <my-spinner :size="50" />
      </div>
      <div
        class="row profile-view"
        v-if="(!maybeIsOwner && !userIsLoading && user !== null) || isOwner"
      >
        <div class="col-lg-3 nav">
          <ul>
            <li>
              <router-link
                :to="{
                  name: 'profile',
                  params: { username: this.$route.params.username },
                }"
                >Профиль</router-link
              >
            </li>
            <li>
              <router-link
                :to="{
                  name: 'userRecipes',
                  params: { username: this.$route.params.username },
                }"
                >Рецепты</router-link
              >
            </li>
            <li v-if="isOwner">
              <router-link
                :to="{
                  name: 'userAddRecipe',
                  params: { username: this.$route.params.username },
                }"
                >Добавить рецепт</router-link
              >
            </li>
          </ul>
        </div>
        <div class="col-lg-9">
          <router-view
            :key="$route.path"
            :user="isOwner ? owner : user"
            :isOwner="isOwner"
          />
        </div>
      </div>
      <div
        class="not-found"
        v-if="!userIsLoading && user === null && !maybeIsOwner"
      >
        <h1>Пользователь {{ this.$route.params.username }} не найден</h1>
      </div>
    </div>
  </main>
</template>

<script>
import { User } from "@/api/user";
import { mapGetters } from "vuex";
import MySpinner from "@/components/MySpinner";
export default {
  components: {
    MySpinner,
  },
  data() {
    return {
      maybeIsOwner: true,
      ownerIsLoadingUnwatch: null,
      authenticatedUnwatch: null,
      userIsLoading: false,
      user: null,
    };
  },
  computed: {
    ...mapGetters("user", {
      ownerIsLoading: "userIsLoading",
      authenticated: "authenticated",
      owner: "user",
      hasAccessToken: "hasAccessToken",
      usernameFromToken: "usernameFromToken",
    }),
    isOwner() {
      if (!this.authenticated) return false;
      if (this.$route.params.username === this.owner.user_name) {
        return true;
      }
      return false;
    },
  },
  methods: {
    checkIsOwner() {
      if (
        this.owner !== null &&
        this.owner.user_name === this.$route.params.username
      ) {
        return true;
      }
      if (
        this.hasAccessToken() &&
        this.usernameFromToken() === this.$route.params.username
      ) {
        return true;
      } else {
        return false;
      }
    },
    loadUser() {
      this.userIsLoading = true;
      User.detail(this.$route.params.username)
        .then((user) => {
          this.user = user.data;
          this.userIsLoading = false;
        })
        .catch(() => {
          this.userIsLoading = false;
        });
    },
    ownerIsLoadingWatchHandler() {
      if (this.ownerIsLoading == false && !this.authenticated) {
        this.ownerIsLoadingUnwatch();
        this.maybeIsOwner = false;
        this.loadUser();
      } else if (this.ownerIsLoading == false && this.authenticated) {
        if (this.isOwner) {
          this.authenticatedUnwatch = this.$watch(
            "authenticated",
            this.authenticatedWatchHandler
          );
        }
      }
    },
    authenticatedWatchHandler() {
      if (!this.authenticated) {
        this.authenticatedUnwatch();
        this.maybeIsOwner = false;
        this.loadUser();
      }
    },
  },
  async created() {
    if (this.isOwner) {
      this.authenticatedUnwatch = this.$watch(
        "authenticated",
        this.authenticatedWatchHandler
      );
      return;
    }
    if (this.checkIsOwner()) {
      this.maybeIsOwner = true; // wait until ownerIsLoading
      this.ownerIsLoadingUnwatch = this.$watch(
        "ownerIsLoading",
        this.ownerIsLoadingWatchHandler
      );
    } else {
      this.maybeIsOwner = false;
      this.loadUser();
    }
  },
};
</script>

<style scoped>
main {
  padding: 50px 0;
}

main .not-found {
  display: flex;
  justify-content: center;
}

main .not-found h1 {
  font-size: 20px;
  text-align: center;
}

.profile-view {
  margin-top: -20px;
}

.profile-view > * {
  margin-top: 20px;
}

.nav {
  background-color: #35302d;
  padding: 0;
  align-self: flex-start;
}

.nav ul {
  display: flex;
  flex-direction: column;
}

.nav ul li {
  position: relative;
  overflow: hidden;
  border-bottom: solid 1px #3c3735;
}

.nav ul li a {
  display: block;
  position: relative;
  z-index: 1;
  transition: 0.35s ease color;
  padding: 1.1em 0;
  color: #dfdbd9;
  text-align: center;
}

.nav ul li a:hover {
  color: #fff;
}

.nav ul li a:hover::before {
  left: -5px;
}

.nav ul li a::before {
  content: "";
  display: block;
  z-index: -1;
  position: absolute;
  left: calc(-100% - 5px);
  top: 0;
  width: 100%;
  height: 100%;
  border-right: solid 5px #df4500;
  background: #3c3735;
  transition: 0.35s ease left;
}
</style>
