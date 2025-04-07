<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 350px;
  padding: 20px;
  text-align: center;
}

.login-logo {
  width: 180px;
  margin: 15px;
  align-items: center;
}

</style>

<template>
  <div class="login-container">
    <img src="@/assets/applogo.png" alt="App Logo" class="login-logo"/>
    <el-card class="login-card">
      <h2>USER LOGIN</h2>
      <el-form ref="loginFormRef" :model="loginForm" label-width="auto">
        <el-form-item label="Email" prop="email">
          <el-input v-model="loginForm.email" placeholder="please input your email"/>
        </el-form-item>
        <el-form-item label="OTP" prop="otp">
          <el-input v-model="loginForm.otp" type="otp" placeholder="otp code"/>
        </el-form-item>
      </el-form>
      <el-row justify="center">
        <el-button type="warning" size="small" @click="sendOtp" :disabled="sendOtpBtnDisabled">
          {{ countdown > 0 ? countdown + "S RESEND" : "SEND OTP" }}
        </el-button>
        <el-button type="primary" size="small" @click="login" :disabled="loginBtnDisabled">LOGIN</el-button>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import api from '@/utils/api.js'
import localStore from '@/utils/store.js'
import {ElMessage} from 'element-plus';
import router from '@/router'

export default {
  data() {
    return {
      loginForm: {
        email: 'admin@conestogac.on.ca',
        otp: '',
      },
      // sendOtpBtnDisabled: true,
      DEFAULT_COUNTDOWN: 60,
      countdown: 0,
      // loginBtnDisabled: true,
    }
  },
  computed: {
    sendOtpBtnDisabled() {
      return !this.loginForm.email || this.countdown > 0;
    },
    loginBtnDisabled() {
      return !(this.loginForm.email && this.loginForm.otp && this.loginForm.otp.length === 6);
    }
  },
  created() {
    localStore.remove('token');
    localStore.remove('user');
  },
  methods: {
    startCountdown() {
      this.countdown = this.DEFAULT_COUNTDOWN
      const timer = setInterval(() => {
        this.countdown--;
        if (this.countdown === 0) {
          clearInterval(timer);
        }
      }, 1000);
    },
    async sendOtp() {
      this.startCountdown();
      const resp = await api.post('/api/send-otp', {email: this.loginForm.email});
      console.log(resp);
      this.loginForm.otp = resp;
      ElMessage.success("SEND SUCCESS");
    },
    async login() {
      const resp = await api.post("/api/login", {
        email: this.loginForm.email,
        otp: this.loginForm.otp,
      });
      ElMessage.success("LOGIN SUCCESS");
      localStore.set("token", resp["token"]);
      localStore.set("user", JSON.stringify(resp));
      const role_name = resp["role_name"];
      if (role_name === "STUDENT") {
        router.push(`/student`);
      } else if (role_name === "INSTRUCTOR") {
        router.push('/instructor');
      } else if (role_name === "ADMIN") {
        router.push('/admin');
      } else {
        ElMessage.error(`unknown role name ${role_name}`);
      }
    }
  }
}
</script>
