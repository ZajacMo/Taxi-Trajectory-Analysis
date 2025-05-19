<template>
  <div ref="chart" style="width: 100%; height: 400px"></div>
</template>

<script>
import * as echarts from "echarts/core";
import { LineChart } from "echarts/charts";
import { TitleComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import {
  LegendComponent,
  ToolboxComponent,
  GridComponent,
} from "echarts/components";

// 注册必须的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  LineChart,
  CanvasRenderer,
  LegendComponent,
  ToolboxComponent,
  GridComponent,
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
      propNames: [
        ["流出该区域", "流出入区域"],
        ["区域1流向区域2", "区域2流向区域1"],
      ],
    };
  },
  computed: {
    flowData() {
      var lists = this.$store.state.echart.data;
      var flowIN = lists.map((item) => item.flowIn);
      var flowOUT = lists.map((item) => item.flowOut);
      return [flowIN, flowOUT];
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
          left: "center",
          top: "0",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            animation: false,
          },
        },
        legend: {
          data: this.propNames[this.mode === "单区域" ? 0 : 1],
          left: "center",
          top: "bottom",
        },
        toolbox: {
          feature: {
            saveAsImage: {
              show: true,
              name: "image",
              title: "保存为图片",
            },
          },
        },
        axisPointer: {
          link: [
            {
              xAxisIndex: "all",
            },
          ],
        },
        grid: [
          {
            left: 60,
            right: 50,
            height: "35%",
          },
          {
            left: 60,
            right: 50,
            top: "55%",
            height: "35%",
          },
        ],
        xAxis: [
          {
            type: "category",
            boundaryGap: false,
            axisLine: { onZero: true },
            axisPointer: {
              snap: true,
              label: {
                show: true,
                backgroundColor: "#6a7985",
              },
            },
            data: this.label,
          },
          {
            gridIndex: 1,
            type: "category",
            boundaryGap: false,
            axisLine: { onZero: true },
            show: false,
            // data: timeData,
            data: this.label,
            position: "top",
          },
        ],
        yAxis: [
          {
            name: "车流量(辆)",
            type: "value",
            // max: 500,
          },
          {
            gridIndex: 1,
            name: "车流量(辆)",
            type: "value",
            inverse: true,
          },
        ],
        series: [
          {
            name: this.propNames[this.mode === "单区域" ? 0 : 1][0],
            type: "line",
            symbolSize: 8,
            // prettier-ignore
            data: this.flowData[0],
          },
          {
            name: this.propNames[this.mode === "单区域" ? 0 : 1][1],
            type: "line",
            xAxisIndex: 1,
            yAxisIndex: 1,
            symbolSize: 8,
            // prettier-ignore
            data: this.flowData[1],
          },
        ],
      };
      chart.setOption(option);
    },
  },
};
</script>

<style scoped></style>
