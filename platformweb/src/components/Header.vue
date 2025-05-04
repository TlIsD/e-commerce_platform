<template>
  <div class="header-box">
    <div class="header">
      <el-row :gutter="20">
        <div class="content">
          <el-col>
            <div class="logo">
              <router-link to="/"><img src="../assets/logo.jpg" alt=""></router-link>
            </div>
          </el-col>

          <el-col>
            <ul class="nav">
              <li v-for="nav in nav.nav_header_list">
                <a v-if="nav.is_http" :href="nav.link">{{ nav.name }}</a>
                <router-link v-else :to="nav.link">{{ nav.name }}</router-link>
              </li>
            </ul>
          </el-col>

          <el-col>
            <div class="search-warp">
              <div class="search-area">
                <input class="search-input" placeholder="请输入关键字..." type="text" autocomplete="off">
                <div class="hotTags">
                  <router-link to="/search/?words=Vue" target="_blank" class="">Vue</router-link>
                  <router-link to="/search/?words=Python" target="_blank" class="last">Python</router-link>
                </div>
              </div>
              <div class="show-hide-search" data-show="no"><img class="imv2-search2" src="../assets/search.svg"  alt=""/></div>
            </div>
          </el-col>

          <el-col>
            <div class="login-bar" v-if="!store.state.user.user_id">
              <div class="shop-cart full-left">
                <img src="../assets/cart.svg" alt="" />
                <span><router-link to="/cart">购物车</router-link></span>
              </div>
              <div class="login-box full-left">
                <span @click="state.show_login=true">登录</span>
                &nbsp;/&nbsp;
                <router-link to="/register">注册</router-link>
              </div>
            </div>

            <div class="login-bar logined-bar" v-if="store.state.user.user_id">
              <div class="shop-cart ">
                <img src="../assets/cart.svg" alt="" />
                <el-badge type="danger" :value="store.state.cart_total" class="item">
                  <span><router-link to="/cart">购物车</router-link></span>
                </el-badge>
              </div>
              <div class="login-box ">
                <span>
                  <router-link to="">我的课堂</router-link>
                </span>
                <el-dropdown>
                <span class="el-dropdown-link">
                  <el-avatar class="avatar" size=default :src="store.state.user.avatar"></el-avatar>
                </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item :icon="UserFilled">学习中心</el-dropdown-item>
                      <el-dropdown-item :icon="List">订单列表</el-dropdown-item>
                      <el-dropdown-item :icon="Setting">个人设置</el-dropdown-item>
                      <el-dropdown-item :icon="Close" @click="logout">注销登录</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </el-col>
        </div>
      </el-row>
    </div>
  </div>

  <el-dialog :width="600" v-model="state.show_login" :style="{ borderRadius: '16px' }">
    <Login @success_handle="login_success"></Login>
  </el-dialog>

</template>


<script setup>
import nav from "../api/nav.js";
import Login from "./Login.vue";
import { reactive } from "vue";
import { UserFilled,List,Setting,Close } from "@element-plus/icons-vue";
import { useStore } from "vuex";

const store = useStore()


// 请求头部导航数据
nav.get_nav_header().then(res =>{
  // console.log(res.data)
  nav.nav_header_list = res.data;
})

// 弹窗登录组件
const state = reactive({
  show_login: false,
})

const login_success = () =>{
  state.show_login = false;
}

const logout = () =>{
  store.commit("logout");
}
</script>

<style scoped>
.header-box{
  height: 72px;
}
.header-box .header{
  width: 100%;
  height: 72px;
  box-shadow: 0 1px 1px 0 #c9c9c9;
  position: fixed;
  top:0;
  left: 0;
  right:0;
  margin: auto;
  z-index: 9;
  background: #fff;
}
.header .content{
  width: 100%;
  margin: 0 auto;
}
.header .content .logo{
  height: 72px;
  line-height: 72px;
  margin: 0 20px;
  float: left;
  cursor: pointer;
}
.header .content .logo img{
  height: 72px;
  vertical-align: middle;
}
.header .nav li{
  float: left;
  height: 80px;
  line-height: 80px;
  margin-right: 30px;
  font-size: 16px;
  color: #4a4a4a;
  cursor: pointer;
  display: inline-block;
}
.header .nav li span{
  padding-bottom: 16px;
  padding-left: 5px;
  padding-right: 5px;
}
.header .nav li span a{
  display: inline-block;
  text-decoration: none;
}

.header .nav li .this{
  color: #4a4a4a;
  border-bottom: 4px solid #ffc210;
}
.header .nav li:hover span{
  color: #00ff00;
}

/*首页导航全局搜索*/
.search-warp {
  position: relative;
  float: left;
  margin-left: 24px;
}
.search-warp .show-hide-search {
  width: 20px;
  height: 24px;
  text-align: right;
  position: absolute;
  display: inline-block;
  right: 0;
  bottom: 24px;
  padding: 0 8px;
  border-radius: 18px;
}
.search-warp .show-hide-search i {
  display: block;
  height: 24px;
  color: #545C63;
  cursor: pointer;
  font-size: 18px;
  line-height: 24px;
  width: 20px;
}
.search-area {
  float: right;
  position: relative;
  height: 40px;
  padding-right: 36px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.4);
  zoom: 1;
  background: #F3F5F6;
  border-radius: 4px;
  margin: 16px 0;
  width: 324px;
  box-sizing: border-box;
  font-size: 0;
  -webkit-transition: width 0.3s;
  -moz-transition: width 0.3s;
  transition: width 0.3s;
}
.search-area .search-input {
  padding: 8px 12px;
  font-size: 14px;
  color: #9199A1;
  line-height: 24px;
  height: 40px;
  width: 100%;
  float: left;
  border: 0;
  -webkit-transition: background-color 0.3s;
  -moz-transition: background-color 0.3s;
  transition: background-color 0.3s;
  background-color: transparent;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
  -ms-box-sizing: border-box;
  box-sizing: border-box;
}
.search-area .search-input.w100 {
  width: 100%;
}
.search-area .hotTags {
  display: inline-block;
  position: absolute;
  top: 0;
  right: 32px;
}
.search-area .hotTags a {
  display: inline-block;
  padding: 4px 8px;
  height: 16px;
  font-size: 14px;
  color: #9199A1;
  line-height: 16px;
  margin-top: 8px;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.search-area .hotTags a:hover {
  color: #F21F1F;
}
.search-area input::-webkit-input-placeholder {
  color: #A6A6A6;
}
.search-area input::-moz-placeholder {
  /* Mozilla Firefox 19+ */
  color: #A6A6A6;
}
.search-area input:-moz-placeholder {
  /* Mozilla Firefox 4 to 18 */
  color: #A6A6A6;
}
.search-area input:-ms-input-placeholder {
  /* Internet Explorer 10-11 */
  color: #A6A6A6;
}
.search-area .btn_search {
  float: left;
  cursor: pointer;
  width: 30px;
  height: 38px;
  text-align: center;
  -webkit-transition: background-color 0.3s;
  -moz-transition: background-color 0.3s;
  transition: background-color 0.3s;
}
.search-area .search-area-result {
  position: absolute;
  left: 0;
  top: 57px;
  width: 300px;
  margin-bottom: 20px;
  border-top: none;
  background-color: #fff;
  box-shadow: 0 8px 16px 0 rgba(7, 17, 27, 0.2);
  font-size: 12px;
  overflow: hidden;
  display: none;
  z-index: 800;
  border-bottom-right-radius: 8px;
  border-bottom-left-radius: 8px;
}
.search-area .search-area-result.hot-hide {
  top: 47px;
}
.search-area .search-area-result.hot-hide .hot {
  display: none;
}
.search-area .search-area-result.hot-hide .history {
  border-top: 0;
}
.search-area .search-area-result h2 {
  font-size: 12px;
  color: #1c1f21;
  line-height: 12px;
  margin-bottom: 8px;
  font-weight: 700;
}
.search-area .search-area-result .hot {
  padding: 12px 0 8px 12px;
  box-sizing: border-box;
}
.search-area .search-area-result .hot .hot-item {
  background: rgba(84, 92, 99, 0.1);
  border-radius: 12px;
  padding: 4px 12px;
  line-height: 16px;
  margin-right: 4px;
  margin-bottom: 4px;
  display: inline-block;
  cursor: pointer;
  font-size: 12px;
  color: #545c63;
}
.search-area .search-area-result .history {
  border-top: 1px solid rgba(28, 31, 33, 0.1);
  box-sizing: border-box;
}
.search-area .search-area-result .history li {
  height: 40px;
  line-height: 40px;
  padding: 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #787d82;
  cursor: pointer;
}
.search-area .search-area-result .history li:hover,
.search-area .search-area-result .history li .light {
  color: #1c1f21;
  background-color: #edf0f2;
}

.header .login-bar{
  margin-top: 20px;
  margin-right: 20px;
  height: 80px;
  float: right;
}
.header .login-bar .shop-cart{
  float: left;
  margin-right: 20px;
  border-radius: 17px;
  background: #f7f7f7;
  cursor: pointer;
  font-size: 14px;
  height: 28px;
  width: 88px;
  line-height: 32px;
  text-align: center;
}
.header .login-bar .shop-cart:hover{
  background: #f0f0f0;
}
.header .login-bar .shop-cart img{
  width: 15px;
  margin-right: 4px;
  margin-left: 6px;
}
.header .login-bar .shop-cart span{
  margin-right: 6px;
}
.header .login-bar .login-box{
  float: left;
  height: 28px;
  line-height: 30px;
}
.header .login-bar .login-box span{
  color: #4a4a4a;
  cursor: pointer;
}
.header .login-bar .login-box span:hover{
  color: #000000;
}

.header .logined-bar .shop-cart{
  height: 32px;
  line-height: 32px;
}
.logined-bar .login-box{
  height: 72px;
  line-height: 72px;
  position: relative;
  margin-right: 20px;
}

.logined-bar .el-dropdown-link{
  margin-left: 15px;
  margin-top: -5px;
}

.logined-bar el-avatar{
  float: right;
  width: 50px;
  height: 50px;
  position: absolute;
  transition: transform .5s ease-in .1s;
}
.logined-bar el-avatar:hover{
  transform: scale(1.3);
}
</style>