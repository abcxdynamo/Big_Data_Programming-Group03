<template>
  <div class="admin-container">
    <img src="@/assets/applogo.png" alt="App Icon" class="app-icon" />
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">
      <el-icon><SwitchButton/></el-icon>logout
    </el-link>
    <el-card class="admin-card">
      <h2>Admin Dashboard</h2>
      <el-tabs v-model="activeTabName" class="admin-tabs">
        <el-tab-pane label="Dashboard" name="Dashboard">
          <AdminDashboard></AdminDashboard>
        </el-tab-pane>
        <el-tab-pane label="InstructorCourses" name="InstructorCourses">
          <AdminInstructorCourse></AdminInstructorCourse>
        </el-tab-pane>
        <el-tab-pane label="StudentGrades" name="StudentGrades">
          <AdminStudentGrade></AdminStudentGrade>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import {SwitchButton} from '@element-plus/icons-vue';
import AdminDashboard from "@/views/dashboard/AdminDashboard.vue";
import AdminInstructorCourse from "@/views/dashboard/AdminInstructorCourse.vue";
import AdminStudentGrade from "@/views/dashboard/AdminStudentGrade.vue";

export default {
  components: {AdminDashboard, AdminInstructorCourse, AdminStudentGrade, SwitchButton},
  data() {
    return {
      activeTabName: "Dashboard",
    }
  },
  computed: {
  },
  async created() {
  },
  mounted() {
  },
  methods: {
    handleLogout() {
      window.location.href = "/login";
    },
  }
};
</script>

<style scoped>
.admin-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.admin-card {
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