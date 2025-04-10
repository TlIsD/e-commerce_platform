<template>
  <div class="home">
    <Header></Header>

    <Footer></Footer>
  </div>
</template>

<script setup>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";

import http from "../utils/http.js";

http.get('/home/test').then(res =>{
  console.log(res.data)
});

</script>

<style scoped>

</style>