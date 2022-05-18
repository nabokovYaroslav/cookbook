<template>
  <main>
    <div class="container content">
      <div class="row">
        <div class="col-12 col-lg-8">
          <div class="category-content">
            <category-item :category="category" />
            <category-recipe-vertical-list
              class="category-recipe-vertical-list"
            />
          </div>
        </div>
        <div class="col-12 col-lg-4 additional">
          <popular-recipe-widget-list />
          <feed-form />
          <week-recipe-widget-list />
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { Category } from "@/api/category";
import CategoryItem from "@/components/CategoryItem";
import CategoryRecipeVerticalList from "@/components/CategoryRecipeVerticalList";
import PopularRecipeWidgetList from "@/components/PopularRecipeWidgetList";
import WeekRecipeWidgetList from "@/components/WeekRecipeWidgetList";
import FeedForm from "@/components/FeedForm";
export default {
  components: {
    CategoryItem,
    CategoryRecipeVerticalList,
    PopularRecipeWidgetList,
    FeedForm,
    WeekRecipeWidgetList,
  },
  data() {
    return {
      category: {},
    };
  },
  async created() {
    const response = await Category.detail(this.$route.params.id);
    this.category = response.data;
  },
};
</script>

<style scoped>
main {
  background-color: #f7f4e8;
}

.content {
  padding: 30px 30px 0 30px;
  box-shadow: 0 0 100px rgb(178 165 105 / 19%);
  background-color: #fff;
}

.category-content .category-recipe-vertical-list {
  margin-top: 24px;
}

.additional {
  display: none;
}

@media (min-width: 992px) {
  .additional {
    display: block;
  }
}
</style>
