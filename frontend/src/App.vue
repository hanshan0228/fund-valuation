<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <h1>基金估值系统</h1>
      <el-menu
        :default-active="$route.path"
        mode="horizontal"
        :ellipsis="false"
        router
      >
        <el-menu-item index="/portfolios">组合列表</el-menu-item>
        <el-menu-item index="/upload">OCR上传</el-menu-item>
        <el-menu-item index="/statistics">收益统计</el-menu-item>
      </el-menu>
    </el-header>
    <el-main class="app-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.app-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.app-header h1 {
  margin: 0 30px 0 0;
  font-size: 24px;
}

.app-main {
  background-color: #f5f5f5;
  padding: 20px;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
  flex: 1;
}

:deep(.el-menu--horizontal .el-menu-item) {
  color: white;
  border-bottom-color: transparent;
}

:deep(.el-menu--horizontal .el-menu-item:hover),
:deep(.el-menu--horizontal .el-menu-item.is-active) {
  background-color: rgba(255, 255, 255, 0.2);
  border-bottom-color: white;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
}
</style>
