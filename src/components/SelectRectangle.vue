<template>
  <el-form :ref="area" :model="area" label-width="3em">
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
  </el-form>
</template>
<script>
import { mapState } from "vuex";
export default {
  name: "SelectRectangle",
  data() {
    return {
        area: {
            nw: { label: "西北点", point: { lng: "", lat: "" } },
            se: { label: "东南点", point: { lng: "", lat: "" } },
        },
    };
  },
  computed: {
    ...mapState(["map"]),
  },
  watch: {
    area: {
      handler(newVal) {
        // console.log("area changed", newVal, oldVal);
        this.$emit("area-changed", newVal);
        // 可以在这里添加一些逻辑
      },
      deep: true, // 深度监听
    },
  },
  methods: {
    pickPoint() {
      if (this.map.markerLayer) {
        this.$store.commit("RESET_MARKERLAYER");
      } else {
        this.$store.commit("SET_MAP", {
          mode: {
            draw: TMap.tools.constants.EDITOR_ACTION.DRAW, // 编辑器的工作模式
            interact: TMap.tools.constants.EDITOR_ACTION.INTERACT, // 进入编辑模式
          },
          markerLayer: new TMap.MultiRectangle({
            map: this.map.map,
          }),
        }),
          this.$store.commit("SET_MAP", {
            editor: new TMap.tools.GeometryEditor({
              map: this.map.map, // 编辑器绑定的地图对象
              overlayList: [
                {
                  overlay: this.map.markerLayer, // 要编辑的图层,
                  id: "rectangle",
                  selectedStyle: "highlight", // 选中样式
                },
              ],
              actionMode: this.map.mode.draw, // 编辑器的工作模式
              activeOverlayId: "rectangle", // 激活图层
              selectable: true, // 开启选择
              snappable: true, // 开启吸附
            }),
          });
        // 监听绘制结束事件，获取绘制几何图形
        this.map.editor.on("draw_complete", (geometry) => {
          this.$store.commit("SET_MAP", { rectangleID: geometry.id });
          // 获取矩形顶点坐标
          var geo = this.map.markerLayer.geometries.filter(function (item) {
            return item.id === geometry.id;
          })[0];
          this.setBox(geo.paths[2], geo.paths[0]);
          this.map.editor.setActionMode(this.map.mode.interact); // 进入编辑模式
          // 需要完善编辑功能
        });
      }
    },
    setBox(nw = { lng: "", lat: "" }, se = { lng: "", lat: "" }) {
      // 框选后自动填入
      this.area.nw.point = { lng: nw.lng, lat: nw.lat };
      this.area.se.point = { lng: se.lng, lat: se.lat };
      this.$forceUpdate();
    },
  },
};
</script>
