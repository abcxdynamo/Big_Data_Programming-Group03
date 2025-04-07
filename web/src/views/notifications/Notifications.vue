<template>
  <div class="notifications-container">
    <img src="@/assets/applogo.png" alt="App Icon" class="app-icon" @click="gotoHomePage()" style="cursor: pointer;" />
    <div style="position:absolute;top:11px;right:82px;">
      <NotificationButton ref="notifyBtn"/>
    </div>
    <el-link style="position:absolute;top:10px;right:20px;" @click="handleLogout">
      <el-icon><SwitchButton/></el-icon>Logout
    </el-link>
    <el-card class="notifications-card">
      <h2>Notifications</h2>
      <el-table :data="paginated_data" v-loading="loading" style="width: 100%" border :row-class-name="tableRowClassName">
        <el-table-column prop="create_time_str" label="Time" width="200"></el-table-column>
        <el-table-column prop="title" label="Title" width="250"></el-table-column>
        <el-table-column prop="content" label="Content" show-overflow-tooltip></el-table-column>
        <el-table-column label="Actions" width="150">
          <template #default="scope">
            <el-button v-if="!scope.row.read_status" type="primary" size="small" @click="readNotification(scope.row)">Read</el-button>
          </template>
        </el-table-column>
      </el-table>
      <p class = "backbtn">Click on logo to go back!</p>
      <el-pagination
        v-if="notifications.length > page_size"
        v-model:current-page="current_page"
        v-model:page-size="page_size"
        :total="notifications.length"
        layout="total, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </el-card>
  </div>
</template>

<script>

import {SwitchButton} from "@element-plus/icons-vue";
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import router from "@/router/index.js";
import NotificationButton from "@/views/notifications/NotificationButton.vue";
import _ from "lodash"

import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
dayjs.extend(utc)
dayjs.extend(timezone)

export default {
  components: {NotificationButton, SwitchButton},
  data() {
    return {
      user_id: null,
      notifications: [],
      current_page: 1,
      page_size: 10,
      loading: true,
    }
  },
  computed: {
    paginated_data() {
      this.loading = true;
      const start = (this.current_page - 1) * this.page_size;
      const data = this.notifications.slice(start, start + this.page_size);
      this.loading = false;
      return data;
    },
  },
  async created() {
    this.user_id = this.get_login_user_id();
    await this.get_notifications();
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
    tableRowClassName({row, rowIndex}) {
      if (!row.read_status) {
        return 'unread-row';
      }
      return '';
    },
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async get_notifications() {
      const notifications = await api.get(`/api/notifications/list/${this.user_id}`);
      _.each(notifications, n => {
        const localTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
        n["create_time_str"] = dayjs.utc(n["create_time"]).tz(localTZ).format('YYYY-MM-DD HH:mm:ss');
      })
      this.notifications = notifications;
    },
    async readNotification(row) {
      await api.post(`/api/notifications/${row.id}/read`)
      row.read_status = true;
      await this.$refs["notifyBtn"].count_news();
    },
    gotoHomePage() {
      router.push("/");
    },
    handleLogout() {
      window.location.href = "/login";
    },
  }
};
  //font-weight: bold;

</script>

<style>
.notifications-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.notifications-card {
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
.el-table .unread-row {
  font-weight: bold;
}
.backbtn{
  font-size: 12px;
  font-style: italic;
  color: #555;
  margin: 16px 0;
  text-align: center;
}
</style>

