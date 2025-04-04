<template>
  <div class="instructor-container">
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">logout</el-link>
    <el-card class="instructor-card">
      <h2>Instructor Dashboard</h2>

      <el-descriptions title="Instructor Information" :column="2" border>
        <el-descriptions-item label="Name">{{ user_info["first_name"] }} {{ user_info["last_name"] }}
        </el-descriptions-item>
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

      <h3>Student Grades</h3>
      <el-table :data="student_grades" style="width: 100%" border>
        <el-table-column prop="student_name" label="Student Name" width="180"></el-table-column>
        <el-table-column prop="student_email" label="Email" width="200"></el-table-column>
        <el-table-column prop="final_grade" label="Grade" width="100">
        </el-table-column>
        <el-table-column prop="feedback" label="Feedback">
          <template #default="scope">
            <el-input v-model="scope.row.edit_feedback" placeholder="Provide feedback"/>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="100">
          <template #default="scope">
            <el-button
                :disabled="(!!scope.row.edit_feedback && scope.row.edit_feedback)===(!!scope.row.grade_feedback && scope.row.grade_feedback)"
                type="primary" size="small" @click="save_grade_feedback(scope.row)">Save
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';
import {ElMessage} from "element-plus";

export default {
  data() {
    return {
      user_id: null,
      user_info: {},
      instructor_courses: [],
      term: {},
      program: {},
      student_grades: [],
    }
  },
  computed: {},
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_instructor_courses();
    await this.query_instructor_student_grades();
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
    async get_user_info() {
      this.user_info = await api.get(`/api/users/info/${this.user_id}`);
    },
    async get_instructor_courses() {
      this.instructor_courses = await api.get(`/api/instructor/courses?instructor_id=${this.user_id}`);
    },
    async query_instructor_student_grades() {
      const student_grades = await api.get(`/api/grades/list?instructor_id=${this.user_id}`);
      const student_ids = student_grades.map(s => s["student_id"]);
      const user_infos = await this.query_user_infos(student_ids);
      _.each(student_grades, s => {
        s["edit_feedback"] = s["grade_feedback"];
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
    async save_grade_feedback(row) {
      await api.post(`/api/grades/${row.grade_id}/feedback`, {"feedback": row["edit_feedback"]});
      ElMessage.success(`save success.`)
      await this.query_instructor_student_grades();
    }
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
  width: 80%;
  padding: 20px;
}
</style>
