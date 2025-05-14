<template>
  <div class="density-view">
    <el-form :model="form" label-width="5em">
      <el-form-item label="距离参数">
        <el-input v-model="form.r" placeholder="请输入距离参数r"></el-input>
      </el-form-item>
      <el-form-item label="时间段">
        <el-time-picker
          v-model="form.timeRange"
          is-range
          range-separator="至"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          size="medium"
        ></el-time-picker>
      </el-form-item>
      <el-form-item>
        <el-button @click="clearForm">清空</el-button>
        <el-button type="primary" @click="confirmForm">确认</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "DensityView",
  data() {
    return {
      form: {
        r: "",
        timeRange: [],
      },
    };
  },
  methods: {
    clearForm() {
      this.form.r = "";
      this.form.timeRange = [];
    },
    confirmForm() {
      console.log("确认参数:", this.form);
      // 这里可以添加具体的业务逻辑
    },
  },
};
</script>

<style scoped>
/* 可以在这里添加样式 */
.el-input {
  /* width: 30%; */
  padding-right: 20px;
}
.density-view {
  padding: 40px;
}
/* .el-date-editor.el-range-editor {
  width: 100px;
} */
</style>
