<template>
  <div class="login-container">
    <div class="login">
      <div class="login-title">
        <img src="../assets/logo.jpg" alt="logo">
        <p>-------------------------------------------</p>
      </div>
      <div class="register_box">
        <div class="title">
          <span class="active">用户注册</span>
        </div>
        <div class="inp">
          <input v-model="user.phone" type="text" placeholder="手机号码" class="user" @blur="check_phone_inp">
          <el-text type="danger" size="small">{{ phone_err }}</el-text>
          <input v-model="user.password" type="password" placeholder="登录密码" class="user" @blur="check_pwd_inp">
          <el-text type="danger" size="small">{{ pwd_err }}</el-text>
          <input v-model="user.re_password" type="password" placeholder="确认密码" class="user" @blur="check_re_pwd_inp">
          <el-text type="danger" size="small">{{ re_pwd_err }}</el-text>
          <div>
            <input v-model="user.captcha" type="text" class="code" placeholder="短信验证码" @blur="check_captcha_inp">
            <el-button id="get_code" type="primary">获取验证码</el-button>
          </div>
          <el-text type="danger" size="small">{{ captcha_err }}</el-text>
          <button class="register_btn" :disabled="isActivate" :class="{'deactivate': isActivate}" @click="show_captcha">注册</button>
          <p class="go_login" >已有账号 <router-link to="/login">立即登录</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import {useStore} from "vuex"
import "../utils/TCaptcha"
import user from "../api/user.js";
import {ElMessage} from "element-plus";
import router from "../router/index.js";
import settings from "../settings.js";

const store = useStore()
const phone_err = ref(null)
const pwd_err = ref(null)
const re_pwd_err = ref(null)
const captcha_err = ref(null)

var isActivate = ref(false)

const check_phone_inp = () =>{
  phone_err.value = ''
  isActivate.value = false
  if(user.phone.length < 1){
    phone_err.value = '请填写手机号'
    isActivate.value = true
  }else if(/1[3-9]\d{9}/.test(user.phone)){
    // 发送ajax验证手机号是否已经注册
    user.check_phone().catch(error=>{
      phone_err.value = error.response.data.err;
      isActivate.value = false
    })
  }else {
    // 手机号格式错误
    phone_err.value = '手机号格式错误'
    isActivate.value = false
  }
}

const check_pwd_inp = () =>{
  pwd_err.value = ''
  isActivate.value = false
  if(user.phone.length < 1){
    pwd_err.value = '请填写密码'
    isActivate.value = true
  }else if (user.password.length < 6 || user.password.length > 16) {
    pwd_err.value = '密码必须在6~16个字符之间'
    isActivate.value = true
  }
}

const check_re_pwd_inp = () =>{
  re_pwd_err.value = ''
  isActivate.value = false
  if(user.phone.length < 1){
    re_pwd_err.value = '请再次输入密码'
    isActivate.value = true
  }else if (user.password !== user.re_password) {
    re_pwd_err.value = '两次密码不一致'
    isActivate.value = true
  }
}

const check_captcha_inp = () =>{
  captcha_err.value = ''
  isActivate.value = false
  if(user.captcha.length < 1){
    captcha_err.value = '请填写验证码'
    isActivate.value = true
  }
}

// 验证码
const show_captcha = () => {
  var captcha = new TencentCaptcha(settings.CaptchaAppId, (res)=>{
    console.log(res);
    // 调用注册处理
    register_handler(res)
  })
  captcha.show()
}

const register_handler = (res)=> {

  // 发送请求
  user.register({
    // 验证码通过的票据信息
    ticket: res.ticket,
    randstr: res.randstr,
  }).then(res=>{
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");

    // 默认不记住登录
    sessionStorage.token = res.data.token;

    // vuex存储登录信息
    let payload = res.data.token.split(".")[1]  // 载荷
    let payload_data = JSON.parse(atob(payload)) // 用户信息
    store.commit("login", payload_data)
    // 清空表单信息
    user.phone = ""
    user.password = ""
    user.re_password = ""
    user.captcha = ""
    user.remember = false
    // 成功提示
    ElMessage.success("注册成功！");
    // 路由跳转到首页
    router.push("/");

  })
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
  background-image: url('../assets/register.jpg');
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
  padding-bottom: 20px;
}

.register_box{
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0,0,0,.5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
  padding-top: 50px;
}
.title{
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: .32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 0px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}
.title span.active{
  color: #4a4a4a;
}

.inp{
  width: 350px;
  margin: 0 auto;
}
.inp .code{
  width: 190px;
  margin-right: 16px;
}
#get_code{
  margin-top: 6px;
}
.inp input{
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
  margin-top: 16px;
}
.inp input span{
  color: #F01414;
  font-size: 12px;
}
.register_btn{
  cursor: pointer;
  width: 100%;
  height: 45px;
  background: #84cc39;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: .26px;
  margin-top: 30px;
  border: none;
  outline: none;
}
.inp .go_login{
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .26px;
  padding-top: 20px;
}
.inp .go_login span{
  color: #84cc39;
  cursor: pointer;
}
.deactivate{
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
  border: 1px solid #999;
}
</style>
