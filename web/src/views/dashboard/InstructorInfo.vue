<template>
  <div class="instructor-container">
    <img src="@/assets/applogo.png" alt="App Icon" class="app-icon" />
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">
      <el-icon><SwitchButton/></el-icon>Logout
    </el-link>
    <el-card class="instructor-card">
      <h2>Instructor Dashboard</h2>
      <el-tabs v-model="activeTabName" class="admin-tabs">
        <el-tab-pane label="Dashboard" name="Dashboard">
          <InstructorDashboard></InstructorDashboard>
        </el-tab-pane>
        <el-tab-pane label="Student Data" name="Student Data">
          <InstructorStudentGradesAttendance></InstructorStudentGradesAttendance>
        </el-tab-pane>
      </el-tabs>        
    </el-card>
  </div>
</template>
<script>
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';
import {ElMessage} from "element-plus";
import {SwitchButton} from '@element-plus/icons-vue';
import InstructorDashboard from "./InstructorDashboard.vue";
import InstructorStudentGradesAttendance from "./InstructorStudentGradesAttendance.vue";

export default {
  components: {InstructorDashboard, InstructorStudentGradesAttendance, SwitchButton},
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
.instructor-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.instructor-card {
  width: 85%;
  padding: 20px;
}
.app-icon {
  position: absolute;
  top: 10px;
  left: 20px;
  width: 40px;
  height: 40px;
  z-index: 10;
}
.el-link .el-icon {
  margin-right: 4px;
  vertical-align: middle;
}
</style>
