<template>
  <div class="area-search-form">
    <el-divider><h3>区域</h3></el-divider>
    <select-rectangle @area-changed="handleAreaChange"></select-rectangle>
    <el-divider><h3>时间</h3></el-divider>
    <el-form>
      <el-form-item prop="date">
        <el-date-picker
        v-model="dateRange"
        type="datetimerange"
        start-placeholder="开始时间"
        end-placeholder="结束时间"
        :picker-options="pickerOptions"
        prop="date"
        align="right"
        />
      </el-form-item>
      <el-button type="danger" @click="clearAll">清空</el-button>
      <el-button type="primary" @click="confirm">确认</el-button>
    </el-form>
  </div>
</template>

<script>
import SelectRectangle from "@/components/SelectRectangle.vue";
import { mapState } from "vuex";
export default {
  name: "AreaSearchView",
  components: {
    SelectRectangle,
  },
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
      area: {
        nw: { label: "西北点", point: { lng: "", lat: "" } },
        se: { label: "东南点", point: { lng: "", lat: "" } },
      },
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
  computed: {
    ...mapState(["map", "markerLayer", "markedPoint"]),
  },
  methods: {
    handleClose() {
      this.localVisible = false;
    },
    handleAreaChange(area) {
      this.area = area;
    },
    clearAll() {
      this.setBox();
      this.dateRange = [];
      this.$store.commit("RESET_MARKERLAYER");
    },
    confirm() {
      if (
        this.area.nw.point.lng === "" ||
        this.area.nw.point.lat === "" ||
        this.area.se.point.lng === "" ||
        this.area.se.point.lat === ""
      ) {
        this.$message.error("请输入完整的区域信息");
        return;
      }
      if (!this.dateRange || this.dateRange.length === 0) {
        this.$message.error("请输入完整的时间信息");
        return;
      }
      // 转换时间格式
      var res = {
        startTime:
          this.dateRange[0].toISOString().split("T")[0] +
          " " +
          this.dateRange[0].toTimeString().split(" ")[0],
        endTime:
          this.dateRange[1].toISOString().split("T")[0] +
          " " +
          this.dateRange[1].toTimeString().split(" ")[0],
        ltPoint: [this.area.nw.point.lng, this.area.nw.point.lat],
        rbPoint: [this.area.se.point.lng, this.area.se.point.lat],
      };
      // console.log(res);
      // 向/api/query_region接口发送请求
      this.$http.post("/api/query_region", res).then((response) => {
        console.log(response.data);
        // this.$store.commit("SET_STATISTICS", response.data);
        this.handleClose();
      });
    },
  },
};
</script>

<style scoped>
.el-row + .el-row {
  margin-top: 8px;
}
.el-input {
  /* width: 30%; */
  padding-right: 20px;
}
.area-search-form {
  padding: 40px;
}
</style>
