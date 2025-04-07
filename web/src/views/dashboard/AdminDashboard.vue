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
          <el-option label="Students Per Program" value="top" />
          <el-option label="Student-Instructor Distribution" value="distribution" />
        </el-select>
      </div>

      <!-- Students Per Program Chart -->
      <div v-show="selectedChart === 'all' || selectedChart === 'top'" class="chart">
        <div ref="topChart" class="inner-chart"></div>
      </div>

      <!-- Distribution Chart -->
      <div v-show="selectedChart === 'all' || selectedChart === 'distribution'" class="chart">
        <div ref="pieChart" class="inner-chart"></div>
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
      selectedChart: "all",
      user_id: null,
      student_program_counts: [],
      instructor_courses: [],
      topChartOptions: {},
      pieChartOptions: {},
    };
  },
  async created() {
    this.user_id = this.get_login_user_id();
    await this.fetchProgramEnrollmentCounts();
    await this.query_instructor_courses();
    this.processTopPrograms();
    this.processInstructorCourseDistribution();
    this.$nextTick(() => {
      this.renderChart(this.$refs.topChart, this.topChartOptions);
      this.renderChart(this.$refs.pieChart, this.pieChartOptions);
    });
  },
  methods: {
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async fetchProgramEnrollmentCounts() {
      const all_grades = await api.get(`/api/grades/list`);
      const grouped = _.groupBy(all_grades, 'program_id');
      const program_counts = Object.keys(grouped).map(pid => ({
        program_id: pid,
        count: grouped[pid].length
      }));
      const program_names = {};
      all_grades.forEach(g => {
        if (g.program_id && g.program_name) {
          program_names[g.program_id] = g.program_name;
        }
      });
      const real = program_counts.map(p => ({
        name: program_names[p.program_id] || `Program ${p.program_id}`,
        count: p.count
      }));
      const dummy = [
        { name: 'Digital Marketing Certificate', count: 50 },
        { name: 'Software QA', count: 40 },
        { name: 'Health Office Administration', count: 35 },
        { name: 'Cloud computing', count: 70 },
        { name: 'IT Support Services', count: 28 },
        { name: 'Food Processing Techniques', count: 24 },
        { name: 'Construction Fundamentals', count: 30 },
        { name: 'Applied Manufacturing', count: 20 },
        { name: 'Green Building Techniques', count: 18 },
        { name: 'Project Management', count: 82 }
      ];
      this.student_program_counts = [...real, ...dummy];
    },
    processTopPrograms() {
      const sorted = _.orderBy(this.student_program_counts, 'count', 'desc').slice(0, 10);
      this.topChartOptions = {
        title: { text: "Top 10 Programs by Student Enrollment", left: "center", textStyle: { fontSize: 12 } },
        tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
        xAxis: { type: "value", name: "Students Enrolled", nameLocation: "middle", nameGap: 25,},
        yAxis: {
          type: "category",
          data: sorted.map(p => p.name),
          inverse: true,
          axisLabel: {
            fontSize: 10,
            interval: 0,       
            lineHeight: 14,  
            overflow: 'break',
          },
        },
        grid: {left: 200, right: 20, top: 50, bottom: 50},
        series: [
          {
            type: "bar",
            data: sorted.map(p => p.count),
            label: { show: true, position: "right" },
            itemStyle: { color: "#4caf50" },
          }
        ]
      };
    },

    async query_instructor_courses() {
      const courses = await api.get(`/api/instructor/courses`);
      const instructor_ids = courses.map(c => c.instructor_id);
      const user_infos = await this.query_user_infos(instructor_ids);
      this.instructor_courses = courses.map(c => ({
        ...c,
        instructor_name: `${user_infos[c.instructor_id]?.first_name || ""} ${user_infos[c.instructor_id]?.last_name || ""}`
      }));
    },

    async query_user_infos(user_ids) {
      const users = await api.post(`/api/users/list`, { ids: _.uniq(user_ids) });
      return _.reduce(users, (result, user) => {
        result[user.id] = user;
        return result;
      }, {});
    },

    processInstructorCourseDistribution() {
      const grouped = _.countBy(this.instructor_courses, "instructor_name");
      const data = Object.keys(grouped).map(name => ({ name, value: grouped[name] }));
      this.pieChartOptions = {
        title: { text: "Student-Instructor Distribution", left: "center", textStyle: { fontSize: 12 } },
        tooltip: { trigger: "item", formatter: "{b}: {c} courses ({d}%)" },
        series: [
          {
            type: "pie",
            radius: "60%",
            data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
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
      if (dropdown) dropdown.style.display = "none";
      const opt = {
        margin: 0.5,
        filename: `Admin_Report.pdf`,
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: "in", format: "a4", orientation: "portrait" },
      };
      html2pdf().set(opt).from(element).save().then(() => {
        if (dropdown) dropdown.style.display = "block";
      });
    },
  },
};
</script>
<style scoped>
.chart {
  display: flex;
  justify-content: center; /* Center chart inside */
  align-items: center;
  width: 100%;
  height: 300px;
  margin-top: 20px;
  overflow: visible;
}

.inner-chart {
  width: 50%;
  height: 100%;
  min-width: 500px; 
}
</style>
