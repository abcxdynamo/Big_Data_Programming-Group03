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
            <div class="bar-chart-container">
              <div class="avg-bar-chart"></div>
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
      chartInstance: null,
      performanceChartOptions: {
        tooltip: {},
        xAxis: { type: 'category', data: [] },
        yAxis: { type: 'value', min: 0, max: 4, name: 'GPA' },
        series: [{
          name: 'Predicted GPA',
          type: 'line',
          data: []
        }],
        lineStyle: {
          color: 'blue', width: 3
        },
        label: {
          show: true, position: 'top', formatter: '{c}', fontSize: 12, formatter: (params) => { return params.dataIndex === 0 ? '' : params.value;}
        },
        title: {
          text: 'GPA Trends', left: 'center', top: '5', textStyle: { fontSize: 12 }
        },
      },
      barChartInstance: null,
      averageComparisonOptions: {
        tooltip: {},
        xAxis: {
          type: 'category',
          data: ['Current Average', 'Predicted Average']
        },
        yAxis: {
          type: 'value',
          max: 100
        },
        series: [{
          type: 'bar',
          data: [],
          itemStyle: {
            color: '#4caf50'
          },
          label: {
            show: true,
            position: 'top',
            fontWeight: 'bold'
          }
        }],
        title: {
          text: 'Weighted Average Trends', left: 'center', top: '5', textStyle: { fontSize: 12 }
        },
      },
    }
  },
  computed: {

  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_enrollment_info();
    await this.load_prediction_data();
    await this.load_average_comparison();
    // this.render_charts();
  },
  mounted() {

  },
  methods: {
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
    async load_prediction_data() {
      const response = await api.get(`/api/performance_predictions?student_id=${this.user_id}`);
      const sorted = _.sortBy(response, 'term_id');

      const xLabels = ['Current'].concat(sorted.map((_, index) => `Semester End`));
      const gpaData = [0].concat(sorted.map(p => parseFloat(p.predicted_gpa)));

      this.performanceChartOptions.xAxis.data = xLabels;
      this.performanceChartOptions.series[0].data = gpaData;

      this.render_charts();  // draw chart after updating options
    },
    init_chart() {
      const chartDom = document.querySelector('.chart');
      this.chartInstance = echarts.init(chartDom);
    },
    render_charts() {
      if (this.chartInstance) {
        this.chartInstance.setOption(this.performanceChartOptions);
      } else {
        this.init_chart();
        this.chartInstance.setOption(this.performanceChartOptions);
      }
    },
    async load_average_comparison() {
      const predictionData = await api.get(`/api/performance_predictions?student_id=${this.user_id}`);
      const latestPrediction = _.last(_.sortBy(predictionData, 'term_id'));
      const predictedAvg = latestPrediction ? parseFloat(latestPrediction.predicted_average) : 0;
      const enrollment = await api.get(`/api/enrollment/${this.user_id}`);
      const { term_id, program_id } = enrollment;
      const termCourses = await api.get(`/api/term_program_courses/${term_id}/${program_id}/${this.user_id}`);
      const courseGrades = await api.get(`/api/grades/${term_id}/${program_id}?student_id=${this.user_id}`);
      const gradesMap = _.reduce(courseGrades, (acc, g) => {
        acc[g.tp_course_id] = g.final_grade;
        return acc;
      }, {});
      let weightedSum = 0;
      let totalCredits = 0;
      for (const course of termCourses) {
        const grade = gradesMap[course.id];
        const credits = course.credits;
        if (!isNaN(grade) && credits) {
          weightedSum += grade * credits;
          totalCredits += credits;
        }
      }
      const currentAvg = totalCredits > 0 ? (weightedSum / totalCredits): 0;
      this.averageComparisonOptions.series[0].data = [
        parseFloat(currentAvg.toFixed(2)),
        parseFloat(predictedAvg.toFixed(2))
      ];
      this.render_bar_chart();
    },
    render_bar_chart() {
      const chartDom = document.querySelector('.avg-bar-chart');
      this.barChartInstance = echarts.init(chartDom);
      this.barChartInstance.setOption(this.averageComparisonOptions);
    }
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

.bar-chart-container {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}

.avg-bar-chart {
  width: 100%;
  height: 100%;
}
</style>
