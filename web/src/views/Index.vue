<template>
  <h1>Index</h1>
</template>
<script>
import router from "@/router/index.js";
import localStore from "@/utils/store.js";

export default {
  created() {
    const user = JSON.parse(localStore.get("user") || {})
    console.log(user);
    if (user && user['role_name']) {
      const role_name = user['role_name'];
      console.log(role_name);
      if (role_name === "STUDENT") {
        router.push('/student');
      } else if (role_name === "INSTRUCTOR") {
        router.push('/instructor');
      } else if (role_name === "ADMIN") {
        router.push('/admin');
      } else {
        router.push('/login');
      }
    }
  }
}
</script>
