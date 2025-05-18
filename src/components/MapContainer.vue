<template>
  <div id="container"></div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "MapContainer",
  data() {
    return {
      initCenter: {
        lng: 39.91799,
        lat: 116.397027,
      },
      zoomLevel: 11,
    };
  },
  mounted() {
    // this.loadMap();
    if(!this.$store.state.map.map){
      this.drawMap();
    }
  },
  computed: {
    ...mapState(["map"]),
  },
  methods: {
    // loadMap() {
    //   // 创建并加载所需的脚本
    //   const scripts = [
    //     { src: 'https://mapapi.qq.com/web/lbs/visualizationApi/demo/data/trail.js', target: 'head', onload: () => this.drawMap() }
    //   ];
    //   scripts.forEach(({ src, target, onload }) => {
    //     const script = document.createElement('script');
    //     script.src = src;
    //     script.type = 'text/javascript';
    //     if (onload) script.onload = onload;
    //     document[target].appendChild(script);
    //   });
    // },
    drawMap(){
      this.$store.commit("SET_MAP", {
        map:new TMap.Map("container", {
          center: new TMap.LatLng(this.initCenter.lng, this.initCenter.lat),
          zoom: this.zoomLevel,
          mapStyleId: "style4",
          pitchable: true,
          baseMap:{
            type: "vector",
            features:["base","building3d"],
          },
          renderOptions:{
            skyOptions:{
              color: "#000000", //天空颜色
              intensity: 0.5, //天空亮度
            },
            fogOptions:{
              color: "#000000", //天空颜色
              intensity: 0.5, //天空亮度
            }
          },
        })
      });
      // 获取缩放控件实例并设置到右下角
      this.map.map
        .getControl(TMap.constants.DEFAULT_CONTROL_ID.ZOOM)
        .setPosition(TMap.constants.CONTROL_POSITION.BOTTOM_RIGHT);
      // 获取3D罗盘控件实例并设置到右下角
      this.map.map
        .getControl(TMap.constants.DEFAULT_CONTROL_ID.ROTATION)
        .setPosition(TMap.constants.CONTROL_POSITION.BOTTOM_RIGHT);
      // 添加轨迹可视化
      this.$store.commit("SET_MAP", {
        trail: new TMap.visualization.Trail({
          pickStyle: function (trailLine) {
            return {
                width: 2,
                color: "rgba(29,250,242,0.3)",
            };
          },
          showDuration: 120, //动画中轨迹点高亮的持续时间
          playRate: 70, // 动画播放倍速
          enableHighlightPoint: true, //是否显示头部高亮点
        }).addTo(this.map.map)
      }) // 通过addTo()添加到指定地图实例
    }
  },
};
</script>

<style scoped>
#container {
  width: 100%;
  height: 100vh;
}
</style>
