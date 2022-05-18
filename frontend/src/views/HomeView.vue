<template>
  <main>
    <section class="slider">
      <random-recipe-slider />
    </section>
    <section class="recipes-week">
      <div class="container">
        <h2 class="section-title">Рецепты недели</h2>
        <week-recipe-list />
      </div>
    </section>
    <section class="feed">
      <div class="container">
        <h2 class="section-title">Подпишись на обновления</h2>
        <feed-form />
      </div>
    </section>
    <section class="popular-recipes">
      <div class="container">
        <h2 class="section-title">Популярные рецепты</h2>
        <popular-recipe-list />
      </div>
    </section>
    <section class="new-recipes">
      <div class="container">
        <h2 class="section-title">Новые рецепты</h2>
        <new-recipe-list />
      </div>
    </section>
  </main>
</template>

<script>
import PopularRecipeList from "@/components/PopularRecipeList";
import WeekRecipeList from "@/components/WeekRecipeList";
import NewRecipeList from "@/components/NewRecipeList";
import RandomRecipeSlider from "@/components/RandomRecipeSlider";
import FeedForm from "@/components/FeedForm";

export default {
  components: {
    RandomRecipeSlider,
    PopularRecipeList,
    FeedForm,
    WeekRecipeList,
    NewRecipeList,
  },
};
</script>

<style scoped>
/* title */

.section-title {
  font-weight: 700;
  font-size: 37.5px;
  line-height: 38.4px;
  color: #ff4e00;
}

/* title */

/* popular-recipes */

.popular-recipes {
  padding: 50px 0;
  background-color: #fff0f0;
}

/* popular-recipes */

/* new-recipes */

.new-recipes {
  padding: 50px 0;
  background-color: #f8f1fa;
}

/* new-recipes */

/* recipes-week */

.recipes-week {
  padding: 50px 0;
  background-color: #fff0f0;
}

/* recipes-week */

/* feed */

.feed {
  padding: 50px 0;
  background-color: #f8f1fa;
}

/* feed */
</style>
