<template>
  <div>首页</div>
  <div class="mb-4">
    <el-button>Default</el-button>
    <el-button type="primary">Primary</el-button>
    <el-button type="success">Success</el-button>
    <el-button type="info">Info</el-button>
    <el-button type="warning">Warning</el-button>
    <el-button type="danger">Danger</el-button>
    <el-rate v-model="store.value2" :colors="store.color"></el-rate>
  </div>
</template>

<script setup>
  import {reactive} from "vue";

  const store = reactive({
    value2: null,
    color: ['#99A9BF', '#F7BA2A', '#FF9900'],
  })
</script>

<style scoped>

</style>