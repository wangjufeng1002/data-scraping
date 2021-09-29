<template>
<el-container style="height: 100%; border: 1px solid #eee">
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
    <el-menu  @select="onSelect">
      <el-submenu index="1">
        <template slot="title"><i class="el-icon-message"></i>映射匹配</template>
          <el-menu-item index="1-1">匹配列表</el-menu-item>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title"><i class="el-icon-message"></i>账号管理</template>
          <el-menu-item index="2-1">账号列表</el-menu-item>
          <el-menu-item index="2-2">账号流量统计</el-menu-item>
      </el-submenu>
      <el-submenu index="3">
        <template slot="title"><i class="el-icon-message"></i>任务管理</template>
          <el-menu-item index="3-1">任务列表</el-menu-item>
      </el-submenu>
    </el-menu>
  </el-aside>
  
  <el-container style="height: 100%">
    <el-main>
      <mapping v-if="index=='1-1'"></mapping>
      <account v-if="index=='2-1'"></account>
      <chart v-if="index=='2-2'"/>
      <taskList v-if="index=='3-1'"/>
    </el-main>
  </el-container>
</el-container>

</template>

<script>
import mapping from './pages/mapping/index.vue'
import account from './pages/account/index.vue'
import chart from './pages/accountChart/index.vue'
import taskList from './pages/task/index.vue'
export default {
  name: 'app',
  components:{
    mapping,
    account,
    chart,
    taskList
  },
     data() {
      return {
        index:'1-1'
      }
    },
    methods:{
      onSelect(index){
        this.index=index
      }
    }
}
</script>

<style>

  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
  
  .el-aside {
    color: #333;
  }
</style>
