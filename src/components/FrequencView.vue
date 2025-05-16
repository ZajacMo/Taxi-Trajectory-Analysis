<template>
  <div class="frequency-search-form">
    <div class="position-input">
      最小距离
      <el-input
        v-model="form.minDistance"
        placeholder="请输入最小距离"
      ></el-input>
    </div>
    <div class="position-input">
      路径数
      <el-input-number
        v-model="form.pathCount"
        :min="1"
        :precision="0"
      ></el-input-number>
    </div>
  </div>
</template>

<script>
export default {
  name: "FrequencView",
  data() {
    return {
      form: {
        minDistance: "",
        pathCount: 10,
      },
    };
  },
  methods: {
    clearForm() {
      this.form.minDistance = "";
      this.form.pathCount = 1;
    },
    confirmForm() {
      console.log("确认参数:", this.form);
      // 这里可以添加具体的业务逻辑
    },
  },
};
</script>

<style scoped>
div.el-input {
  width: 70%;
  margin: auto;
  display: block;
}
div.position-input {
  display: inline-flex;
  align-items: center;
  width: 50%;
}
.frequency-search-form {
  padding: 0px;
}
</style>
