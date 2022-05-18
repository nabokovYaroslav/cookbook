<template>
  <div class="dropbox">
    <input
      type="file"
      :name="uploadFieldName"
      :disabled="isUploading"
      @change="fileChange($event.target.name, $event.target.files)"
      :accept="accept"
      class="input-file"
    />
    <p v-if="isInitial">
      Перетащите файл<br />
      или кликните, чтобы выбрать
    </p>
    <p v-if="isUploading">Загружаем файл...</p>
    <p v-if="isFailed">Недопустимый файл</p>
    <p v-if="isSuccess">Файл загружен</p>
  </div>
</template>

<script>
import { upload } from "@/utils/file-upload";

const STATUS_INITIAL = 0,
  STATUS_UPLOADING = 1,
  STATUS_SUCCESS = 3,
  STATUS_FAILED = 2;
export default {
  props: {
    accept: {
      type: String,
      default: "*",
    },
  },
  data() {
    return {
      uploadedFile: null,
      currentStatus: STATUS_INITIAL,
      uploadFieldName: "images",
    };
  },
  computed: {
    isInitial() {
      return this.currentStatus === STATUS_INITIAL;
    },
    isUploading() {
      return this.currentStatus === STATUS_UPLOADING;
    },
    isFailed() {
      return this.currentStatus === STATUS_FAILED;
    },
    isSuccess() {
      return this.currentStatus === STATUS_SUCCESS;
    },
  },
  methods: {
    async fileChange(fieldName, fileList) {
      const formData = new FormData();
      if (!fileList.length) return;

      formData.append(fieldName, fileList[0], fileList[0].name);

      this.currentStatus = STATUS_UPLOADING;

      const image = await upload(formData);
      if (image === undefined) {
        this.currentStatus = STATUS_FAILED;
        return;
      }
      this.uploadedFile = image;
      this.currentStatus = STATUS_SUCCESS;
      this.$emit("fileUploaded", this.uploadedFile);
    },
  },
};
</script>

<style scoped>
.dropbox {
  outline: 2px dashed grey; /* the dash box */
  outline-offset: -10px;
  background: lightcyan;
  color: dimgray;
  padding: 10px 10px;
  min-height: 200px; /* minimum height */
  position: relative;
  cursor: pointer;
  transition: 0.3s;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dropbox p {
  text-align: center;
}

.input-file {
  opacity: 0; /* invisible but it's there! */
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  position: absolute;
  cursor: pointer;
}

.dropbox:hover {
  background: lightblue; /* when mouse over to the drop zone, change color */
}
</style>
