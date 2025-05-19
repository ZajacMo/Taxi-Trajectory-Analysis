<template>
  <div class="frequency-search-form">
    <div class="position-input" v-show="selected.radio === '单区域'">
      最小距离
      <el-input v-model="form.minDistance" placeholder="请输入最小距离"
        ><template slot="append">千米</template>
      </el-input>
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
  name: "FrequenceView",
  props: {
    selected: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        minDistance: "",
        pathCount: 10,
      },
    };
  },
  watch: {
    form: {
      handler(newVal) {
        // console.log("area changed", newVal);
        this.$emit("frequence-changed", newVal);
        // 可以在这里添加一些逻辑
      },
      deep: true,
    },
  },
  methods: {
    clearForm() {
      this.form.minDistance = "";
      this.form.pathCount = 10;
    },
  },
};
</script>

<style scoped>
div.position-input {
  div.el-input {
    width: 70%;
    margin-left: auto;
    /* display: block; */
  }

  div.el-input-number {
    width: 70%;
    margin-left: auto;
    display: block;
  }
  margin-top: 10px;
  display: inline-flex;
  align-items: center;
  width: 100%;
}
.frequency-search-form {
  padding: 0px;
}
</style>
