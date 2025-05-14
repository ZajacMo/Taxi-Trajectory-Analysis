<template>
  <div class="frequency-search-form">
    <el-form :model="form" label-width="5em">
      <el-form-item label="最小距离">
        <el-input
          v-model="form.minDistance"
          placeholder="请输入最小距离"
        ></el-input>
      </el-form-item>
      <el-form-item label="路径数">
        <el-input-number
          v-model="form.pathCount"
          :min="1"
          :precision="0"
        ></el-input-number>
      </el-form-item>
      <el-button @click="clearForm">清空</el-button>
      <el-button type="primary" @click="confirmForm">确认</el-button>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "FrequencView",
  data() {
    return {
      form: {
        minDistance: "",
        pathCount: 1,
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
.el-input {
  padding-right: 20px;
}
.frequency-search-form {
  padding: 40px;
}
</style>
