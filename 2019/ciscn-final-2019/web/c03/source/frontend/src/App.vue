<template>
  <div id="app">
    <el-container>
      <el-header
        height="45px"
        :style="{ 'background-color': primaryColor, paddingTop: '10px', color: '#ffffff', 'text-align': 'center'}"
      >
        分布式网盘系统
      </el-header>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data: function () {
    return {
      primaryColor: '#409eff'
    }
  }
}
</script>

<style>
  .value {
    color: #FFFFFF;
  }

  #app {
    font-family: Helvetica, sans-serif;
  }
</style>
