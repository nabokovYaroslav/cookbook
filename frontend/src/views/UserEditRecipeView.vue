<template>
  <div class="form">
    <div class="not-allowed" v-if="!authenticated">
      <h1>
        Вы не можете просматривать данную страницу, т.к. вы не авторизованы
      </h1>
    </div>
    <div class="not-allowed" v-if="authenticated && !isOwner">
      <h1>
        Вы не можете просматривать данную страницу т.к. вы не являетесь
        владельцом данного профиля
      </h1>
    </div>
    <div class="loader" v-if="recipeIsLoading">
      <my-spinner :size="50" />
    </div>
    <div class="empty" v-if="isOwner && !recipeIsLoading && !recipeFound">
      <h1>Рецепт не найден</h1>
    </div>
    <form
      @submit.prevent="onFormSubmit"
      v-if="isOwner && !recipeIsLoading && recipeFound"
    >
      <div class="main-error" :class="{ active: error.isVisible }">
        {{ error.message }}
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: name.error.isVisible }">{{
          name.error.message
        }}</span>
        <my-input
          placeholder="Название"
          v-model="name.value"
          @input="onNameInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: category.error.isVisible }">{{
          category.error.message
        }}</span>
        <my-select
          v-model="category.value"
          :disabled="categoriesIsLoading"
          @input="onCategoryInput"
        >
          <option
            value=""
            style="display: none"
            v-if="!categoriesIsLoading && category.value == ''"
          >
            Категория
          </option>
          <option value="" style="display: none" v-if="categoriesIsLoading">
            Идёт загрузка категорий...
          </option>
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
            :selected="category.value == category.id"
          >
            {{ category.name }}
          </option>
        </my-select>
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: description.error.isVisible }">{{
          description.error.message
        }}</span>
        <my-textarea
          rows="7"
          placeholder="Описание"
          v-model="description.value"
          @input="onDescriptionInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: time.error.isVisible }">{{
          time.error.message
        }}</span>
        <my-input
          placeholder="Время приготовления (в минутах)"
          type="number"
          v-model.number="time.value"
          @input.native="onTimeInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: colorie.error.isVisible }">{{
          colorie.error.message
        }}</span>
        <my-input
          placeholder="Калории на порцию"
          type="number"
          v-model.number="colorie.value"
          @input.native="onColorieInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: protein.error.isVisible }">{{
          protein.error.message
        }}</span>
        <my-input
          placeholder="Белки на порцию"
          type="number"
          v-model.number="protein.value"
          @input.native="onProteinInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: fat.error.isVisible }">{{
          fat.error.message
        }}</span>
        <my-input
          placeholder="Жиры на порцию"
          type="number"
          v-model.number="fat.value"
          @input.native="onFatInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: carbohydrate.error.isVisible }">{{
          carbohydrate.error.message
        }}</span>
        <my-input
          placeholder="Углеводы на порцию"
          type="number"
          v-model.number="carbohydrate.value"
          @input.native="onCarbohydrateInput"
        />
      </div>
      <div class="form-group">
        <span class="error" :class="{ active: count.error.isVisible }">{{
          count.error.message
        }}</span>
        <my-input
          placeholder="Расчитываемое кол-во порций"
          type="number"
          v-model.number="count.value"
          @input.native="onCountInput"
        />
      </div>
      <div class="form-group">
        <label>Изображение</label>
        <span class="error" :class="{ active: image.error.isVisible }">{{
          image.error.message
        }}</span>
        <file-uploader
          @fileUploaded="fileUploaded"
          v-if="!image.value"
          style="margin-top: 5px"
          :accept="'image/*'"
        />
        <div class="image" v-else>
          <img
            :src="image.value"
            alt="image"
            style="max-width: 100%; max-height: 200px"
          />
          <my-button
            type="button"
            style="margin-top: 15px"
            @click.native="fileUploaded('')"
            >Выбрать другое изображение</my-button
          >
        </div>
      </div>
      <div class="ingredients-wrapper">
        <span>Ингредиенты</span>
        <div class="empty" v-if="ingredients.length === 0">
          Пока нет ни одного ингредиента
        </div>
        <div class="ingredients">
          <div
            class="ingredient"
            v-for="(ingredient, index) in ingredients"
            :key="index"
          >
            <div class="form-group">
              <span
                class="error"
                :class="{ active: ingredient.name.error.isVisible }"
                >{{ ingredient.name.error.message }}</span
              >
              <my-input
                placeholder="Название ингредиента"
                v-model="ingredient.name.value"
                @input="onIngredientNameInput(index)"
              />
            </div>
            <div class="form-group">
              <span
                class="error"
                :class="{ active: ingredient.unit.error.isVisible }"
                >{{ ingredient.unit.error.message }}</span
              >
              <my-select
                v-model="ingredient.unit.value"
                @input="onIngredientUnitInput(index)"
                :disabled="unitsIsLoading"
              >
                <option
                  value=""
                  style="display: none"
                  v-if="!unitsIsLoading && ingredient.unit.value == ''"
                >
                  Единица измерения
                </option>
                <option value="" style="display: none" v-if="unitsIsLoading">
                  Идёт загрузка единиц измерений...
                </option>
                <option v-for="unit in units" :key="unit.id" :value="unit.id">
                  {{ unit.name }}
                </option>
              </my-select>
            </div>
            <div class="form-group">
              <span
                class="error"
                :class="{ active: ingredient.value.error.isVisible }"
                >{{ ingredient.value.error.message }}</span
              >
              <my-input
                placeholder="Значение"
                type="number"
                step="0.1"
                v-model="ingredient.value.value"
                @input="onIngredientValueInput(index)"
                @change="onIngredientValueChange(index)"
              />
            </div>
            <my-button
              class="remove"
              type="button"
              @click.native="removeIngredient(index)"
              >Удалить</my-button
            >
          </div>
          <my-button class="add" type="button" @click.native="addIngredient"
            >Добавить</my-button
          >
        </div>
      </div>
      <div class="steps-wrapper">
        <span>Шаги</span>
        <div class="empty" v-if="steps.length === 0">
          Пока нет ни одного шага
        </div>
        <div class="steps">
          <div class="step" v-for="(step, index) in steps" :key="index">
            <div class="form-group">
              <label>Изображение</label>
              <span
                class="error"
                :class="{ active: step.image.error.isVisible }"
                >{{ step.image.error.message }}</span
              >
              <file-uploader
                @fileUploaded="stepFileUploaded($event, index)"
                v-if="!step.image.value"
                style="margin-top: 5px"
                :accept="'image/*'"
              />
              <div class="image" v-else>
                <img
                  :src="step.image.value"
                  alt="image"
                  style="max-width: 100%; max-height: 200px"
                />
                <my-button
                  type="button"
                  style="margin-top: 15px"
                  @click.native="stepFileUploaded('', index)"
                  >Выбрать другое изображение</my-button
                >
              </div>
            </div>
            <div class="form-group">
              <span
                class="error"
                :class="{ active: step.description.error.isVisible }"
                >{{ step.description.error.message }}</span
              >
              <my-textarea
                rows="7"
                placeholder="Описание шага"
                v-model="step.description.value"
                @input="onStepDescriptionInput(index)"
              />
            </div>
            <my-button
              class="remove"
              type="button"
              @click.native="removeStep(index)"
              >Удалить</my-button
            >
          </div>
          <my-button class="add" type="button" @click.native="addStep"
            >Добавить</my-button
          >
        </div>
        <div class="form-group">
          <span class="error" :class="{ active: result.error.isVisible }">{{
            result.error.message
          }}</span>
          <my-textarea
            rows="7"
            placeholder="Вывод"
            v-model="result.value"
            @input="onResultInput"
          />
        </div>
      </div>
      <div class="loader" v-if="formSubmitting">
        <my-spinner :size="40" />
      </div>
      <my-button type="submit" v-else :disabled="!formIsValid"
        >Изменить рецепт</my-button
      >
    </form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import { Recipe } from "@/api/recipe";
import { Unit } from "@/api/unit";
import { Category } from "@/api/category";
import MySpinner from "@/components/MySpinner";
import MyInput from "@/components/UI/MyInput";
import MyButton from "@/components/UI/MyButton";
import MyTextarea from "@/components/UI/MyTextarea";
import MySelect from "@/components/UI/MySelect";
import FileUploader from "@/components/FileUploader";
export default {
  components: {
    MyInput,
    MyTextarea,
    MyButton,
    FileUploader,
    MySelect,
    MySpinner,
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
  data() {
    return {
      recipeIsLoading: false,
      recipeFound: false,
      error: {
        isVisible: false,
        message: "",
      },
      formSubmitting: false,
      categories: null,
      categoriesIsLoading: false,
      units: null,
      unitsIsLoading: false,
      name: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      category: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      description: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      time: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      colorie: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      protein: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      fat: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      carbohydrate: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      count: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      image: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
      ingredients: [],
      steps: [],
      result: {
        value: "",
        error: {
          isVisible: false,
          message: "",
        },
        valid: true,
      },
    };
  },
  methods: {
    ...mapActions("user", {
      logout: "logout",
    }),
    fileUploaded(url) {
      this.error.isVisible = false;
      this.image.value = url;
      if (this.image.value === "") {
        this.image.valid = false;
        this.image.error.message = "Обязательное поле";
        this.image.error.isVisible = true;
        return;
      }
      this.image.valid = true;
      this.image.error.message = "";
      this.image.error.isVisible = false;
    },
    stepFileUploaded(url, stepIndex) {
      this.error.isVisible = false;
      this.steps[stepIndex].image.value = url;
      if (this.steps[stepIndex].image.value === "") {
        this.steps[stepIndex].image.valid = false;
        this.steps[stepIndex].image.error.message = "Обязательное поле";
        this.steps[stepIndex].image.error.isVisible = true;
        return;
      }
      this.steps[stepIndex].image.valid = true;
      this.steps[stepIndex].image.error.message = "";
      this.steps[stepIndex].image.error.isVisible = false;
    },
    addIngredient() {
      this.ingredients.push({
        id: {
          value: null,
        },
        name: {
          value: "",
          error: {
            isVisible: false,
            message: "",
          },
          valid: false,
        },
        unit: {
          value: "",
          error: {
            isVisible: false,
            message: "",
          },
          valid: false,
        },
        value: {
          value: "",
          error: {
            isVisible: false,
            message: "",
          },
          valid: false,
        },
      });
    },
    removeIngredient(index) {
      this.ingredients.splice(index, 1);
    },
    addStep() {
      this.steps.push({
        id: {
          value: null,
        },
        image: {
          value: "",
          error: {
            isVisible: false,
            message: "",
          },
          valid: false,
        },
        description: {
          value: "",
          error: {
            isVisible: false,
            message: "",
          },
          valid: true,
        },
      });
    },
    removeStep(index) {
      this.steps.splice(index, 1);
    },
    onNameInput() {
      this.error.isVisible = false;
      if (this.name.value.length == 0) {
        this.name.valid = false;
        this.name.error.message = "Обязательное поле";
        this.name.error.isVisible = true;
        return;
      }
      if (this.name.value.length > 255) {
        this.name.valid = false;
        this.name.error.message = "Название не может быть больше 255 символов";
        this.name.error.isVisible = true;
        return;
      }
      this.name.valid = true;
      this.name.error.message = "";
      this.name.error.isVisible = false;
    },
    onCategoryInput() {
      this.error.isVisible = false;
      if (this.category.value === "") {
        this.category.valid = false;
        this.category.error.message = "Обязательное поле";
        this.category.error.isVisible = true;
        return;
      }
      this.category.valid = true;
      this.category.error.message = "";
      this.category.error.isVisible = false;
    },
    onDescriptionInput() {
      this.category.valid = true;
      this.category.error.message = "";
      this.category.error.isVisible = false;
    },
    onTimeInput() {
      this.error.isVisible = false;
      if (this.time.value === "") {
        this.time.valid = false;
        this.time.error.message = "Обязательное поле";
        this.time.error.isVisible = true;
        return;
      }
      if (this.time.value > 2147483647) {
        this.time.value = 2147483647;
      } else if (this.time.value < 0) {
        this.time.value = 0;
      }
      this.time.valid = true;
      this.time.error.message = "";
      this.time.error.isVisible = false;
    },
    onColorieInput() {
      this.error.isVisible = false;
      if (this.colorie.value === "") {
        this.colorie.valid = false;
        this.colorie.error.message = "Обязательное поле";
        this.colorie.error.isVisible = true;
        return;
      }
      if (this.colorie.value > 2147483647) {
        this.colorie.value = 2147483647;
      } else if (this.colorie.value < 0) {
        this.colorie.value = 0;
      }
      this.colorie.valid = true;
      this.colorie.error.message = "";
      this.colorie.error.isVisible = false;
    },
    onProteinInput() {
      this.error.isVisible = false;
      if (this.protein.value === "") {
        this.protein.valid = false;
        this.protein.error.message = "Обязательное поле";
        this.protein.error.isVisible = true;
        return;
      }
      if (this.protein.value > 2147483647) {
        this.protein.value = 2147483647;
      } else if (this.protein.value < 0) {
        this.protein.value = 0;
      }
      this.protein.valid = true;
      this.protein.error.message = "";
      this.protein.error.isVisible = false;
    },
    onFatInput() {
      this.error.isVisible = false;
      if (this.fat.value === "") {
        this.fat.valid = false;
        this.fat.error.message = "Обязательное поле";
        this.fat.error.isVisible = true;
        return;
      }
      if (this.fat.value > 2147483647) {
        this.fat.value = 2147483647;
      } else if (this.fat.value < 0) {
        this.fat.value = 0;
      }
      this.fat.valid = true;
      this.fat.error.message = "";
      this.fat.error.isVisible = false;
    },
    onCarbohydrateInput() {
      this.error.isVisible = false;
      if (this.carbohydrate.value === "") {
        this.carbohydrate.valid = false;
        this.carbohydrate.error.message = "Обязательное поле";
        this.carbohydrate.error.isVisible = true;
        return;
      }
      if (this.carbohydrate.value > 2147483647) {
        this.carbohydrate.value = 2147483647;
      } else if (this.carbohydrate.value < 0) {
        this.carbohydrate.value = 0;
      }
      if (this.carbohydrate.value < 0) {
        this.carbohydrate.valid = false;
        this.carbohydrate.error.message = "Значение должно быть больше 0";
        this.carbohydrate.error.isVisible = true;
        return;
      }
      this.carbohydrate.valid = true;
      this.carbohydrate.error.message = "";
      this.carbohydrate.error.isVisible = false;
    },
    onCountInput() {
      if (this.count.value === "") {
        this.count.valid = false;
        this.count.error.message = "Обязательное поле";
        this.count.error.isVisible = true;
        return;
      }

      if (this.count.value > 32767) {
        this.count.value = 32767;
      } else if (this.count.value < 1) {
        this.count.value = 1;
      }
      this.count.valid = true;
      this.count.error.message = "";
      this.count.error.isVisible = false;
    },
    onIngredientNameInput(index) {
      this.error.isVisible = false;
      if (this.ingredients[index].name.value.length == 0) {
        this.ingredients[index].name.valid = false;
        this.ingredients[index].name.error.message = "Обязательное поле";
        this.ingredients[index].name.error.isVisible = true;
        return;
      }
      if (this.ingredients[index].name.value.length > 255) {
        this.ingredients[index].name.valid = false;
        this.ingredients[index].name.error.message =
          "Название не может быть больше 255 символов";
        this.ingredients[index].name.error.isVisible = true;
        return;
      }
      this.ingredients[index].name.valid = true;
      this.ingredients[index].name.error.message = "";
      this.ingredients[index].name.error.isVisible = false;
    },
    onIngredientUnitInput(index) {
      this.error.isVisible = false;
      if (this.ingredients[index].unit.value === "") {
        this.ingredients[index].unit.valid = false;
        this.ingredients[index].unit.error.message = "Обязательное поле";
        this.ingredients[index].unit.error.isVisible = true;
        return;
      }
      this.ingredients[index].unit.valid = true;
      this.ingredients[index].unit.error.message = "";
      this.ingredients[index].unit.error.isVisible = false;
    },
    onIngredientValueInput(index) {
      this.error.isVisible = false;
      if (this.ingredients[index].value.value === "") {
        this.ingredients[index].value.valid = false;
        this.ingredients[index].value.error.message = "Обязательное поле";
        this.ingredients[index].value.error.isVisible = true;
        return;
      }
      const integerPart = Math.trunc(this.ingredients[index].value.value);
      if (String(integerPart).length > 6) {
        this.ingredients[index].value.valid = false;
        this.ingredients[index].value.error.message =
          "Целая часть не может быть больше 6 знаков";
        this.ingredients[index].value.error.isVisible = true;
        return;
      }
      this.ingredients[index].value.valid = true;
      this.ingredients[index].value.error.message = "";
      this.ingredients[index].value.error.isVisible = false;
    },
    onIngredientValueChange(index) {
      if (this.ingredients[index].value.value === "") return;
      this.ingredients[index].value.value = +Number(
        this.ingredients[index].value.value
      ).toFixed(1);
    },
    onStepDescriptionInput(index) {
      this.steps[index].description.valid = true;
      this.steps[index].description.error.message = "";
      this.steps[index].description.error.isVisible = false;
    },
    onResultInput() {
      this.result.valid = true;
      this.result.error.message = "";
      this.result.error.isVisible = false;
    },
    async onFormSubmit() {
      try {
        this.formSubmitting = true;
        await Recipe.update(
          this.$route.params.recipeId,
          this.name.value,
          this.category.value,
          this.description.value,
          this.time.value,
          this.colorie.value,
          this.protein.value,
          this.fat.value,
          this.carbohydrate.value,
          this.count.value,
          this.image.value,
          this.ingredients.map((ingredient) => {
            return {
              id: ingredient.id.value,
              name: ingredient.name.value,
              unit: ingredient.unit.value,
              value: ingredient.value.value,
            };
          }),
          this.steps.map((step) => {
            return {
              id: step.id.value,
              image: step.image.value,
              description: step.description.value,
            };
          }),
          this.result.value,
          this.user.user
        );
        this.$router.push({
          name: "userRecipes",
          params: { username: this.$route.params.username },
        });
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status === 401) {
            await this.logout();
          } else if (status === 400) {
            if (response.data.name) {
              this.name.valid = false;
              this.name.error.message = response.data.user_name.join("\n");
              this.name.error.isVisible = true;
            }
            if (response.data.category) {
              this.category.valid = false;
              this.category.error.message = response.data.email.join("\n");
              this.category.error.isVisible = true;
            }
            if (response.data.description) {
              this.description.valid = false;
              this.description.error.message =
                response.data.password.join("\n");
              this.description.error.isVisible = true;
            }
            if (response.data.time) {
              this.time.valid = false;
              this.time.error.message = response.data.password.join("\n");
              this.time.error.isVisible = true;
            }
            if (response.data.colorie) {
              this.colorie.valid = false;
              this.colorie.error.message = response.data.password.join("\n");
              this.colorie.error.isVisible = true;
            }
            if (response.data.protein) {
              this.protein.valid = false;
              this.protein.error.message = response.data.password.join("\n");
              this.protein.error.isVisible = true;
            }
            if (response.data.fat) {
              this.fat.valid = false;
              this.fat.error.message = response.data.password.join("\n");
              this.fat.error.isVisible = true;
            }
            if (response.data.carbohydrate) {
              this.carbohydrate.valid = false;
              this.carbohydrate.error.message =
                response.data.password.join("\n");
              this.carbohydrate.error.isVisible = true;
            }
            if (response.data.count) {
              this.count.valid = false;
              this.count.error.message = response.data.password.join("\n");
              this.count.error.isVisible = true;
            }
            if (response.data.image) {
              this.image.valid = false;
              this.image.error.message = response.data.password.join("\n");
              this.image.error.isVisible = true;
            }
            if (response.data.ingredients) {
              for (let i = 0; i < response.data.ingredients.length; i++) {
                if (response.data.ingredients[i].name) {
                  this.ingredients[i].name.valid = false;
                  this.ingredients[i].name.error.message =
                    response.data.ingredients[i].name.join("\n");
                  this.ingredients[i].name.error.isVisible = true;
                }
                if (response.data.ingredients[i].unit) {
                  this.ingredients[i].unit.valid = false;
                  this.ingredients[i].unit.error.message =
                    response.data.ingredients[i].unit.join("\n");
                  this.ingredients[i].unit.error.isVisible = true;
                }
                if (response.data.ingredients[i].value) {
                  this.ingredients[i].value.valid = false;
                  this.ingredients[i].value.error.message =
                    response.data.ingredients[i].value.join("\n");
                  this.ingredients[i].value.error.isVisible = true;
                }
              }
            }
            if (response.data.steps) {
              for (let i = 0; i < response.data.steps.length; i++) {
                if (response.data.steps[i].image) {
                  this.steps[i].image.valid = false;
                  this.steps[i].image.error.message =
                    response.data.ingredients[i].image.join("\n");
                  this.steps[i].image.error.isVisible = true;
                }
                if (response.data.steps[i].description) {
                  this.steps[i].description.valid = false;
                  this.steps[i].description.error.message =
                    response.data.ingredients[i].description.join("\n");
                  this.steps[i].description.error.isVisible = true;
                }
              }
            }
            if (response.data.result) {
              this.image.valid = false;
              this.image.error.message = response.data.password.join("\n");
              this.image.error.isVisible = true;
            }
            this.error.message = "Исправьте ошибки ниже";
            this.error.isVisible = true;
          } else if (status === 500) {
            this.error.message =
              "Ошибка на сервере, пожалуйста, попробуйте еще раз, если ошибка повторится, сообщите администратору";
            this.error.isVisible = true;
          } else {
            this.error.message =
              "Непредвиденная ошибка, пожалуйста, сообщите администратору";
            this.error.isVisible = true;
          }
        } else {
          this.error.message =
            "Неизвестная ошибка, пожалуйста, сообщите администратору";
        }
      } finally {
        this.formSubmitting = false;
      }
    },
    loadUnitsAndCategories() {
      this.categoriesIsLoading = true;
      Category.list()
        .then((categories) => {
          this.categories = categories.data;
          this.categoriesIsLoading = false;
        })
        .catch(() => {
          this.categoriesIsLoading = false;
        });

      this.unitsIsLoading = true;
      Unit.list()
        .then((units) => {
          this.units = units.data;
          this.unitsIsLoading = false;
        })
        .catch(() => {
          this.unitsIsLoading = false;
        });
    },
  },
  computed: {
    formIsValid() {
      return (
        this.name.valid &&
        this.category.valid &&
        this.description.valid &&
        this.time.valid &&
        this.colorie.valid &&
        this.protein.valid &&
        this.fat.value &&
        this.carbohydrate.value &&
        this.count.valid &&
        this.image.valid &&
        this.ingredients.filter((ingredient) => {
          return !(
            ingredient.name.valid &&
            ingredient.unit.valid &&
            ingredient.value.valid
          );
        }).length == 0 &&
        this.steps.filter((step) => {
          return !(step.image.valid && step.image.valid);
        }).length == 0 &&
        this.result.valid
      );
    },
    ...mapGetters("user", {
      authenticated: "authenticated",
    }),
  },
  async created() {
    if (this.isOwner) {
      try {
        this.recipeIsLoading = true;
        const response = await Recipe.edit(this.$route.params.recipeId);
        this.recipeFound = true;
        const recipe = response.data;
        this.name.value = recipe.name;
        this.category.value = recipe.category;
        this.description.value = recipe.description;
        this.time.value = recipe.time;
        this.colorie.value = recipe.colorie;
        this.protein.value = recipe.protein;
        this.fat.value = recipe.fat;
        this.carbohydrate.value = recipe.carbohydrate;
        this.count.value = recipe.count;
        this.image.value = recipe.image;
        recipe.ingredients.forEach((ingredient) => {
          this.ingredients.push({
            id: {
              value: ingredient.id,
            },
            name: {
              value: ingredient.name,
              error: {
                isVisible: false,
                message: "",
              },
              valid: true,
            },
            unit: {
              value: ingredient.unit,
              error: {
                isVisible: false,
                message: "",
              },
              valid: true,
            },
            value: {
              value: ingredient.value,
              error: {
                isVisible: false,
                message: "",
              },
              valid: true,
            },
          });
        });
        recipe.steps.forEach((step) => {
          this.steps.push({
            id: {
              value: step.id,
            },
            image: {
              value: step.image,
              error: {
                isVisible: false,
                message: "",
              },
              valid: true,
            },
            description: {
              value: step.description,
              error: {
                isVisible: false,
                message: "",
              },
              valid: true,
            },
          });
        });
        this.result.value = recipe.result;
        this.loadUnitsAndCategories();
      } catch (error) {
        if (error.response) {
          const response = error.response;
          const status = response.status;
          if (status == 401 || status == 403) {
            await this.logout();
          } else if (status == 404) {
            this.recipeFound = false;
          }
        }
      } finally {
        this.recipeIsLoading = false;
      }
    }
  },
};
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
}

.form .empty {
  padding: 50px 0;
  text-align: center;
  font-size: 20px;
  border: 2px dashed grey;
  margin-top: 10px;
}

.form > .loader {
  display: flex;
  justify-content: center;
  padding: 50px 0;
}

.form .not-allowed {
  padding: 50px 0;
}

.form .not-allowed h1 {
  font-size: 20px;
  text-align: center;
}

.form img {
  display: block;
}

.form form .loader {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}

.form {
  display: flex;
  flex-direction: column;
}

.form form .form-group {
  display: flex;
  flex-direction: column;
}

.form form {
  margin-top: -15px;
}

.form form .ingredients {
  display: flex;
  flex-direction: column;
  justify-content: unset;
  margin-top: 10px;
}

.form form .ingredients .ingredient {
  display: flex;
  flex-direction: column;
  padding: 15px;
  border: 2px dashed grey;
  margin-top: 10px;
}

.form form .ingredients .add {
  align-self: flex-end;
  margin-top: 20px;
}

.form form .ingredients .ingredient .remove {
  margin-top: 15px;
  align-self: flex-end;
}

.form form .steps {
  display: flex;
  flex-direction: column;
  justify-content: unset;
  margin-top: 10px;
}

.form form .steps .step {
  display: flex;
  flex-direction: column;
  padding: 15px;
  border: 2px dashed grey;
  margin-top: 10px;
}

.form form .steps .add {
  align-self: flex-end;
  margin-top: 20px;
}

.form form .steps .step .remove {
  margin-top: 15px;
  align-self: flex-end;
}

.form .main-error {
  width: 100%;
  text-align: center;
  color: #fff;
  padding: 15px 15px;
  background-color: rgb(255 0 0 / 80%);
  display: none;
}

.form .main-error.active {
  display: block;
}

.form form .form-group {
  width: 100%;
  margin-top: 15px;
}

.form form .form-group .error {
  font-size: 14px;
  color: red;
  display: none;
}

.form form .form-group .error.active {
  display: block;
}

.form form .form-group input {
  margin-top: 5px;
}

.form form button[type="submit"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form form button[type="submit"] {
  width: 100%;
  margin-top: 15px;
}

.form form .steps-wrapper,
.form form .ingredients-wrapper {
  margin-top: 15px;
}
</style>
