<template>
  <div class="student-container">
    <el-card class="student-card">
      <h2>Student Dashboard</h2>
      
      <el-descriptions title="Student Information" :column="2" border>
        <el-descriptions-item label="Name">{{ student.name }}</el-descriptions-item>
        <el-descriptions-item label="Course">{{ student.course }}</el-descriptions-item>
        <el-descriptions-item label="Email">{{ student.email }}</el-descriptions-item>
      </el-descriptions>

      <h3>Grades Overview</h3>
      <el-table :data="student.grades" style="width: 100%" border >
        <el-table-column prop="subject" label="Course" width=""></el-table-column>
        <el-table-column prop="grade" label="Grade" width=""></el-table-column>
      </el-table>

      <h3>Performance Trends</h3>
      <div class="chart-container">
        <ECharts :option="performanceChartOptions" class="chart" />
      </div>

      <h3>Co-op Prediction</h3>
      <el-progress :percentage="student.coopPrediction" status="success" />

      <h3>Career Advice</h3>
      <el-alert :title="student.careerAdvice" type="info" show-icon />
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import * as echarts from 'echarts';

export default {
  data() {
    return {
      student: {
        name: 'John Doe',
        course: 'Computer Science',
        email: 'johndoe@example.com',
        grades: [
          { subject: 'Math', grade: 'A' },
          { subject: 'Programming', grade: 'B+' },
          { subject: 'Data Science', grade: 'A-' }
        ],
        coopPrediction: 85,
        careerAdvice: 'Consider specializing in AI and Data Science for better opportunities.'
      },
      performanceChartOptions: {
        // width: 1000,
        // height:1000,
        title: { text: 'Performance Trends' },
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
  created() {
  },
  mounted() {
    const chartDom = document.querySelector('.chart');
    const myChart = echarts.init(chartDom);
    myChart.setOption(this.performanceChartOptions);
  },
  methods: {
  }
};
</script>

<style scoped>
.student-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.student-card {
  width: 80%;
  padding: 20px;
}

.chart-container {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
