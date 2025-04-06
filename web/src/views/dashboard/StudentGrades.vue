<template>
    <h3>Grades Overview</h3>
      <el-table :data="term_program_courses" style="width: 100%" border >
        <el-table-column prop="course_code" label="Code" width=""></el-table-column>
        <el-table-column prop="course_name" label="Name" width=""></el-table-column>
        <el-table-column prop="course_instructor" label="Instructor" width=""></el-table-column>
        <el-table-column prop="course_grade" label="Grade" width=""></el-table-column>
      </el-table>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
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
      predicted_average: null
    }
  },
  computed: {
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_enrollment_info();
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
      const term_program_courses = await api.get(`/api/term_program_courses/${term_id}/${program_id}/${this.user_id}`);
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
      const predictionData = await api.get(`/api/performance_predictions?student_id=${this.user_id}`);
      const latestPrediction = _.last(_.sortBy(predictionData, 'term_id'));
      this.predicted_average = latestPrediction ? parseFloat(latestPrediction.predicted_average) : null;
      term_program_courses.push({
        course_instructor: "Total",
        course_grade: _.sumBy(term_program_courses, "course_grade"),
      },
      {
        course_instructor: "Predicted Weighted Average",
        course_grade: this.predicted_average,
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
        result[g.tp_course_id] = g["final_grade"];
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