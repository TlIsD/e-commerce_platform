<template>
  <div class="login-container">
    <div class="login">
      <div class="login-title">
        <img src="../assets/logo.jpg" alt="logo">
        <p>-------------------------------------------</p>
      </div>
      <div class="login_box">
        <Login @success_handle = 'success_handle'></Login>
      </div>
    </div>
  </div>
</template>

<script setup>
import Login from "../components/Login.vue";
import router from "../router/index.js";

const success_handle = () => {
  router.push("/");
}
</script>

<style scoped>
.login-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../assets/loginBI.jpg');
  background-size: cover;
  background-position: center;
  z-index: -1;
}

.login {
  position: absolute;
  width: 80%;
  max-width: 500px;
  height: auto;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

.login-title {
  width: 100%;
  text-align: center;
}

.login-title img {
  width: 90px;
  height: 100px;
}

.login-title p {
  font-size: 18px;
  color: #fff;
  letter-spacing: 0.29px;
  padding-top: 10px;
  padding-bottom: 50px;
}

.login_box {
  width: 100%;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  padding: 50px 20px 40px;
}
</style>
