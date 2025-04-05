<template>
    <h3>Career Recommendation</h3>
      <el-alert :title="coop.careerAdvice" type="info" show-icon />
</template>
  
<script>
import { defineComponent, ref, onMounted } from 'vue';
import * as echarts from 'echarts';
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';

export default {
  data() {
    return {
      coop: {
        coopPrediction: 85,
        careerAdvice: 'Consider specializing in AI and Data Science for better opportunities.'
      },
    }
  },
  computed: {

  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.get_user_info();
    await this.get_enrollment_info();
    this.render_charts();
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
        result[g.course_id] = g["final_grade"];
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

.chart-container {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
