<template>
  <div ref="chart" style="width: 100%; height: 400px"></div>
</template>

<script>
import * as echarts from "echarts/core";
import { FunnelChart } from "echarts/charts";
import { TitleComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { LegendComponent, ToolboxComponent } from "echarts/components";

// 注册必须的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  FunnelChart,
  CanvasRenderer,
  LegendComponent,
  ToolboxComponent,
]);

export default {
  name: "EChartsFunnelChart",
  props: {
    mode: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      label: Array.from({ length: 24 }, (_, index) => {
        const start = String(index).padStart(2, "0");
        const end = String(index + 1).padStart(2, "0");
        return `${start}:00-${end}:00`;
      }),
    };
  },
  computed: {
    flowData() {
      return this.$store.state.echart.data;
    },
  },
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.chart);
      const option = {
        title: {
          text: `${this.mode}关联分析图`,
          subtext: "Fake Data",
          left: "center",
          top: "top",
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c}%",
        },
        toolbox: {
          show: true,
          orient: "vertical",
          top: "center",
          feature: {
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {},
          },
        },
        legend: {
          orient: "vertical",
          left: "left",
          data: this.label,
        },
        series: [
          {
            name: "Funnel",
            type: "funnel",
            width: "40%",
            height: "90%",
            left: "5%",
            top: "10%",
            sort: "none",
            funnelAlign: "right",
            data: [
              { value: 60, name: "Prod C" },
              { value: 30, name: "Prod D" },
              { value: 80, name: "Prod B" },
              { value: 10, name: "Prod E" },
              { value: 100, name: "Prod A" },
            ],
          },
          {
            name: "Pyramid",
            type: "funnel",
            width: "40%",
            height: "90%",
            left: "55%",
            top: "10%",
            sort: "none",
            funnelAlign: "left",
            data: [
              { value: 60, name: "Prod C" },
              { value: 30, name: "Prod D" },
              { value: 10, name: "Prod E" },
              { value: 80, name: "Prod B" },
              { value: 100, name: "Prod A" },
            ],
          },
        ],
      };
      chart.setOption(option);
    },
  },
};
</script>

<style scoped></style>
