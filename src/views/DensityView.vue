<template>
  <div class="density-view"
    v-loading="this.loading"
    element-loading-text="拼命计算中，请耐心等待">
    <h3>车流密度分析</h3>
    <el-input v-model="form.r" placeholder="请输入距离参数r">
      <template slot="append">千米</template>
    </el-input>
    <TimeSelecter @time-changed="(selectedHours) => { this.form.startTime = selectedHours }" />
    <div>
      <el-button @click="clearForm">清空</el-button>
      <el-button type="primary" @click="confirmForm">确认</el-button>
    </div>
    <el-card shadow="hover" style="width: 100%; margin-top: 20px">
      <div style="width: 100%; display: inline-block">
        <el-statistic title="聚合热力值">
          <template slot="formatter">{{ heatValue }}</template>
        </el-statistic>
      </div>
    </el-card>
  </div>
</template>

<script>
import TimeSelecter from '@/components/TimeSelecter.vue';
export default {
  name: "DensityView",
  components: {
    TimeSelecter,
  },
  data() {
    return {
      form: {
        r: "",
        startTime: "",
      },
      heatValue: "请选择",
    };
  },
  computed: {
    map() {
      return this.$store.state.map.map;
    },
    heat() {
      return this.$store.state.map.heat;
    },
    loading() {
      return this.$store.state.trails.loading;
    },
  },
  methods: {
    clearForm() {
      this.form.r = "";
      this.form.startTime = "";
      this.form.endTime = "";
    },
    confirmForm() {
      if (!this.form.r || !this.form.startTime || !this.form.endTime) {
        this.$message.error("请填写完整的参数");
        return;
      }
      // console.log("确认参数:", this.form);
      //初始化网格热力图图并添加至map图层
      this.$store.commit("SET_MAP", {
        heat: new TMap.visualization.Grid({
          sideLength: this.form.r*1000, // 设置网格边长
          heightRange: [1, 30000], // 高度变化区间
          showRange: [1, 100], // 聚合数据显示区间
          selectOptions: {
            //拾取配置
            action: "click", //拾取动作
            style: "#E9AB1D",
            enableHighlight: false, //是否使用高亮效果
          },
        }).addTo(this.map),
      });
      this.$store.dispatch("fetchDensityData", {
        r: this.form.r, 
        startTime: this.form.startTime
      });
      // 绑定事件
      this.heat.on("click", (evt) => {
        var aggregator = evt && evt.detail && evt.detail.aggregator;
        if (aggregator) {
          this.heatValue = aggregator.count;
        }
      });
    },
  },
};
</script>

<style scoped>
/* 可以在这里添加样式 */
.el-input {
  /* width: 30%; */
  padding-right: 20px;
}
.density-view {
  padding: 40px;
}
div{
  margin-bottom: 20px;
}
/* .el-date-editor.el-range-editor {
  width: 100px;
} */
</style>
