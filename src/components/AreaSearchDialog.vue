<template>
  <div class="area-search-form">
    <el-form
      :ref="area"
      :model="area"
      label-width="3em"
    >
      <h4>{{ area.sw.label }}</h4>
      <el-form-item label="纬度">
        <el-input v-model="area.sw.lat" placeholder="请输入纬度" />
      </el-form-item>
      <el-form-item label="经度">
        <el-input v-model="area.sw.lng" placeholder="请输入经度" />
      </el-form-item>
      <h4>{{ area.ne.label }}</h4>
      <el-form-item label="纬度">
        <el-input v-model="area.ne.lat" placeholder="请输入纬度" />
      </el-form-item>
      <el-form-item label="经度">
        <el-input v-model="area.ne.lng" placeholder="请输入经度" />
      </el-form-item>
      <el-form-item>
        <el-button @click="pickPoint">地图选点</el-button>
      </el-form-item>
    </el-form>
    <el-form>
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
import { mapState } from "vuex";
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
      area: {
        sw:{ label: "西南点", point: { lng: "", lat: "" } },
        ne:{ label: "东北点", point: { lng: "", lat: "" } },
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
  computed:{
    ...mapState(["map","markerLayer","markedPoint"]),
  },
  methods: {
    handleClose() {
      this.localVisible = false;
    },
    pickPoint() {
      if(!this.markerLayer){
        this.$store.commit("SET_MARKERLAYER",new TMap.MultiRectangle({
          map: this.map,
        }));
      }
      const editor = new TMap.tools.GeometryEditor({
        map: this.map, // 编辑器绑定的地图对象
        overlayList: [
          {
            overlay: this.markerLayer, // 要编辑的图层,
            id: 'rectangle',
          },
        ],
        actionMode: TMap.tools.constants.EDITOR_ACTION.DRAW, // 编辑器的工作模式
        activeOverlayId: 'rectangle', // 激活图层
        snappable: true, // 开启吸附
      });
      // 监听绘制结束事件，获取绘制几何图形
      editor.on('draw_complete', (geometry) => {
        // 判断当前处于编辑状态的图层id是否是overlayList中id为rectangle（矩形）图层
        var id = geometry.id;
        // 获取矩形顶点坐标
        var geo = this.markerLayer.geometries.filter(function (item) {
          return item.id === id;
        });
        // console.log('绘制的矩形定位的坐标：', geo[0].paths);
        this.area.ne.lat = geo[0].paths[1].lat;
        this.area.ne.lng = geo[0].paths[1].lng;
        this.area.sw.lat = geo[0].paths[3].lat;
        this.area.sw.lng = geo[0].paths[3].lng;
        this.$forceUpdate();
      });
      
      // this.$store.commit("setMarkerLayer", markerLayer);
      // this.$emit("pick-point", type);
    },
    clearAll() {
      this.area.forEach((point) => {
        point.lng = "";
        point.lat = "";
      });
    },
    saveTemp() {
      // 可扩展：暂存当前输入
      this.$message.success("已暂存");
    },
    confirm() {
  
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
    /* width: 30%; */
    padding-right: 20px;
  }
}
</style>
