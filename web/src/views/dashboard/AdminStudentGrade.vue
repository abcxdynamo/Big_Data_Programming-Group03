<template>
  <el-form ref="queryFormRef" :inline="true" :model="query_form" label-position="left" style="text-align: left;">
    <el-form-item label="Email">
      <el-input v-model="query_form.email" placeholder="Please Input Email" style="width:200px;"></el-input>
    </el-form-item>
    <el-form-item label="Course">
      <el-input v-model="query_form.course_name" placeholder="Please Input Course Name" style="width:200px;"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="queryData">查询</el-button>
      <el-button @click="resetForm">重置</el-button>
    </el-form-item>
  </el-form>
  <el-table :data="paginated_data" v-loading="loading" style="width: 100%" border>
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
    <el-table-column label="Actions">
      <template #default="scope">
        <el-button v-if="scope.row.student_is_active" type="danger" size="small"
                   @click="toggleActive(scope.row, 'deactivate')">Deactivate
        </el-button>
        <el-button v-if="!scope.row.student_is_active" type="primary" size="small"
                   @click="toggleActive(scope.row, 'activate')">Activate
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination
      v-if="student_grades.length > page_size"
      v-model:current-page="current_page"
      v-model:page-size="page_size"
      :total="student_grades.length"
      layout="total, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
  />
</template>

<script>
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import _ from 'lodash';
import {ElMessageBox, ElMessage} from 'element-plus'
import {reactive} from 'vue'

export default {
  data() {
    return {
      query_form: {},
      student_grades: [],
      current_page: 1,
      page_size: 10,
      loading: true,
    }
  },
  computed: {
    paginated_data() {
      this.loading = true;
      const start = (this.current_page - 1) * this.page_size;
      const data = this.student_grades.slice(start, start + this.page_size);
      this.loading = false;
      return data;
    },
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.query_student_grades();
  },
  mounted() {

  },
  methods: {
    handleSizeChange(size) {
      this.page_size = size;
      this.current_page = 1;
    },
    handlePageChange(page) {
      this.current_page = page;
    },
    queryData() {
      this.loading = true;
      let student_grades = reactive(this.student_grades);
      if (this.query_form.email) {
        student_grades = this.student_grades.filter(item => _.includes(item.student_email, this.query_form.email));
      }
      if (this.query_form.course_name) {
        student_grades = this.student_grades.filter(item => _.includes(item.course_name, this.query_form.course_name));
      }
      this.student_grades = student_grades;
      this.loading = false;
    },
    resetForm() {
      this.query_form = {};
      this.query_student_grades();
    },
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async query_student_grades() {
      this.loading = true;
      this.student_grades = await api.get(`/api/grades/list`);
      await this.update_students_info();
      this.loading = false;
    },
    async update_students_info(ids = []) {
      let student_grades = reactive(this.student_grades);
      let student_ids = student_grades.map(s => s["student_id"]);
      if (ids && ids.length > 0) {
        student_grades = _.filter(student_grades, s => _.includes(ids, s["student_id"]));
        student_ids = ids;
      }
      const user_infos = await this.query_user_infos(student_ids);
      _.each(student_grades, s => {
        const user = user_infos[s["student_id"]];
        s["student_name"] = user["first_name"] + " " + user["last_name"];
        s["student_email"] = user["email"];
        s["student_is_active"] = user["is_active"];
      });
    },
    async query_user_infos(user_ids) {
      const users = await api.post(`/api/users/list`, {"ids": _.uniq(user_ids)});
      return _.reduce(users, (result, user) => {
        result[user.id] = user;
        return result;
      }, {});
    },
    async toggleActive(row, op) {
      ElMessageBox.confirm(
          `Are you sure you want to ${op} this record?`,
          'WARNING',
          {
            confirmButtonText: 'Confirm',
            cancelButtonText: 'Cancel',
            type: 'warning',
          }
      ).then(async () => {
        await api.post(`/api/users/toggle_active/${row["student_id"]}`, {});
        ElMessage.success(`${op} success.`)
        await this.update_students_info(row["student_id"]);
      });
    }
  }
};
</script>
