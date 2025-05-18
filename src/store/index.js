import Vue from "vue";
import Vuex from "vuex";
import { Notification } from "element-ui";
// import TMap from "https://map.qq.com/api/gljs?v=1.exp&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77&libraries=visualization";
// import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    map: {
      map: null, // 用于存储地图实例的状态
      mode: null,
      trail: null, // 用于存储轨迹实例的状态
      heat: null, // 用于存储热力图实例的状态
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
    refresh: false,
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
    SET_HEAT_DATA(state, value) {
      console.log("设置热力图数据", value);
      // console.log("热力图实例", state.map.heat);
      state.map.heat.setData(value);
      // 数据聚合之后才能够真正获取值域范围
      state.map.heat.setShowRange(state.map.heat.getValueRange());
      // state.trails.data = value;
    },
    RESET_MARKERLAYER(state) {
      if (state.map.rectangleID) {
        state.map.markerLayer.remove(state.map.rectangleID);
        state.map.rectangleID = null;
        state.map.editor.setActionMode(state.map.mode.draw);
      }
    },
  },
  actions: {
    async fetchDensityData({ commit }, { r, startTime }) {
      commit("SET_TRAILS", { loading: true });
      try {
        const params = new URLSearchParams({
          r: r / 111,
          hour: startTime,
        });
        const response = await fetch(`/api/heatmap?${params.toString()}`, {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        });
        var data = await response.json();
        if (data.length === 0) {
          Notification({
            title: "消息",
            message: "暂无热力图数据",
            type: "error",
            duration: 5000,
          });
        } else {
          commit("SET_HEAT_DATA", data.data);
          // console.log(data);
          Notification({
            title: "成功",
            message: `成功获取${data.data.length}条热力图数据`,
            type: "success",
            duration: 5000,
          });
        }
      } catch (error) {
        Notification({
          title: "错误",
          message: "获取热力图数据失败",
          type: "error",
          duration: 5000,
        });
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
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
        if (data.length === 0) {
          Notification({
            title: "消息",
            message: "暂无轨迹",
            type: "error",
            duration: 5000,
          });
        } else {
          Notification({
            title: "成功",
            message: `成功获取${data.length}条轨迹`,
            type: "success",
            duration: 5000,
          });
        }
      } catch (error) {
        Notification({
          title: "错误",
          message: "获取轨迹数据失败",
          type: "error",
          duration: 5000,
        });
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
    async fetchAreaTrails({ commit }, { dateRange, area }) {
      commit("SET_TRAILS", { loading: true });
      try {
        const response = await fetch("/api/query_region", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            startTime:
              dateRange[0].toISOString().split("T")[0] +
              " " +
              dateRange[0].toTimeString().split(" ")[0],
            endTime:
              dateRange[1].toISOString().split("T")[0] +
              " " +
              dateRange[1].toTimeString().split(" ")[0],
            ltPoint: [area.nw.point.lng, area.nw.point.lat],
            rbPoint: [area.se.point.lng, area.se.point.lat],
          }),
        });
        var data = await response.json();
        // console.log(data);
        if (data.total === 0) {
          Notification({
            title: "消息",
            message: "查询区域范围内无轨迹",
            type: "error",
            duration: 10000,
          });
        } else {
          commit("SET_TRAILS_DATA", data.path);
          Notification({
            title: "成功",
            message: `成功查询区域范围内${data.total}条轨迹`,
            type: "success",
            duration: 10000,
          });
        }
      } catch (error) {
        Notification({
          title: "错误",
          message: "查询区域范围内轨迹失败",
          type: "error",
          duration: 5000,
        });
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
    async fetchAreaAssociation({ commit }, { area1, area2 }) {
      commit("SET_TRAILS", { loading: true });
      try {
        const params = {
          area1: `${area1.nw.point.lng},${area1.se.point.lng},${area1.se.point.lat},${area1.nw.point.lat}`,
        };
        if (area2) {
          params.area2 = `${area2.nw.point.lng},${area2.se.point.lng},${area2.se.point.lat},${area2.nw.point.lat}`;
        }
        const queryString = Object.entries(params)
          .map(
            ([key, value]) =>
              `${encodeURIComponent(key)}=${encodeURIComponent(value)}`
          )
          .join("&");
        const url = `/api/flow_analysis?${queryString}`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });
        var data = await response.json();
        console.log(data);
        if (data.status === "success") {
          Notification({
            title: "成功",
            message: "查询区域关联关系成功",
            type: "success",
            duration: 5000,
          });
        } else {
          throw new Error("查询区域关联关系失败");
        }
      } catch (error) {
        Notification({
          title: "错误",
          message: "查询区域关联关系失败",
          type: "error",
          duration: 5000,
        });
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
    async fetchFrequencePath({ commit }, { frequence }) {
      commit("SET_TRAILS", { loading: true });
      try {
        const response = await fetch("/api/frequent_paths", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            minDistance: parseInt(frequence.minDistance),
            k: frequence.pathCount,
          }),
        });
        var data = await response.json();
        console.log(data);
      } catch (error) {
        console.error("请求 /frequent_paths 时出错:", error);
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
    async fetchFrequencePath2({ commit }, { frequence, area1, area2 }) {
      commit("SET_TRAILS", { loading: true });
      try {
        const response = await fetch("/api/frequent_paths_ab", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({
            k: frequence.pathCount,
            areaA: {
              ltPoint: [area1.nw.point.lng, area1.nw.point.lat],
              rbPoint: [area1.se.point.lng, area1.se.point.lat],
            },
            areaB: {
              ltPoint: [area2.nw.point.lng, area2.nw.point.lat],
              rbPoint: [area2.se.point.lng, area2.se.point.lat],
            },
          }),
        });
        var data = await response.json();
        console.log(data);
      } catch (error) {
        // console.error("请求 /flow_analysi 时出错:", error);
        Notification({
          title: "错误",
          message: "区域关联分析失败",
          type: "error",
          duration: 5000,
        });
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
    async fetchTimeSpaceAnalysis({ commit }, { area1, area2 }) {
      commit("SET_TRAILS", { loading: true });
      try {
        const params = {
          area1: `${area1.nw.point.lng},${area1.se.point.lng},${area1.se.point.lat},${area1.nw.point.lat}`,
          area2: `${area2.nw.point.lng},${area2.se.point.lng},${area2.se.point.lat},${area2.nw.point.lat}`,
        };
        const queryString = Object.entries(params)
          .map(
            ([key, value]) =>
              `${encodeURIComponent(key)}=${encodeURIComponent(value)}`
          )
          .join("&");
        const url = `/api/optimized_path?${queryString}`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });
        var data = await response.json();
        // console.log(data);
        if (data.status === "success") {
          Notification({
            title: "成功",
            message: "通行时间分析成功",
            type: "success",
            duration: 5000,
          });
        } else {
          throw new Error("请求失败");
        }
      } catch (error) {
        // console.error("请求 /flow_analysi 时出错:", error);
        Notification({
          title: "错误",
          message: "通行时间分析失败",
          type: "error",
          duration: 5000,
        });
      } finally {
        commit("SET_TRAILS", { loading: false });
      }
    },
  },
  modules: {},
});
