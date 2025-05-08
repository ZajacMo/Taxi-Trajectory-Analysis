<template>
  <div id="container"></div>
</template>

<script>
export default {
  name: "MapContainer",
  props: {
  },

  data() {
    return {
      // src:`https://map.qq.com/api/gljs?v=1.exp&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77&libraries=visualization`,
      map: null,
      initCenter: {
        lng: 39.91799,
        lat: 116.397027,
      },
      zoomLevel: 11,
      trail:null,
    };
  },
  mounted() {
    this.loadMap();
  },
  methods: {
    loadMap() {
      // 创建并加载所需的脚本
      const scripts = [
        { src: `https://map.qq.com/api/gljs?v=1.exp&key=U3EBZ-4MQ6T-F3FX5-LVNPW-RYHNQ-FIB6V&libraries=visualization`, target: 'head' },
        { src: 'https://map.qq.com/api/gljs?v=1.exp&key=U3EBZ-4MQ6T-F3FX5-LVNPW-RYHNQ-FIB6V', target: 'head' },
        { src: 'https://mapapi.qq.com/web/lbs/visualizationApi/demo/data/trail.js', target: 'head', onload: () => this.drawMap() }
      ];
      scripts.forEach(({ src, target, onload }) => {
        const script = document.createElement('script');
        script.src = src;
        script.type = 'text/javascript';
        if (onload) script.onload = onload;
        document[target].appendChild(script);
      });
    },
    drawMap(){
      this.map = new TMap.Map("container", {
        center: new TMap.LatLng(this.initCenter.lng, this.initCenter.lat),
        zoom: this.zoomLevel,
        mapStyleId: "style2",
        baseMap:{
          type: "vector",
          features:["base","building3d"],
        }
      });
      // 获取缩放控件实例并设置到右下角
      const zoomControl = this.map.getControl(TMap.constants.DEFAULT_CONTROL_ID.ZOOM);
      zoomControl.setPosition(TMap.constants.CONTROL_POSITION.BOTTOM_RIGHT);
      // 获取3D罗盘控件实例并设置到右下角
      const compassControl = this.map.getControl(TMap.constants.DEFAULT_CONTROL_ID.ROTATION);
      compassControl.setPosition(TMap.constants.CONTROL_POSITION.BOTTOM_RIGHT);
      // 添加轨迹可视化
      this.trail = new TMap.visualization.Trail({
        pickStyle: function (trailLine) {
          return {
              width: 2,
              color: "rgba(29,250,242,0.3)",
            };
          },
          showDuration: 120, //动画中轨迹点高亮的持续时间
          playRate: 70, // 动画播放倍速
          enableHighlightPoint: true, //是否显示头部高亮点
      }).addTo(this.map); // 通过addTo()添加到指定地图实例
      // 轨迹点数据
      this.trail.setData(trailData);
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
