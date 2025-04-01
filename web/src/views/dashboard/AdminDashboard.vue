<template>
  <h3>Dashboard</h3>
</template>

<script>
import localStore from "@/utils/store.js";

export default {
  data() {
    return {
    }
  },
  computed: {
  },
  async created() {
    this.user_id = this.$route.params.id || this.get_login_user_id();
  },
  mounted() {
  },
  methods: {
    get_login_user_id() {
      return JSON.parse(localStore.get("user"))["user_id"];
    },
  }
};
</script>
