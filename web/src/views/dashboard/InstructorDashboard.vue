<template>
  <div>
    <div ref="reportRef" id="instructor-dashboard">
      <h3>Instructor Information</h3>
      <el-descriptions border>
        <el-descriptions-item label="Name">{{ user_info["first_name"] }} {{ user_info["last_name"] }}</el-descriptions-item>
        <el-descriptions-item label="Email">{{ user_info["email"] }}</el-descriptions-item>
      </el-descriptions>

      <h3>Instructor Courses</h3>
      <el-table :data="instructor_courses" style="width: 100%" border>
        <el-table-column prop="term" label="Term">
          <template #default="scope">
            {{ scope.row.term_year }}-{{ scope.row.term_season }}-{{ scope.row.term_section }}
          </template>
        </el-table-column>
        <el-table-column prop="program_name" label="Program">
          <template #default="scope">
            {{ scope.row.program_code }}-{{ scope.row.program_name }}
          </template>
        </el-table-column>
        <el-table-column prop="course" label="Course">
          <template #default="scope">
            {{ scope.row.course_code }}-{{ scope.row.course_name }}
          </template>
        </el-table-column>
      </el-table>
      <h3>Analysis</h3>
      <div ref="chartDropdown" style="margin: 16px 0;">
        <el-select v-model="selectedChart" placeholder="Select Chart to Display" style="width: 250px;">
          <el-option label="All" value="all" />
          <el-option label="Average Grades by Course" value="average" />
          <el-option label="Attendance vs Grade" value="attendance" />
          <el-option label="Top Students per Course" value="topstudents" />
          <el-option label="Poor Performance Students" value="bottomstudents" />
        </el-select>
      </div>
      <div v-show="selectedChart === 'all' || selectedChart === 'average'" class="chart">
        <div ref="avgChart" style="height: 100%; width: 50%;"></div>
      </div>

      <div v-show="selectedChart === 'all' || selectedChart === 'attendance'" class="chart">
        <div ref="scatterChart" style="height: 100%; width: 50%;"></div>
      </div>
      <div v-show="selectedChart === 'all' || selectedChart === 'topstudents'" class="chart">
        <div ref="groupedChart" style="height: 100%; width: 50%;"></div>
      </div>
      <div v-show="selectedChart === 'all' || selectedChart === 'bottomstudents'" class="chart">
        <div ref="bottomGroupedChart" style="height: 100%; width: 50%;"></div>
      </div>
    </div>

    <el-button type="primary" @click="exportDashboardReport" style="margin-top: 16px;">
      Export Dashboard Report
    </el-button>
  </div>
</template>

<script>
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';
import {ElMessage} from "element-plus";
import * as echarts from 'echarts';
import html2pdf from 'html2pdf.js';

export default {
  data() {
    return {
      user_id: null,
      user_info: {},
      instructor_courses: [],
      term: {},
      program: {},
      student_grades: [],
      selectedChart: 'all',
      averageGradesChartOptions: {},
      attendanceChartOptions: {},
      groupedChartOptions: {},
      bottomGroupedChartOptions: {}
    }
  },
  computed: {},
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_instructor_courses();
    await this.query_instructor_student_grades();
    this.processAverageGrades();
    this.processAttendanceVsPerformance();
    this.processTopStudentsPerCourse();
    this.processBottomStudentsPerCourse();
    this.$nextTick(() => {
      this.renderEChart(this.$refs.avgChart, this.averageGradesChartOptions);
      this.renderEChart(this.$refs.scatterChart, this.attendanceChartOptions);
      this.renderEChart(this.$refs.groupedChart, this.groupedChartOptions);
      this.renderEChart(this.$refs.bottomGroupedChart, this.bottomGroupedChartOptions);
    });
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
    async get_instructor_courses() {
      this.instructor_courses = await api.get(`/api/instructor/courses?instructor_id=${this.user_id}`);
    },
    async query_instructor_student_grades() {
    const allGrades = [];
      console.log("hi")
      for (const course of this.instructor_courses) {
        const courseId = course.course_id;
        const response = await api.get(
          `/api/grades/list?instructor_id=${this.user_id}&course_id=${courseId}`
        );

        // Optionally get user info if you want to display student names/emails
        const student_ids = response.map(s => s.student_id);
        const user_infos = await this.query_user_infos(student_ids);

        response.forEach(s => {
          allGrades.push({
            ...s,
            course_id: course.course_id,
            course_name: course.course_name,
            course_code: course.course_code,
            final_grade: s.final_grade,
            attendance_percent: s.attendance_percent,
            student_name: `${user_infos[s.student_id]?.first_name || ''} ${user_infos[s.student_id]?.last_name || ''}`,
            student_email: user_infos[s.student_id]?.email || ''
          });
        });
      }

      this.student_grades = allGrades;
    },

    async query_user_infos(user_ids) {
      const users = await api.post(`/api/users/list`, { ids: _.uniq(user_ids) });
      return _.reduce(users, (result, user) => {
        result[user.id] = user;
        return result;
      }, {});
    },
    processAverageGrades() {
      const grouped = _.groupBy(this.student_grades, 'course_name');
      const avgGrades = Object.keys(grouped).map(course => {
        const grades = grouped[course].map(s => s.final_grade).filter(g => g !== null);
        return {
          course,
          avg: _.mean(grades).toFixed(2)
        };
      });
      this.averageGradesChartOptions = {
        title: { text: 'Average Grade per Course', left: 'center', textStyle: { fontSize: 12 } },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}%'
        },
        xAxis: { name: 'Courses', type: 'category', data: avgGrades.map(item => item.course) , nameLocation: "middle", nameGap: 35},
        yAxis: { name: 'Grade', type: 'value', min: 0, max: 100 , nameLocation: "middle", nameGap: 35},
        series: [{
          type: 'bar',
          data: avgGrades.map(item => parseFloat(item.avg)),
          itemStyle: { color: '#5470c6' },
          label: { show: true, position: 'top' }
        }]
      };
    },
    processAttendanceVsPerformance() {
      const filtered = this.student_grades.filter(s => s.attendance_percent != null && s.final_grade != null);
      this.attendanceChartOptions = {
        title: { text: 'Attendance vs Grade', left: 'center', textStyle: { fontSize: 12 } },
        tooltip: {
          trigger: 'item',
          formatter: params => `Attendance: ${params.value[0]}%<br/>Grade: ${params.value[1]}%`
        },
        xAxis: { name: 'Attendance (%)', type: 'value', min: 0, max: 100, nameLocation: "middle", nameGap: 35},
        yAxis: { name: 'Grade', type: 'value', min: 0, max: 100 , nameLocation: "middle", nameGap: 35},
        series: [{
          symbolSize: 10,
          type: 'scatter',
          data: filtered.map(s => [s.attendance_percent, s.final_grade]),
          itemStyle: { color: '#91cc75' }
        }]
      };
    },
    processTopStudentsPerCourse() {
      const grouped = _.groupBy(this.student_grades, 'course_name');
      const courses = Object.keys(grouped);

      // Get top 3 students per course and collect unique names
      const topStudentsPerCourse = {};
      const allStudentNames = new Set();

      courses.forEach(course => {
        const top3 = _.orderBy(grouped[course], 'final_grade', 'desc').slice(0, 3);
        topStudentsPerCourse[course] = top3;
        top3.forEach(s => allStudentNames.add(s.student_name));
      });

      const studentList = Array.from(allStudentNames);

      // Build one series per student (only if they appear in at least one course)
      const series = studentList.map(student => ({
        name: student,
        type: 'bar',
        data: courses.map(course => {
          const studentGrade = topStudentsPerCourse[course].find(s => s.student_name === student);
          return studentGrade ? studentGrade.final_grade : 0;
        }),
        barGap: '0%',
        barCategoryGap: '50%'
      }));

      this.groupedChartOptions = {
        title: {
          text: 'Top 3 Students Per Course',
          left: 'center',
          textStyle: { fontSize: 12 }
        },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: {
          type: 'scroll',
          orient: 'vertical',        // Vertical layout
          left: 'center',            // Center horizontally
          top: 'middle',             // Middle vertically
          itemWidth: 10,
          itemHeight: 10,
          textStyle: {
            fontSize: 10
          },
          pageIconSize: 10,
          pageTextStyle: {
            fontSize: 9
          }
        },
        grid: { left: 60, right: 30, top: 50, bottom: 50 },
        xAxis: {
          type: 'category',
          data: courses,
          axisLabel: { interval: 0, rotate: 0, fontSize: 10 },
          name: 'Courses',
          nameLocation: 'middle',
          nameGap: 35
        },
        yAxis: {
          type: 'value',
          name: 'Grade',
          min: 0,
          max: 100,
          nameLocation: 'middle',
          nameGap: 30
        },
        series
      };
    },
    processBottomStudentsPerCourse() {
      const grouped = _.groupBy(this.student_grades, 'course_name');
      const courses = Object.keys(grouped);

      const bottomStudentsPerCourse = {};
      const allStudentNames = new Set();

      courses.forEach(course => {
        const bottom3 = _.orderBy(grouped[course], 'final_grade', 'asc').slice(0, 3);
        bottomStudentsPerCourse[course] = bottom3;
        bottom3.forEach(s => allStudentNames.add(s.student_name));
      });

      const studentList = Array.from(allStudentNames);

      const series = studentList.map(student => ({
        name: student,
        type: 'bar',
        data: courses.map(course => {
          const studentGrade = bottomStudentsPerCourse[course].find(s => s.student_name === student);
          return studentGrade ? studentGrade.final_grade : 0;
        }),
        barGap: '0%',
        barCategoryGap: '50%'
      }));

      this.bottomGroupedChartOptions = {
        title: {
          text: 'Bottom 3 Students Per Course',
          left: 'center',
          textStyle: { fontSize: 12 }
        },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          left: 'center',
          top: 'middle',
          itemWidth: 10,
          itemHeight: 10,
          textStyle: { fontSize: 10 },
          pageIconSize: 10,
          pageTextStyle: { fontSize: 9 }
        },
        grid: { left: 60, right: 30, top: 50, bottom: 50 },
        xAxis: {
          type: 'category',
          data: courses,
          axisLabel: { interval: 0, rotate: 0, fontSize: 10 },
          name: 'Courses',
          nameLocation: 'middle',
          nameGap: 35
        },
        yAxis: {
          type: 'value',
          name: 'Grade',
          min: 0,
          max: 100,
          nameLocation: 'middle',
          nameGap: 30
        },
        series
      };
    },
    renderEChart(dom, option) {
      if (dom) {
        const chart = echarts.init(dom);
        chart.setOption(option);
      }
    },
    exportDashboardReport() {
      const element = this.$refs.reportRef;
      const dropdown = this.$refs.chartDropdown;
      if (dropdown) dropdown.style.display = 'none';
      const opt = {
        margin: 0.5,
        filename: `Instructor_Report_${this.user_id}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
      };
      html2pdf().set(opt).from(element).save().then(() => {
        if (dropdown) dropdown.style.display = 'block';
      });
    }
  }
};
</script>
<style scoped>
.chart {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 300px;
  margin-top: 20px;
  overflow: visible;
}
</style>