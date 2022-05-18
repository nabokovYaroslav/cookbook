<template>
  <user-recipe-list
    :wrapperClass="'col-12 col-sm-6'"
    :user="user"
    :isOwner="isOwner"
  />
</template>

<script>
import UserRecipeList from "@/components/UserRecipeList";
export default {
  components: {
    UserRecipeList,
  },
  props: {
    user: {
      type: Object,
      required: true,
    },
    isOwner: {
      type: Boolean,
      required: true,
    },
  },
};
</script>
