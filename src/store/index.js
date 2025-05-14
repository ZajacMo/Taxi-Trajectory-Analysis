import Vue from "vue";
import Vuex from "vuex";
// import TMap from "https://map.qq.com/api/gljs?v=1.exp&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77&libraries=visualization";
// import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    map: {
      map: null, // 用于存储地图实例的状态
      mode: null,
      trail: null, // 用于存储轨迹实例的状态
      markerLayer: null, // 用于存储标记点实例的状态
      rectangleID: null, // 用于存储矩形实例的状态
    },
    markedPoint: [], // 用于存储标记点的状态
    // 轨迹数据的状态
    trails: {
      loading: false,
      options: [],
      data: [],
    },
  },
  mutations: {
    SET_MAP(state, item) {
      for (let key in item) {
        state.map[key] = item[key];
      }
    },
    SET_TRAILS(state, item) {
      for (let key in item) {
        state.trails[key] = item[key];
      }
    },
    SET_TRAILS_DATA(state, value) {
      state.map.trail.setData(value);
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
    RESET_STATISTICS(state) {
      if (state.map.rectangleID) {
        state.map.markerLayer.remove(state.map.rectangleID);
        state.map.rectangleID = null;
        state.map.editor.setActionMode(state.map.mode.draw);
      }
    },
  },
  actions: {
    async fetchTrails({ commit }, { taxi_ids, simplify, tolerance }) {
      commit("SET_TRAILS", { loading: true, options: taxi_ids });
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
        commit("SET_TRAILS_DATA", data);
      } catch (error) {
        console.error("发送路线数据失败:", error);
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
  },
  modules: {},
});
