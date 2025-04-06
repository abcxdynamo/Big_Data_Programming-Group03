<template>
    <h3>Student Grades & Attendance</h3>
    <el-select v-model="selectedCourse" placeholder="Select a course" @change="onCourseChange" style="margin-bottom: 16px;">
    <el-option
      v-for="course in instructor_courses"
      :key="course.course_id"
      :label="course.course_name"
      :value="course.course_id"
    />
    </el-select>
      <el-table :data="student_grades" style="width: 100%" border>
        <el-table-column prop="student_name" label="Student Name" width=""></el-table-column>
        <el-table-column prop="student_email" label="Email" width=""></el-table-column>
        <el-table-column prop="final_grade" label="Grade" width="">
            <template #default="scope">
              <el-input-number 
                v-model="scope.row.edit_grade"
                @keyup.enter.native="saveChanges(scope.row)"
                :min="0"
                :max="100"
                :step="1"
                :disabled="!scope.row.editing"
                :controls="false"
              />
            </template>
          </el-table-column>
          <el-table-column prop="attendance" label="Attendance (%)" width="">
            <template #default="scope">
              <el-input-number
                v-model="scope.row.edit_attendance"
                @keyup.enter.native="saveChanges(scope.row)"
                :min="0"
                :max="100"
                :step="1"
                :disabled="!scope.row.editing"
                :controls="false"
              />
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200">
          <template #default="scope">
            <el-button
              v-if="!scope.row.editing"
              type="primary" 
              size="small"
              @click="enableEditing(scope.row)"
            >
              Edit
            </el-button>
            
            <div v-else>
              <el-button
                type="success"
                size="small"
                @click="saveChanges(scope.row)"
              >
                Save
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="cancelEditing(scope.row)"
              >
                Cancel
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
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
      selectedCourse: null,
    };
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_instructor_courses();
    if (this.instructor_courses.length > 0) {
      this.selectedCourse = this.instructor_courses[0].course_id;
      await this.query_instructor_student_data();
    }
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
    async onCourseChange() {
      await this.query_instructor_student_data();
    },
    async query_instructor_student_data() {
      if (!this.selectedCourse) return;

      try {
        const response = await api.get(
          `/api/grades/list?instructor_id=${this.user_id}&course_id=${this.selectedCourse}`
        );
        const student_ids = response.map(s => s.student_id);
        const user_infos = await this.query_user_infos(student_ids);
        this.student_grades = response.map(s => ({
          ...s,
          student_name: `${user_infos[s.student_id]?.first_name || ""} ${user_infos[s.student_id]?.last_name || ""}`,
          student_email: user_infos[s.student_id]?.email || "",
          edit_grade: s.final_grade,
          edit_attendance: s.attendance_percent,
          grade_id: s.grade_id,
          attendance_id: s.attendance_id,
          editing: false
        }));
      } catch (error) {
        console.error("Failed to load student records:", error);
      }
      // this.student_grades = student_grades;
    },
    async query_user_infos(user_ids) {
      const users = await api.post(`/api/users/list`, { ids: _.uniq(user_ids) });
      return _.reduce(users, (result, user) => {
        result[user.id] = user;
        return result;
      }, {});
    },
    enableEditing(row) {
      row.editing = true;
    },
    cancelEditing(row) {
      row.edit_grade = row.final_grade;
      row.edit_attendance = row.attendance_percent;
      row.editing = false;
    },
    async saveChanges(row) {
      try {
        // Save grade
        await api.post(`/api/grades/${row.grade_id}/update`, {
          final_grade: row.edit_grade
        });

        // Save attendance
        await api.post(`/api/attendance/${row.attendance_id}/update`, {
          attendance: row.edit_attendance
        });

        ElMessage.success("Changes saved successfully.");

        // Update UI values
        row.final_grade = row.edit_grade;
        row.attendance = row.edit_attendance;
        row.editing = false;
      } catch (err) {
        ElMessage.error("Failed to save changes.");
        console.error(err);
      }
    }
  }
};
</script>