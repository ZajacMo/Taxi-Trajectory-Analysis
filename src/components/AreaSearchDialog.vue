<template>
  <div class="area-search-form">
    <el-form ref="form" :model="form" label-width="7em">
      <el-form-item label="西南点坐标">
        <el-input v-model="sw.lng" placeholder="经度" />
        <el-input v-model="sw.lat" placeholder="纬度" />
        <el-button @click="pickPoint('sw')">地图选点</el-button>
      </el-form-item>
      <el-form-item label="东北点坐标">
        <el-input v-model="ne.lng" placeholder="经度" />
        <el-input v-model="ne.lat" placeholder="纬度" />
        <el-button @click="pickPoint('ne')">地图选点</el-button>
      </el-form-item>
      <el-form-item label="时间段">
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          :picker-options="pickerOptions"
          align="right"
        />
      </el-form-item>
      <el-button type="danger" @click="clearAll">清空</el-button>
      <el-button @click="saveTemp">暂存</el-button>
      <el-button type="primary" @click="confirm">确认</el-button>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "AreaSearchDialog",
  props: {
    mode: {
      type: String,
      default: "input",
    },
    visible: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      localVisible: this.visible, // 本地弹窗显示状态，避免直接修改 props
      sw: { lng: "", lat: "" },
      ne: { lng: "", lat: "" },
      dateRange: [],
      pickerOptions: {
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", [new Date(), new Date()]);
            },
          },
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setDate(start.getDate() - 7);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
    };
  },
  created() {
    this.localVisible = this.visible;
  },
  watch: {
    // 监听父组件 visible 变化，同步到本地
    visible(val) {
      this.localVisible = val;
    },
    // 监听本地弹窗关闭，通知父组件
    localVisible(val) {
      if (!val) {
        this.$emit("close");
      }
    },
  },
  methods: {
    handleClose() {
      this.localVisible = false;
    },
    pickPoint(type) {
      // 触发地图组件进入选点模式，选中后回填经纬度
      this.$emit("pick-point", type);
    },
    clearAll() {
      this.sw = { lng: "", lat: "" };
      this.ne = { lng: "", lat: "" };
      this.dateRange = [];
    },
    saveTemp() {
      // 可扩展：暂存当前输入
      this.$message.success("已暂存");
    },
    confirm() {
      // 提交区域查找参数
      this.$emit("confirm", {
        sw: this.sw,
        ne: this.ne,
        dateRange: this.dateRange,
      });
      this.$emit("close");
    },
    setBox(sw, ne) {
      // 框选后自动填入
      this.sw = { ...sw };
      this.ne = { ...ne };
    },
  },
};
</script>

<style scoped>
.el-row + .el-row {
  margin-top: 8px;
}
.area-search-form {
  padding: 40px;
  .el-input {
    width: 30%;
    padding-right: 20px;
  }
}
</style>
