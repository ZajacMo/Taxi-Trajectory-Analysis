<template>
  <div class="density-view">
    <el-input v-model="form.r" placeholder="请输入距离参数r">
      <template slot="append">千米</template>
    </el-input>

    <el-time-select
      placeholder="起始时间"
      v-model="form.startTime"
      :editable="false"
      :picker-options="{
        start: '00:00',
        step: '01:00',
        end: '23:00',
      }"
    >
    </el-time-select>
    <el-time-select
      placeholder="结束时间（只读）"
      v-model="form.endTime"
      readonly
    >
    </el-time-select>
    <div>
      <el-button @click="clearForm">清空</el-button>
      <el-button type="primary" @click="confirmForm">确认</el-button>
    </div>
    <el-card shadow="hover" style="width: 100%; margin-top: 20px">
      <div style="width: 100%; display: inline-block">
        <el-statistic :value="heatValue" title="聚合热力值"> </el-statistic>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "DensityView",
  data() {
    return {
      form: {
        r: "",
        startTime: "",
        endTime: "",
      },
      heatValue: 0,
    };
  },
  watch: {
    form: {
      handler(newVal) {
        this.$emit("form-changed", newVal);
        if (newVal.startTime) {
          const [hours, minutes] = newVal.startTime.split(":");
          let newHours = parseInt(hours, 10) + 1;
          if (newHours >= 24) {
            newHours = 0;
          }
          this.form.endTime = `${newHours
            .toString()
            .padStart(2, "0")}:${minutes}`;
        }
      },
      deep: true, // 深度监听
    },
  },
  computed: {
    map() {
      return this.$store.state.map.map;
    },
    heat() {
      return this.$store.state.map.heat;
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
        startTime: parseInt(this.form.startTime.slice(0, 2), 10)
      });
      // 绑定事件
      this.heat.on("click", (evt) => {
        var aggregator = evt && evt.detail && evt.detail.aggregator;
        if (aggregator) {
          this.heatValue = aggregator.count;
        }
      });
      // 这里可以添加具体的业务逻辑
      // this.$emit(");
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
/* .el-date-editor.el-range-editor {
  width: 100px;
} */
</style>
