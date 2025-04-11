<template>
  <div class="footer">
    <ul>
      <li v-for="nav in nav.nav_footer_list">
        <a v-if="nav.is_http" :href="nav.link">{{ nav.name }}</a>
        <router-link v-else :to="nav.link">{{ nav.name }}</router-link>
      </li>
    </ul>
    <p>Copyright © x x x x x x x x | x x x x x x x x</p>
  </div>
</template>

<script setup>
import nav from "../api/nav.js";

// 请求脚部导航数据
nav.get_nav_footer().then(res =>{
  // console.log(res.data)
  nav.nav_footer_list = res.data;
})
</script>

<style scoped>
.footer {
  width: 100%;
  height: 128px;
  color: #555555;
}
.footer ul{
  margin: 0 auto 16px;
  padding-top: 38px;
  width: 930px;
}
.footer ul li{
  float: left;
  width: 112px;
  margin: 0 10px;
  text-align: center;
  font-size: 14px;
  display: block;
}
.footer ul li a{
  color: #1c1f21;
}
.footer ul::after{
  content:"";
  display:block;
  clear:both;
}
.footer p{
  text-align: center;
  font-size: 12px;
}
</style>