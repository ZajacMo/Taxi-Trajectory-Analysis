<template>
  <div class="map-container">
    <map-container ref="mapInstance" @ready="initMapOverlays" />
    <g
      v-for="node in nodes"
      :key="node.id"
      :transform="`translate(${node.x},${node.y})`"
      @click="selectNode(node)"
    >
      <circle r="15" :fill="node.color || '#4CAF50'" />
      <text y="5" class="node-label">{{ node.name }}</text>
    </g>
  </div>
</template>

<script>
import { mapState } from "vuex";
import MapContainer from "@/components/MapContainer";

export default {
  components: {
    MapContainer,
  },
  props: {
    selectedRoutes: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      transportType: "walk",
      mapMarkers: [],
      pathOverlays: [],
    };
  },
  computed: {
    ...mapState(["nodes", "edges", "currentPath"]),
    paths() {
      return this.currentPath?.map((segment) => ({
        d: this.generatePathD(segment),
        color: this.getTransportColor(segment.transport),
      }));
    },
  },
  methods: {
    // 地图初始化完成回调
    initMapOverlays() {
      this.$refs.mapInstance.map.addEventListener("click", this.handleMapClick);
    },

    // 地图点击事件
    handleMapClick() {
      // const point = new window.BMap.Point(e.point.lng, e.point.lat);
      // 这里添加点击地图的交互逻辑
    },
    // ...其他交互方法

    // 路径计算方法
    async calculatePath() {
      const { startNode, endNode } = this.$store.state;
      try {
        const res = await this.$axios.post("/shortest-path", {
          startId: startNode.id,
          endId: endNode.id,
          transport: this.transportType,
        });
        this.$store.commit("SET_CURRENT_PATH", res.data.path);
      } catch (error) {
        console.error("路径计算失败:", error);
      }
    },
  },
  watch: {
    selectedRoutes: {
      async handler(newRoutes, oldRoutes) {
        if (newRoutes.length !== oldRoutes.length) {
          // 向后端发送选中路线数据
          try {
            // 确保axios实例已正确导入和配置
            await this.$http.post("/api", {
              routes: newRoutes,
            });
          } catch (error) {
            console.error("发送路线数据失败:", error);
          }
        }
      },
      deep: true,
    },
  },
};
</script>

<style>
.clickable {
  cursor: pointer;
  transition: stroke-width 0.2s;
}

.clickable:hover {
  stroke-width: 3px;
}
</style>
