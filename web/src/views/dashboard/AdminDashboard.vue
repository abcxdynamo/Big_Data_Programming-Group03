<template>
  <div>
    <div ref="reportRef" id="admin-dashboard">
      <h3>College Information</h3>
      <el-descriptions border>
        <el-descriptions-item label="Programs">300</el-descriptions-item>
        <el-descriptions-item label="Students">30000</el-descriptions-item>
        <el-descriptions-item label="Instructors">1500</el-descriptions-item>
      </el-descriptions>

      <h3>Analysis</h3>
      <div ref="chartDropdown" style="margin: 16px 0;">
        <el-select v-model="selectedChart" placeholder="Select Chart to Display" style="width: 250px;">
          <el-option label="All" value="all" />
          <el-option label="Top Performing Students" value="top" />
          <el-option label="Student-Instructor Distribution" value="distribution" />
        </el-select>
      </div>

      <!-- Top Performers Chart -->
      <div v-show="selectedChart === 'all' || selectedChart === 'top'" class="chart">
        <div ref="topChart" style="width: 100%; height: 100%;"></div>
      </div>

      <!-- Distribution Chart -->
      <div v-show="selectedChart === 'all' || selectedChart === 'distribution'" class="chart">
        <div ref="pieChart" style="width: 100%; height: 100%;"></div>
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
import * as echarts from 'echarts';
import html2pdf from 'html2pdf.js';

export default {
  data() {
    return {
      selectedChart: 'all',
      user_id: null,
      student_grades: [],
      instructor_courses: [],
      topChartOptions: {},
      pieChartOptions: {},
    }
  },
  computed: {
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.query_student_grades();
    await this.query_instructor_courses();
    this.processTopStudents();
    this.processInstructorCourseDistribution();
    this.$nextTick(() => {
      this.renderChart(this.$refs.topChart, this.topChartOptions);
      this.renderChart(this.$refs.pieChart, this.pieChartOptions);
    });

  },
  mounted() {
  },
  methods: {
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async query_student_grades() {
      const all_grades = await api.get(`/api/grades/list`);
      const grouped = _.chain(all_grades).groupBy('student_id').map((entries, student_id) => entries[0]).value();
      this.student_grades = await this.update_students_info(grouped);
    },
    async update_students_info(students) {
      const student_ids = students.map(s => s["student_id"]);
      const user_infos = await this.query_user_infos(student_ids);
      return students.map(s => {
        const user = user_infos[s["student_id"]];
        return {
          ...s,
          student_name: `${user?.first_name || ''} ${user?.last_name || ''}`,
          student_email: user?.email || '',
        };
      });
    },
    async query_instructor_courses() {
      const courses = await api.get(`/api/instructor/courses`);
      this.instructor_courses = await this.update_instructors_info(courses);
    },
    async update_instructors_info(courses) {
      const instructor_ids = courses.map(c => c["instructor_id"]);
      const user_infos = await this.query_user_infos(instructor_ids);
      return courses.map(c => {
        const user = user_infos[c["instructor_id"]];
        return {
          ...c,
          instructor_name: `${user?.first_name || ''} ${user?.last_name || ''}`,
        };
      });
    },
    async query_user_infos(user_ids) {
      const users = await api.post(`/api/users/list`, { ids: _.uniq(user_ids) });
      return _.reduce(users, (result, user) => {
        result[user.id] = user;
        return result;
      }, {});
    },
    processTopStudents() {
      const sorted = _.orderBy(this.student_grades, 'final_grade', 'desc').slice(0, 10);
      this.topChartOptions = {
        title: { text: 'Top Performing Students', left: 'center', textStyle: { fontSize: 12 } },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        xAxis: { type: 'value', max: 100, name: 'Grade' },
        yAxis: {
          type: 'category',
          data: sorted.map(s => s.student_name),
          inverse: true
        },
        series: [{
          type: 'bar',
          data: sorted.map(s => s.final_grade),
          label: { show: true, position: 'right' },
          itemStyle: { color: '#4caf50' }
        }]
      };
    },
    processInstructorCourseDistribution() {
      const grouped = _.countBy(this.instructor_courses, 'instructor_name');
      const data = Object.keys(grouped).map(name => ({
        name,
        value: grouped[name]
      }));
      this.pieChartOptions = {
        title: { text: 'Instructor-Course Distribution', left: 'center', textStyle: { fontSize: 12 } },
        tooltip: { trigger: 'item', formatter: '{b}: {c} courses ({d}%)' },
        series: [{
          type: 'pie',
          radius: '60%',
          data,
          emphasis: {
            itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
          }
        }]
      };
    },
    renderChart(dom, option) {
      if (dom && option && option.series) {
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
        filename: `Admin_Report.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'a4', orientation: 'portrait' }
      };
      html2pdf().set(opt).from(element).save().then(() => {
        if (dropdown) dropdown.style.display = 'block';
      });
    }
  }
}
</script>
<style scoped>
.chart {
  display: flex;
  justify-content: center;
  width: 100%;
  height: 300px;
  margin-top: 20px;
  overflow: visible;
}
</style>