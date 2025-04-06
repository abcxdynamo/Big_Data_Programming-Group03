<template>
  <div style="cursor:pointer;" @click="gotoNotificationPage()">
    <el-icon v-if="news_count!==0">
      <el-badge is-dot class="item">
        <BellFilled/>
      </el-badge>
    </el-icon>
    <el-icon v-if="news_count===0">
      <Bell/>
    </el-icon>
  </div>
</template>
<script>
import {defineComponent} from "vue";
import {Bell, BellFilled} from "@element-plus/icons-vue";
import localStore from "@/utils/store.js";
import api from "@/utils/api.js";
import router from "@/router/index.js";

export default defineComponent({
  name: 'NotificationButton',
  components: {Bell, BellFilled},
  data() {
    return {
      polling: false,
      user_id: null,
      news_count: 0,
    }
  },
  async created() {
    this.user_id = this.get_login_user_id();
    await this.count_news();
  },
  mounted() {
    this.polling = true;
  },
  unmounted() {
    this.polling = false;
  },
  methods: {
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
    async count_news() {
      const res = await api.get(`/api/notifications/count_news/${this.user_id}`);
      this.news_count = res["news_count"];
      if (this.news_count === 0) {
        await this.check_news();
      }
    },
    async check_news() {
      const res = await api.get(`/api/notifications/check_news/${this.user_id}`, {
        timeout: 1000 * 35, // server timeout 30s
      });
      this.news_count = res["news_count"];
      if (this.news_count === 0 && this.polling) {
        await this.check_news();
      }
    },
    gotoNotificationPage() {
      if (router.currentRoute.value.path === "/notifications") {
        window.location.reload();
      } else {
        this.polling = false;
        router.push(`/notifications`);
      }
    }
  }
})
</script>
<style>

</style>