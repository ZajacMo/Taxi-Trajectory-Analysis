<template>
  <div class="association-view">
    <div style="margin-top: 20px; margin-bottom: 30px">
      <el-radio v-model="radio" label="1">单区域</el-radio>
      <el-radio v-model="radio" label="2">两区域</el-radio>
    </div>
    <div>
      <el-divider><h3 v-show="radio === '2'">区域1</h3></el-divider>
      <select-rectangle
        :key="1"
        @area-change="handleAreaChange"
      ></select-rectangle>
    </div>
    <div v-show="radio === '2'">
      <el-divider><h3>区域2</h3></el-divider>
      <select-rectangle
        :key="2"
        @area-change="handleAreaChange"
      ></select-rectangle>
    </div>
    <div style="padding-top: 20px">
      <el-button type="danger" @click="clearAll">清空</el-button>
      <el-button type="primary" @click="confirm">确认</el-button>
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";
import SelectRectangle from "@/components/SelectRectangle.vue";
export default {
  name: "AssociationView",
  components: {
    SelectRectangle,
  },
  computed: {
    ...mapState(["map"]),
  },
  data() {
    return {
      radio: "1",
    };
  },
  methods: {
    handleAreaChange(newVal) {
      console.log("area changed", newVal);
      // 在这里处理区域改变后的逻辑
    },
  },
};
</script>
<style>
.el-input {
  padding-right: 20px;
}
.association-view {
  padding: 40px;
  padding-top: 0;
}
</style>
