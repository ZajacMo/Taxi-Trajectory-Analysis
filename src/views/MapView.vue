<template>
  <div class="map-container">
    <nav-menu style="max-width: 65%" />
    <map-container ref="mapInstance" @ready="initMapOverlays" />
    <!-- <g
      v-for="node in nodes"
      :key="node.id"
      :transform="`translate(${node.x},${node.y})`"
      @click="selectNode(node)"
    >
      <circle r="15" :fill="node.color || '#4CAF50'" />
      <text y="5" class="node-label">{{ node.name }}</text>
    </g> -->
  </div>
</template>

<script>
// import { mapState } from "vuex";
import NavMenu from "@/components/NavMenu.vue";
import MapContainer from "@/components/MapContainer";
export default {
  components: {
    MapContainer,
    NavMenu,
  },
  data() {
    return {
      transportType: "walk",
      mapMarkers: [],
      pathOverlays: [],
    };
  },
  // computed: {
  //   ...mapState(["nodes", "edges", "currentPath"]),
  //   paths() {
  //     return this.currentPath?.map((segment) => ({
  //       d: this.generatePathD(segment),
  //       color: this.getTransportColor(segment.transport),
  //     }));
  //   },
  // },
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
        const res = await this.$axios.post(
          "/shortest-path",
          {
            startId: startNode.id,
            endId: endNode.id,
            transport: this.transportType,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
          }
        );
        this.$store.commit("SET_CURRENT_PATH", res.data.path);
      } catch (error) {
        console.error("路径计算失败:", error);
      }
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
