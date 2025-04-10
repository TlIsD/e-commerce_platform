<template>
  <div>Hello</div>
  <router-view></router-view>
</template>

<script setup>

</script>

<style scoped>
/* 全局初始化 */
body,h1,h2,h3,h4,p,table,tr,td,ul,li,a,form,input,select,option,textarea{
  margin:0;
  padding: 0;
  font-size: 15px;
}
a{
  text-decoration: none;
  color: #333;
  cursor: pointer;
}
ul,li{
  list-style: none;
}
table{
  border-collapse: collapse;
}
img{
  max-width: 100%;
  max-height: 100%;
}
input{
  outline: none;
}
</style>
