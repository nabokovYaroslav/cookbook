<template>
  <div class="ingredients">
    <div class="ingredients-header">
      <div class="ingredients-title">Ингредиенты</div>
      <div class="ingredients-serves">
        Порции:
        <button class="dec" @click="decrementServesCounter">-</button>
        <input
          type="number"
          v-model.number="servesCounter"
          @input="onServesCounterInput"
        />
        <button class="inc" @click="incrementServesCounter">+</button>
      </div>
    </div>
    <div class="ingredients-info">
      <ul>
        <li v-for="ingredient in calculatedIngredients" :key="ingredient.id">
          <span>{{ ingredient.name }}</span>
          <span>{{ ingredient.value }} {{ ingredient.unit_short_name }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    ingredients: {
      type: Array,
      required: true,
    },
    serves: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      servesCounter: this.serves,
      maxServesCounter: 100,
      minServesCounter: 1,
    };
  },

  computed: {
    calculatedIngredients() {
      return this.ingredients.map((ingredient) => {
        const ingredientCopy = { ...ingredient };
        ingredientCopy.value = this.servesCounter * ingredient.value;
        return ingredientCopy;
      });
    },
  },

  methods: {
    incrementServesCounter() {
      if (this.servesCounter === this.maxServesCounter) {
        return;
      } else if (this.servesCounter + 1 > this.maxServesCounter) {
        this.servesCounter = this.maxServesCounter;
      } else {
        this.servesCounter += 1;
      }
    },
    decrementServesCounter() {
      if (this.servesCounter === this.minServesCounter) {
        return;
      } else if (this.servesCounter - 1 < this.minServesCounter) {
        this.servesCounter = this.minServesCounter;
      } else {
        this.servesCounter -= 1;
      }
    },
    onServesCounterInput() {
      if (this.servesCounter > this.maxServesCounter) {
        this.servesCounter = this.maxServesCounter;
      } else if (this.servesCounter < this.minServesCounter) {
        this.servesCounter = this.minServesCounter;
      }
    },
  },
};
</script>

<style scoped>
.ingredients {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.ingredients .ingredients-header {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 24px;
  margin-top: -10px;
}

.ingredients .ingredients-header .ingredients-title {
  padding-left: 40px;
  background: 0 2px url(@/assets/img/ingredient.svg) no-repeat;
  font-weight: 700;
  font-size: 18px;
  margin-right: 25px;
  margin-top: 10px;
}

.ingredients .ingredients-header .ingredients-serves {
  font-size: 14px;
  color: #666;
  margin-top: 10px;
}

.ingredients .ingredients-header .ingredients-serves .dec,
.ingredients .ingredients-header .ingredients-serves .inc {
  display: inline-flex;
  width: 28px;
  height: 28px;
  padding: 4px 0;
  background: #f3f3f3;
  font-size: 14px;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  line-height: 1.5;
  transition: 0.3s;
  border: none;
}

.ingredients .ingredients-header .ingredients-serves .dec:hover,
.ingredients .ingredients-header .ingredients-serves .inc:hover {
  background: #ff4e00;
  color: #fff;
}

.ingredients .ingredients-header .ingredients-serves input {
  width: 40px;
  height: 28px;
  padding-left: 0;
  padding-right: 0;
  text-align: center;
  border: none;
  font-weight: 700;
  box-shadow: 0 1px 0 #f3f3f3;
  outline: none;
  transition: 0.3s;
  font-size: 100%;
}

.ingredients
  .ingredients-header
  .ingredients-serves
  input::-webkit-outer-spin-button,
.ingredients
  .ingredients-header
  .ingredients-serves
  input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
  appearance: none;
}

.ingredients .ingredients-header .ingredients-serves input:focus {
  box-shadow: 0 1px 0 #ff4e00;
}

.ingredients .ingredients-info {
  padding-left: 40px;
  flex: 0 0 90%;
  max-width: 90%;
}

.ingredients .ingredients-info ul li {
  position: relative;
  display: flex;
  justify-content: space-between;
  padding: 3px 0;
}

.ingredients .ingredients-info ul li span:first-child {
  position: relative;
  padding: 2px 4px 2px 0;
  background: #fff;
  z-index: 2;
}

.ingredients .ingredients-info ul li span:last-child {
  position: relative;
  padding: 2px 0 2px 4px;
  background: #fff;
  z-index: 2;
}

.ingredients .ingredients-info ul li::after {
  content: "";
  position: absolute;
  bottom: 5px;
  width: 100%;
  border-bottom: 1px dotted #d6d6d6;
  z-index: 1;
}

@media (max-width: 767px) {
  .ingredients {
    display: block;
  }

  .ingredients .ingredients-info {
    max-width: none;
    flex: none;
    padding-left: 0;
  }
}
</style>
