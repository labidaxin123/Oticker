<template>
  <div class="alert" :class="{'alert-success':showAlert}" role="alert">
    {{ message }}
    <button type="button" class="close" @click="closeAlert">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
</template>



<script>
export default {
  props: ['message'],
  emits: ['close-alert'],

  data() {
    return {
      showAlert: true,

    };
  },
  methods: {
    closeAlert() {
      this.showAlert = false;
      this.$emit('close-alert');
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

