<template>
  <!-- <tlbs-map
    ref="mapRef"
    api-key="U3EBZ-4MQ6T-F3FX5-LVNPW-RYHNQ-FIB6V"
    :center="center"
    :zoom="zoom"
    :control="control"
    :options="{
      mapStyleId: 'style4',
      pitch: 46.9,
      rotation: 13.6,
      renderOptions: {
        enableBloom: true, // 泛光
      },
    }"
    @click="onClick"
    @map_inited="onMapInited"
  >
    <tlbs-multi-marker
      ref="markerRef"
      :geometries="geometries"
      :styles="styles"
      :options="options"
    />
    <div class="control-container">
      <button @click.stop="getLayerInstance">打印点标记实例</button>
    </div>
  </tlbs-map> -->
  <div id="container"></div>
</template>

<script>
export default {
  name: "MapContainer",
  props: {
  },

  data() {
    return {
      src: `https://map.qq.com/api/gljs?v=1.exp&key=U3EBZ-4MQ6T-F3FX5-LVNPW-RYHNQ-FIB6V&libraries=visualization`,
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

  // setup() {
  //   const mapRef = ref(null);
  //   const markerRef = ref(null);
  //   const center = ref({ lat: 39.91799, lng: 116.397027 });
  //   const zoom = ref(11);
  //   const arcData = ref([]);
  //   const onClick = (e) => {
  //     console.log(e);
  //   };
  //   // onMounted(async () => {
  //   //   await loadData();
  //   //   arcData.value = (window as any).arcData || [];
  //   // });
  //   const onMapInited = () => {
  //     // 地图加载完成后，可以获取地图实例、点标记实例，调用地图实例、点标记实例方法
  //     console.log(mapRef.value.map);
  //     console.log(markerRef.value.marker);
  //   };

  //   const getLayerInstance = () => {
  //     // 可以获取点标记实例，调用点标记实例方法
  //     console.log(markerRef.value.marker);
  //   };

  //   return {
  //     center,
  //     zoom,
  //     onClick,
  //     onMapInited,
  //     getLayerInstance,
  //     control: {
  //       scale: {},
  //       zoom: {
  //         position: "topRight",
  //       },
  //     },
  //     mapRef,
  //     markerRef,
  //     geometries: [
  //       { styleId: "marker", position: { lat: 39.91799, lng: 116.397027 } },
  //     ],
  //     styles: {
  //       marker: {
  //         width: 20,
  //         height: 30,
  //         anchor: { x: 10, y: 30 },
  //       },
  //     },
  //     options: {
  //       minZoom: 5,
  //       maxZoom: 15,
  //     },
  //   };
  // },
  mounted() {
    this.loadMap();
  },
  methods: {
    loadMap() {
      let script = document.createElement("script");
      script.src = this.src;
      script.type = "text/javascript";
      document.body.appendChild(script);
      let styleId = document.createElement("script");
      styleId.src = "https://map.qq.com/api/gljs?v=1.exp&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77";
      document.head.appendChild(styleId);
      let scriptData = document.createElement("script");
      scriptData.src = "https://mapapi.qq.com/web/lbs/visualizationApi/demo/data/trail.js";
      document.head.appendChild(scriptData);
      scriptData.onload = () => {
        this.drawMap();
      };

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
