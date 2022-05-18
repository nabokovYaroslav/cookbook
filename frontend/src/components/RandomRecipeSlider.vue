<template>
  <swiper class="swiper" :options="swiperOption">
    <swiper-slide v-for="recipe in recipes" :key="recipe.id">
      <router-link
        :to="{
          name: 'recipe',
          params: { category_id: recipe.category, id: recipe.id },
        }"
        class="slide"
        :style="{ 'background-image': 'url(' + recipe.image + ')' }"
      >
        <div class="content">
          <router-link
            :to="{ name: 'category', params: { id: recipe.id } }"
            class="category"
            >{{ recipe.category_name }}</router-link
          >
          <div class="title">{{ recipe.name }}</div>
          <div class="description">{{ recipe.description }}</div>
        </div>
      </router-link>
    </swiper-slide>
    <div class="swiper-pagination" slot="pagination"></div>
    <div class="swiper-button-prev" slot="button-prev"></div>
    <div class="swiper-button-next" slot="button-next"></div>
  </swiper>
</template>

<script>
import { Swiper, SwiperSlide } from "vue-awesome-swiper";
import "swiper/css/swiper.css";
import { Recipe } from "@/api/recipe";
export default {
  components: {
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      swiperOption: {
        slidesPerView: 1,
        loop: false,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
      recipes: [],
    };
  },
  async created() {
    const response = await Recipe.random_recipes();
    this.recipes = response.data;
  },
};
</script>

<style>
/* slider */

.slide {
  height: 100%;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  display: block;
}

.slide .content {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  color: #fff;
  background-image: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.8));
  padding: 6% 10% 10%;
  display: flex;
  flex-direction: column;
}

.slide .content .category {
  display: inline-block;
  padding: 0.3em 1.4em;
  background: #ff4e00;
  color: #fff;
  border-radius: 3px;
  text-decoration: none;
  font-size: 0.7em;
  width: fit-content;
}

.slide .content .title {
  margin-top: 11px;
  font-size: 1.8em;
  line-height: 1.3;
  font-weight: 700;
}

.slide .content .description {
  font-size: 0.95em;
  opacity: 0.75;
  margin-top: 8px;
}

.swiper {
  height: 400px;
}

.swiper-button-next {
  right: 20px;
}

.swiper-button-prev {
  left: 20px;
}

.swiper-button-next,
.swiper-button-prev {
  color: #fff;
  opacity: 0.3;
  transition: 0.3s;
}

.swiper-button-next:hover,
.swiper-button-prev:hover {
  opacity: 1;
}

.swiper-pagination .swiper-pagination-bullet {
  background-color: #fff;
  transition: 0.3s;
  opacity: 0.2;
}

.swiper-pagination .swiper-pagination-bullet.swiper-pagination-bullet-active {
  background-color: #ff4e00;
  opacity: 1;
}

@media (min-width: 768px) {
  .slide .content {
    padding: 11% 10% 6%;
  }
}

/* slider */
</style>
