<template>
  <div class="student-container">
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">logout</el-link>
    <el-card class="student-card">
      <h2>Student Dashboard</h2>

      <el-descriptions title="Student Information" :column="2" border>
        <el-descriptions-item label="Name">{{ user_info.first_name }} {{ user_info.last_name }}</el-descriptions-item>
        <el-descriptions-item label="Email">{{ user_info.email }}</el-descriptions-item>
        <el-descriptions-item label="Term">{{ term.year }} {{ term.season }}</el-descriptions-item>
        <el-descriptions-item label="Program">{{ program.name }}</el-descriptions-item>
      </el-descriptions>

      <h3>Grades Overview</h3>
      <el-table :data="term_program_courses" style="width: 100%" border >
        <el-table-column prop="course_code" label="Code" width=""></el-table-column>
        <el-table-column prop="course_name" label="Name" width=""></el-table-column>
        <el-table-column prop="course_instructor" label="Instructor" width=""></el-table-column>
        <el-table-column prop="course_grade" label="Grade" width=""></el-table-column>
      </el-table>

      <h3>Performance Trends</h3>
      <div class="chart-container">
<!--        <ECharts :option="performanceChartOptions" class="chart" />-->
        <div class="chart" ></div>
      </div>

      <h3>Co-op Prediction</h3>
      <el-progress :percentage="coop.coopPrediction" status="success" />

      <h3>Career Advice</h3>
      <el-alert :title="coop.careerAdvice" type="info" show-icon />
    </el-card>
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
      term_program_courses: [],
      // student: {
      //   name: 'John Doe',
      //   course: 'Computer Science',
      //   email: 'johndoe@example.com',
      //   grades: [
      //     { subject: 'Math', grade: 'A' },
      //     { subject: 'Programming', grade: 'B+' },
      //     { subject: 'Data Science', grade: 'A-' }
      //   ],
      //   coopPrediction: 85,
      //   careerAdvice: 'Consider specializing in AI and Data Science for better opportunities.'
      // },
      coop: {
        coopPrediction: 85,
        careerAdvice: 'Consider specializing in AI and Data Science for better opportunities.'
      },
      performanceChartOptions: {
        width: 600,
        height:400,
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
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_enrollment_info();
    this.render_charts();
  },
  mounted() {

  },
  methods: {
    handleLogout() {
      window.location.href="/login";
    },
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
      await this.get_term_program_courses(term_id, program_id);
    },
    async get_term(term_id) {
      this.term = await api.get(`/api/terms/${term_id}`);
    },
    async get_program(program_id) {
      this.program = await api.get(`/api/programs/${program_id}`);
    },
    async get_term_program_courses(term_id, program_id) {
      const term_program_courses = await api.get(`/api/term_program_courses/${term_id}/${program_id}`);
      const course_ids = term_program_courses.map(course => course.id);
      const courses = await this.get_courses(course_ids);
      const course_grades = await this.get_grades(term_id, program_id, this.user_id);
      const instructor_ids = term_program_courses.map(course => course.instructor_id);
      const instructors = await this.get_instructors(instructor_ids);
      _.each(term_program_courses, tpc => {
        const course_id = tpc.course_id;
        tpc.course_code = courses[course_id]["code"];
        tpc.course_name = courses[course_id]["name"];
        tpc.course_grade = course_grades[course_id];
        const instructor = instructors[tpc.instructor_id];
        tpc.course_instructor = instructor["first_name"] + ' ' + instructor["last_name"];
      });
      term_program_courses.push({
        course_code: "",
        course_name: "Total",
        course_grade: _.sumBy(term_program_courses, "course_grade"),
      })
      this.term_program_courses = term_program_courses;
    },
    async get_courses(ids) {
      const courses = await api.post(`/api/courses/list`, {"ids": ids});
      return _.reduce(courses, (result, c) => {
        result[c.id] = c;
        return result;
      }, {})
    },
    async get_grades(term_id, program_id, student_id) {
      const grades = await api.get(`/api/grades/${term_id}/${program_id}?student_id=${student_id}`);
      return _.reduce(grades, (result, g) => {
        result[g.course_id] = g["final_grade"];
        return result;
      }, {})
    },
    async get_instructors(instructor_ids) {
      const instructors = await api.post(`/api/users/list`, {"ids": instructor_ids});
      return _.reduce(instructors, (result, instructor) => {
        result[instructor.id] = instructor;
        return result;
      }, {});
    },
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
