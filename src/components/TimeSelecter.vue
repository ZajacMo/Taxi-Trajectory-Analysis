<template>
  <div>
    <el-time-select
      placeholder="起始时间"
      v-model="startTime"
      :editable="false"
      :picker-options="pickerOptions"
    >
    </el-time-select>
    <el-time-select placeholder="结束时间（只读）" v-model="endTime" readonly>
    </el-time-select>
  </div>
</template>

<script>
export default {
  name: "TimeSelecter",
  data() {
    return {
      startTime: "",
      endTime: "",
      pickerOptions: {
        start: "00:00",
        step: "01:00",
        end: "23:00",
      },
    };
  },
  watch: {
    startTime: {
      handler(newVal) {
        this.$emit("form-changed", newVal);
        if (newVal) {
          const [hours, minutes] = newVal.split(":");
          let newHours = parseInt(hours, 10) + 1;
          if (newHours >= 24) {
            newHours = 0;
          }
          this.endTime = `${newHours.toString().padStart(2, "0")}:${minutes}`;
          this.$emit("time-changed", parseInt(hours));
        }
      },
      deep: true, // 深度监听
    },
  },
};
</script>

<style scoped>
/* 可以在这里添加样式 */
</style>
