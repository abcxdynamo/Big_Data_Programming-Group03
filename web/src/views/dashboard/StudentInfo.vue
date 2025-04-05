<template>
  <div class="student-container">
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">logout</el-link>
    <el-card class="student-card">
      <h2>Student Dashboard</h2>
      <el-tabs v-model="activeTabName" class="admin-tabs">
        <el-tab-pane label="Dashboard" name="Dashboard">
          <StudentDashboard></StudentDashboard>
        </el-tab-pane>
        <el-tab-pane label="Grades" name="Grades">
          <StudentGrades></StudentGrades>
        </el-tab-pane>
        <el-tab-pane label="Attendance" name="Attendance">
          <StudentAttendance></StudentAttendance>
        </el-tab-pane>
        <el-tab-pane label="Co-op Predictor" name="Co-op Predictor">
          <StudentCoopPredictor></StudentCoopPredictor>
        </el-tab-pane>
        <el-tab-pane label="Career Suggestion" name="Career Suggestion">
          <StudentCareerSuggester></StudentCareerSuggester>
        </el-tab-pane>
      </el-tabs>  
    </el-card>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';
import StudentGrades from './StudentGrades.vue';
import StudentAttendance from './StudentAttendance.vue';
import StudentDashboard from './StudentDashboard.vue';
import StudentCoopPredictor from './StudentCoopPredictor.vue';
import StudentCareerSuggester from './StudentCareerSuggester.vue';

export default {
  components: {StudentDashboard, StudentAttendance, StudentGrades, StudentCoopPredictor, StudentCareerSuggester},
  data() {
    return {
      activeTabName: "Dashboard",
    }
  },
  computed: {

  },
  mounted() {

  },
  methods: {
    handleLogout() {
      window.location.href="/login";
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
</style>
