import Vue from "vue";
import Vuex from "vuex";
// import TMap from "https://map.qq.com/api/gljs?v=1.exp&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77&libraries=visualization";
// import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    map: null, // 用于存储地图实例的状态
    trail: null, // 用于存储轨迹实例的状态
    markerLayer: null, // 用于存储标记点实例的状态
    markedPoint: [], // 用于存储标记点的状态
    // 轨迹数据的状态
    trails: {
      loading: false,
      options: [],
      data: [],
    },
  },
  mutations: {
    SET_MAP(state, map) {
      state.map = map;
    },
    SET_TRAIL(state, trail) {
      state.trail = trail;
    },
    SET_TRAIL_LOADING(state, value) {
      state.trails.loading = value;
    },
    SET_TRAIL_OPTIONS(state, value) {
      state.trails.options = value;
    },
    SET_MARKERLAYER(state, markerLayer) {
      state.markerLayer = markerLayer;
    },
    SET_TRAIL_DATA(state, value) {
      state.trail.setData(value);
      state.trails.data = value;
    },
    CREATE_MARKER(state, markerLayer) {
      //监听点击事件添加marker
      state.map.on("click", (evt) => {
        markerLayer.add({
          position: evt.latLng,
        });
        state.markedPoint = evt.latLng;
      });
    },
  },
  actions: {
    async fetchTrails({ commit }, { taxi_ids, simplify, tolerance }) {
      commit("SET_TRAIL_LOADING", true);
      commit("SET_TRAIL_OPTIONS", taxi_ids);
      console.log("正在发送路线数据...");
      try {
        // 确保axios实例已正确导入和配置
        const response = await fetch("/api/trails/data", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            taxi_ids: taxi_ids,
            simplify: simplify,
            tolerance: tolerance,
          }),
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        commit("SET_TRAIL_DATA", data);
      } catch (error) {
        console.error("发送路线数据失败:", error);
      } finally {
        commit("SET_TRAIL_LOADING", false);
      }
    },
  },
  modules: {},
});
