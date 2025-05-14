<template>
  <div class="area-search-form">
    <!-- <el-form :ref="area" :model="area" label-width="3em">
      <h4>{{ area.nw.label }}</h4>
      <el-form-item label="纬度" prop="lat">
        <el-input v-model="area.nw.point.lat" placeholder="请输入纬度" />
      </el-form-item>
      <el-form-item label="经度" prop="lng">
        <el-input v-model="area.nw.point.lng" placeholder="请输入经度" />
      </el-form-item>
      <h4>{{ area.se.label }}</h4>
      <el-form-item label="纬度" prop="lat">
        <el-input v-model="area.se.point.lat" placeholder="请输入纬度" />
      </el-form-item>
      <el-form-item label="经度" prop="lng">
        <el-input v-model="area.se.point.lng" placeholder="请输入经度" />
      </el-form-item>
      <el-button @click="pickPoint">地图选点</el-button>
    </el-form> -->
    <select-rectangle @area-changed="handleAreaChange"></select-rectangle>
    <el-form>
      <el-form-item label="时间段" prop="date">
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
      // console.log("area changed", area);
      this.area = area;
    },
    // pickPoint() {
    //   if (this.map.markerLayer) {
    //     this.$store.commit("RESET_STATISTICS");
    //   } else {
    //     this.$store.commit("SET_MAP", {
    //       mode: {
    //         draw: TMap.tools.constants.EDITOR_ACTION.DRAW, // 编辑器的工作模式
    //         interact: TMap.tools.constants.EDITOR_ACTION.INTERACT, // 进入编辑模式
    //       },
    //       markerLayer: new TMap.MultiRectangle({
    //         map: this.map.map,
    //       }),
    //     }),
    //       this.$store.commit("SET_MAP", {
    //         editor: new TMap.tools.GeometryEditor({
    //           map: this.map.map, // 编辑器绑定的地图对象
    //           overlayList: [
    //             {
    //               overlay: this.map.markerLayer, // 要编辑的图层,
    //               id: "rectangle",
    //               selectedStyle: "highlight", // 选中样式
    //             },
    //           ],
    //           actionMode: this.map.mode.draw, // 编辑器的工作模式
    //           activeOverlayId: "rectangle", // 激活图层
    //           selectable: true, // 开启选择
    //           snappable: true, // 开启吸附
    //         }),
    //       });
    //     // 监听绘制结束事件，获取绘制几何图形
    //     this.map.editor.on("draw_complete", (geometry) => {
    //       this.$store.commit("SET_MAP", { rectangleID: geometry.id });
    //       // 获取矩形顶点坐标
    //       var geo = this.map.markerLayer.geometries.filter(function (item) {
    //         return item.id === geometry.id;
    //       })[0];
    //       this.setBox(geo.paths[2], geo.paths[0]);
    //       this.map.editor.setActionMode(this.map.mode.interact); // 进入编辑模式
    //       // 需要完善编辑功能
    //     });
    //   }
    //   // this.$store.commit("setMarkerLayer", markerLayer);
    //   // this.$emit("pick-point", type);
    // },
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
    // setBox(nw = { lng: "", lat: "" }, se = { lng: "", lat: "" }) {
    //   // 框选后自动填入
    //   this.area.nw.point = { lng: nw.lng, lat: nw.lat };
    //   this.area.se.point = { lng: se.lng, lat: se.lat };
    //   this.$forceUpdate();
    // },
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
