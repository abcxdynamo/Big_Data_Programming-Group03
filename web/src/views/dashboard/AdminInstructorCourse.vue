<template>
  <el-table :data="paginated_data" style="width: 100%" border>
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
    <el-table-column label="Actions">
      <template #default="scope">
        <el-button v-if="scope.row.instructor_is_active" type="danger" size="small"
                   @click="toggleActive(scope.row, 'deactivate')">Deactivate
        </el-button>
        <el-button v-if="!scope.row.instructor_is_active" type="primary" size="small"
                   @click="toggleActive(scope.row, 'activate')">Activate
        </el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination
      v-if="instructor_courses.length > page_size"
      v-model:current-page="current_page"
      v-model:page-size="page_size"
      :total="instructor_courses.length"
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
      instructor_courses: [],
      current_page: 1,
      page_size: 10,
    }
  },
  computed: {
    paginated_data() {
      const start = (this.current_page - 1) * this.page_size;
      return this.instructor_courses.slice(start, start + this.page_size);
    },
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
    await this.query_instructor_courses();
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
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async query_instructor_courses() {
      this.instructor_courses = await api.get(`/api/instructor/courses`);
      await this.update_instructors_info();
    },
    async update_instructors_info(ids = []) {
      let instructor_courses = reactive(this.instructor_courses);
      let instructor_ids = instructor_courses.map(i => i["instructor_id"]);
      if (ids && ids.length > 0) {
        instructor_courses = _.filter(instructor_courses, i => _.includes(ids, i["instructor_id"]));
        instructor_ids = ids;
      }
      const user_infos = await this.query_user_infos(instructor_ids);
      _.each(instructor_courses, c => {
        const user = user_infos[c["instructor_id"]];
        c["instructor_name"] = user["first_name"] + " " + user["last_name"];
        c["instructor_email"] = user["email"];
        c["instructor_is_active"] = user["is_active"];
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
        await api.post(`/api/users/toggle_active/${row["instructor_id"]}`, {});
        ElMessage.success(`${op} success.`)
        await this.update_instructors_info(row["instructor_id"]);
      });
    }
  }
};
</script>
