<template>
  <div class="admin-container">
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">logout</el-link>
    <el-card class="admin-card">
      <h2>Admin Dashboard</h2>

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
        <el-table-column prop="instructor_name" label="Instructor Name">
        </el-table-column>
        <el-table-column prop="instructor_email" label="Instructor Email">
        </el-table-column>
      </el-table>

      <h3>Student Grades</h3>
      <el-table :data="student_grades" style="width: 100%" border>
        <el-table-column prop="student_name" label="Student Name"></el-table-column>
        <el-table-column prop="student_email" label="Email"></el-table-column>
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
        <el-table-column prop="final_grade" label="Grade"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import {defineComponent, ref, onMounted} from 'vue';
import * as echarts from 'echarts';
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';

export default {
  data() {
    return {
      user_id: null,
      user_info: {},
      admin_courses: [],
      term: {},
      program: {},
      student_grades: [],
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
    }
  },
  computed: {},
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.query_instructor_courses();
    await this.query_student_grades();
    // this.render_charts();
  },
  mounted() {

  },
  methods: {
    handleLogout() {
      window.location.href = "/login";
    },
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async query_instructor_courses() {
      const instructor_courses = await api.get(`/api/instructor/courses`);
      const instructor_ids = instructor_courses.map(s => s["instructor_id"]);
      const user_infos = await this.query_user_infos(instructor_ids);
      _.each(instructor_courses, c => {
        const user = user_infos[c["instructor_id"]];
        c["instructor_name"] = user["first_name"] + " " + user["last_name"];
        c["instructor_email"] = user["email"];
      })
      this.instructor_courses = instructor_courses;
    },
    async query_student_grades() {
      const student_grades = await api.get(`/api/grades/list`);
      const student_ids = student_grades.map(s => s["student_id"]);
      const user_infos = await this.query_user_infos(student_ids);
      _.each(student_grades, s => {
        const user = user_infos[s["student_id"]];
        s["student_name"] = user["first_name"] + " " + user["last_name"];
        s["student_email"] = user["email"];
      })
      this.student_grades = student_grades;
    },
    async query_user_infos(user_ids) {
      const users = await api.post(`/api/users/list`, {"ids": _.uniq(user_ids)});
      return _.reduce(users, (result, user) => {
        result[user.id] = user;
        return result;
      }, {});
    },
  }
};
</script>

<!--<script>-->
// import { defineComponent, ref } from 'vue';
// import { ElMessage } from 'element-plus';
//
// export default {
//   name: 'AdminDashboard',
//   setup() {
//     const admin = ref({
//       name: 'Dr. Jane Smith',
//       course: 'Computer Science',
//       email: 'janesmith@example.com'
//     });
//
//     const students = ref([
//       { name: 'John Doe', email: 'johndoe@example.com', grade: 'B+', feedback: '' },
//       { name: 'Alice Johnson', email: 'alicejohnson@example.com', grade: 'A', feedback: '' },
//       { name: 'Michael Brown', email: 'michaelbrown@example.com', grade: 'B-', feedback: '' }
//     ]);
//
//     const updateGrade = (student) => {
//       console.log('Updated Student:', student);
//       ElMessage.success(`Updated grade for ${student.name}`);
//     };
//
//     return { admin, students, updateGrade };
//   }
// };
<!--</script>-->

<style scoped>
.admin-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.admin-card {
  width: 80%;
  padding: 20px;
}
</style>
