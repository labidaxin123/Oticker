<template>
  <div v-if="showAlert" class="alert alert-success" role="alert">
    <span>{{ message }}</span>
    <button type="button" class="close" @click="closeAlert">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
</template>

<script>
export default {
  props: ['message'],
  data() {
    return {
      message: '',
      showAlert: true,
    };
  },
  methods: {
    closeAlert() {
      this.showAlert = false;
    },
  },
};
</script>

<style scoped>
.alert {
  padding: 20px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
}

.close:hover {
  color: #000;
}
</style>

