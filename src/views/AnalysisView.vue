<template>
  <div
    class="association-view"
    v-loading="this.loading"
    element-loading-text="拼命计算中，请耐心等待"
  >
    <!-- 模式和区域切换 -->
    <ModeAndAreaSwitch @select-change="(newVal) => (selected = newVal)" />

    <!-- 频繁路径分析 -->
    <frequence-view
      :selected="selected"
      @frequence-changed="(newVal) => (form.frequence = newVal)"
      v-show="selected.mode === '频繁路径分析'"
      ref="frequenceView"
    />

    <!-- 区域1坐标 -->
    <div
      v-show="selected.mode !== '频繁路径分析' || selected.radio !== '单区域'"
    >
      <el-divider>
        <h3
          v-if="
            (selected.radio === '两区域' &&
              ['区域关联分析', '频繁路径分析'].includes(selected.mode)) ||
            selected.mode === '通时行间分析'
          "
        >
          区域1
        </h3>
        <h3 v-else>区域</h3>
      </el-divider>
      <select-rectangle
        id="1"
        @area1-changed="
          (newVal) => {
            form.area1 = newVal;
          }
        "
        ref="area1"
      />
    </div>

    <!-- 区域2坐标 -->
    <div
      v-show="
        (selected.radio === '两区域' &&
          ['区域关联分析', '频繁路径分析'].includes(selected.mode)) ||
        selected.mode === '通时行间分析'
      "
    >
      <el-divider><h3>区域2</h3></el-divider>
      <select-rectangle
        id="2"
        @area2-changed="
          (newVal) => {
            form.area2 = newVal;
          }
        "
        ref="area2"
      />
    </div>

    <!-- 时间选择器 -->
    <el-date-picker
      v-if="selected.mode === '区域范围查找'"
      v-model="form.dateRange"
      type="datetimerange"
      start-placeholder="开始时间"
      end-placeholder="结束时间"
      :default-value="new Date(2008, 0, 1, 0, 0, 0)"
      :picker-options="options.pickerOptions"
      size="small"
      align="right"
    />

    <div style="padding-top: 20px">
      <el-button type="danger" @click="clearAll">清空</el-button>

      <el-button type="primary" @click="confirm" :loading="this.loading"
        >确认</el-button
      >
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";
import SelectRectangle from "@/components/SelectRectangle.vue";
import FrequenceView from "@/components/FrequenceView.vue";
import ModeAndAreaSwitch from "@/components/ModeAndAreaSwitch.vue";
export default {
  name: "AnalysisView",
  components: {
    SelectRectangle,
    FrequenceView,
    ModeAndAreaSwitch,
  },
  computed: {
    ...mapState(["map"]),
    loading() {
      return this.$store.state.trails.loading;
    },
  },
  data() {
    return {
      // radio: "单区域",
      // selectedMode: "区域范围查找",
      selected: {
        radio: "单区域",
        mode: "区域范围查找",
      },
      form: {
        dateRange: null,
        frequence: {
          minDistance: "",
          pathCount: 10,
        },
        area1: null,
        area2: null,
      },
      options: {
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
      },
    };
  },

  methods: {
    clearAll() {
      // 清空所有区域
      // this.$store.commit("RESET_MARKERLAYER");
      this.$refs.area1.setBox();
      this.$refs.area2.setBox();
      this.$refs.frequenceView.clearForm();
      this.form.dateRange = null;
      this.$store.commit("RESET_MARKERLAYER");
    },

    confirm() {
      if (this.selected.mode === "区域范围查找") {
        this.$store.dispatch("fetchAreaTrails", {
          dateRange: this.form.dateRange,
          area: this.form.area1,
        });
      } else if (this.selected.mode === "区域关联分析") {
        // console.log("区域关联分析");
        this.$store.dispatch("fetchAreaAssociation", {
          area1: this.form.area1,
          area2: this.form.area2,
        });
      } else if (this.selected.mode === "频繁路径分析") {
        if (this.selected.radio === "单区域") {
          console.log("单区域分析", this.form.frequence);
          this.$store.dispatch("fetchFrequencePath", {
            frequence: this.form.frequence,
          });
        } else {
          console.log("两区域分析", this.form);
          this.$store.dispatch("fetchFrequencePath2", {
            frequence: this.form.frequence,
            area1: this.form.area1,
            area2: this.form.area2,
          });
        }
      } else {
        this.$store.dispatch("fetchTimeSpaceAnalysis", {
          area1: this.form.area1,
          area2: this.form.area2,
        });
      }
    },
  },
};
</script>
<style scoped>
/* .el-input {
  padding-right: 20px;
} */
.association-view {
  padding: 40px;
  padding-top: 0;
}
h3 {
  margin: 0;
}
</style>
