<template>
  <div class="title">
    <span :class="{active:user.login_type===0}" @click="user.login_type=0">密码登录</span>
    <span :class="{active:user.login_type===1}" @click="user.login_type=1">短信登录</span>
  </div>
  <div class="inp" v-if="user.login_type===0">
    <div v-if="user.rem_password && user.rem_account">
      <input v-model="user.rem_account" type="text" placeholder="用户名 / 手机号码" class="user">
      <input v-model="user.rem_password" type="password" class="pwd" placeholder="密码">
    </div>
    <div v-else>
      <input v-model="user.account" type="text" placeholder="用户名 / 手机号码" class="user">
      <input v-model="user.password" type="password" class="pwd" placeholder="密码">
    </div>
    <div id="geetest1"></div>
    <div class="remember">
      <label>
        <input type="checkbox" class="no" v-model="user.remember"/>
        <span>记住密码</span>
      </label>
      <p>忘记密码？</p>
    </div>
    <button class="login_btn" @click="show_captcha">登录</button>
    <p class="go_login">没有账号
      <span><router-link to="/register" style="color: #2c70b6; cursor:pointer">立即注册</router-link></span>
    </p>
  </div>
  <div class="inp" v-show="user.login_type===1">
    <div>
      <input v-model="user.phone" type="text" placeholder="手机号码" class="user" @blur="check_phone_inp">
      <el-text type="danger" size="small">{{ phone_err }}</el-text>
    </div>
    <input v-model="user.captcha"  type="text" class="code" placeholder="短信验证码">
    <el-button id="get_code" type="primary" :disabled="isSmsActivate">获取验证码</el-button>
    <button class="login_btn" @click="show_captcha">登录</button>
    <p class="go_login">没有账号
      <span><router-link to="/register" style="color: #2c70b6; cursor:pointer">立即注册</router-link></span>
    </p>
  </div>
</template>

<script setup>
import user from "../api/user.js";
import { ElMessage } from "element-plus";
import {useStore} from 'vuex';
import '../utils/TCaptcha.js'
import settings from "../settings.js";
import {ref} from "vue";

const store = useStore();

const emmit = defineEmits(["success_handle"]);

const phone_err = ref(null)
var isSmsActivate = ref(false)

const check_phone_inp = () =>{
  phone_err.value = ''
  isSmsActivate.value = false
  if(user.phone.length < 1){
    phone_err.value = '请填写手机号'
    isSmsActivate.value = true
  }else if(!/1[3-9]\d{9}/.test(user.phone)){
    phone_err.value = '手机号格式错误'
    isSmsActivate.value = true
  }
}

// 验证码
const show_captcha = () => {
  if(user.login_type===0){
    if(user.rem_account && user.rem_password){
      user.account = user.rem_account
      user.password = user.rem_password
    }
    if(user.account.length < 1 || user.password.length < 1){
      // 错误提示
      ElMessage.error('用户名或密码不能为空')
    }
    else{
      var captcha = new TencentCaptcha(settings.CaptchaAppId, (res)=>{
        // console.log(res);
        // 调用登录处理
        login_handler(res)
      })
      captcha.show()
    }
  }else if(user.login_type===1){
    if(user.phone.length < 1 || user.captcha.length < 1){
      ElMessage.error('手机号或验证码不能为空')
    }else{
      ElMessage.error('尚未开发完成')
      // var captcha = new TencentCaptcha(settings.CaptchaAppId, (res)=>{
      //   phone_login_handler(res)
      // })
      // captcha.show()
    }
  }
}

// 账号密码登录
const login_handler = (res) => {
  // 登录请求
  user.login({
    ticket: res.ticket,
    randstr: res.randstr
  }).then((res) => {
    // 先删除原先的状态
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');

    // console.log(res.data)

    // 获取载荷信息
    let payload = res.data.token.split('.')[1]
    let payload_data = JSON.parse(atob(payload))
    // console.log(payload_data)
    store.commit('login', payload_data)
    store.commit('cart_total', res.data.cart_total)

    ElMessage.success('登录成功')

    // 后续处理
    if(!user.remember){
      user.account = ''
      user.rem_account = ''
      user.password = ''
      user.rem_password = ''
      user.remember = false
      user.phone = ''
      user.captcha = ''
      localStorage.removeItem('remember');
      localStorage.removeItem('rem_account')
      localStorage.removeItem('rem_password')
    }else {
      // 记住密码
      localStorage.setItem('remember', true)
      localStorage.setItem('rem_account', user.account)
      localStorage.setItem('rem_password', user.password)
    }

    emmit('success_handle')
  }).catch(err => {
    ElMessage.error('登录失败')
  })
}

// // 手机验证码登录
// const phone_login_handler = (res) => {
//   user.login({
//     ticket: res.ticket,
//     randstr: res.randstr
//   }).then((res) => {
//     // 先删除原先的状态
//     localStorage.removeItem('token');
//     sessionStorage.removeItem('token');
//
//     console.log('res:::', res)
//
//     // 获取载荷信息
//     let payload = res.data.token.split('.')[1]
//     let payload_data = JSON.parse(atob(payload))
//     console.log('payload:::', payload_data)
//
//     store.commit('login', payload_data)
//     ElMessage.success('登录成功')
//
//     user.phone = ''
//     user.captcha = ''
//
//     emmit('success_handle')
//   }).catch(err => {
//     ElMessage.error('登录失败')
//   })
// }
</script>

<style scoped>
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
  border-bottom: 2px solid #84cc39;
}

.inp{
  width: 350px;
  margin: 0 auto;
}
.inp .code{
  width: 220px;
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
}
.inp input.user{
  margin-bottom: 16px;
}
.inp .remember{
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}
.inp .remember p:first-of-type{
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: .19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
}
.inp .remember p:nth-of-type(2){
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: .19px;
  cursor: pointer;
}

.inp .remember input{
  outline: 0;
  width: 25px;
  height: 25px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
  vertical-align: middle;
  margin-right: 4px;
}

.inp .remember p span{
  display: inline-block;
  font-size: 12px;
  width: 100px;
}
.login_btn{
  cursor: pointer;
  width: 100%;
  height: 45px;
  background: #2c70b6;
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
  color: #2c70b6;
  cursor: pointer;
}
</style>