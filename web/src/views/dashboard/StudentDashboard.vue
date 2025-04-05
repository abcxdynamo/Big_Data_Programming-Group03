<template>
        <h3>Student Information</h3>
        <el-descriptions border>
            <el-descriptions-item label="Name">{{ user_info.first_name }} {{ user_info.last_name }}</el-descriptions-item>
            <el-descriptions-item label="Email">{{ user_info.email }}</el-descriptions-item>
            <el-descriptions-item label="Term">{{ term.year }} {{ term.season }}</el-descriptions-item>
            <el-descriptions-item label="Program">{{ program.name }}</el-descriptions-item>
        </el-descriptions>
            <h3>Performance Trends</h3>
            <div class="chart-container">
                <div class="chart" ></div>
            </div>
</template>
<script>
import { defineComponent, ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';

export default {
  data() {
    return {
      user_id: null,
      user_info: {},
      enrollment: {},
      term: {},
      program: {},
      performanceChartOptions: {
        width: 600,
        height:400,
        //title: { text: 'Performance Trends' },
        tooltip: {},
        xAxis: { data: ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4'] },
        yAxis: {},
        series: [{
          name: 'GPA',
          type: 'line',
          data: [3.2, 3.5, 3.7, 3.8]
        }]
      }
    }
  },
  computed: {

  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_enrollment_info();
    this.render_charts();
  },
  mounted() {

  },
  methods: {
    render_charts() {
      const chartDom = document.querySelector('.chart');
      const myChart = echarts.init(chartDom);
      myChart.setOption(this.performanceChartOptions);
    },
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async get_user_info() {
      this.user_info = await api.get(`/api/users/info/${this.user_id}`);
    },
    async get_enrollment_info() {
      this.enrollment = await api.get(`/api/enrollment/${this.user_id}`);
      const {term_id, program_id} = this.enrollment;
      await this.get_term(term_id);
      await this.get_program(program_id);
    },
    async get_term(term_id) {
      this.term = await api.get(`/api/terms/${term_id}`);
    },
    async get_program(program_id) {
      this.program = await api.get(`/api/programs/${program_id}`);
    },
  }
};
</script>

<style scoped>

.chart-container {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}

.chart {
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;
}
</style>
