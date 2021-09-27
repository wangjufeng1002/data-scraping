<template>
  <div>
    <el-card>
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="账号">
          <el-input
            v-model="formInline.account"
            placeholder="账号"
          ></el-input>
        </el-form-item>
        <el-form-item label="代理ip">
          <el-input
            v-model="formInline.proxyIp"
            placeholder="代理ip"
          ></el-input>
        </el-form-item>
        <el-form-item label="启用状态">
          <el-select v-model="formInline.status" placeholder="启用状态">
            <el-option label="未启用" value="0"></el-option>
            <el-option label="已启用" value="1"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onQuery">查询</el-button>
          <el-button type="danger" @click="onAdd">新增</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card style="margin-top: 20px" >
      <el-table :data="tableData" style="width: 100%" v-loading="loading"> 
        <el-table-column prop="account" label="账号" />
        <el-table-column prop="adb" label="手机adb地址" />
        <el-table-column prop="ip" label="部署ip" />
        <el-table-column prop="proxyIp" label="代理ip" />
        <el-table-column prop="statusDesc" label="启用状态" />
        <el-table-column prop="runStatus" label="运行状态" />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="onClickEdit(scope.row)"
              >编辑</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <div style="float: right; margin-top: 30px">
        <el-pagination layout="prev, pager, next" :total="pageParam.total" @current-change="handlePageChange">
        </el-pagination>
      </div>
    </el-card>
      <el-dialog :visible.sync="editDialogVisiable">
      <edit
        :editForm="selectData"
        :onCancel="
          () => {
            this.editDialogVisiable = false;
          }
        "
      ></edit>
    </el-dialog>
  </div>
</template>
<script>
import edit from "./edit.vue";
import {requestList} from './request'
export default {
    components: {
    edit,
  },
    data(){
        return{
            formInline:{

            },
            tableData:[],
            pageParam:{
              size:10,
              page:1,
              total:10,
            },
            selectData:{},
            editDialogVisiable:false,
            loading:false
        }
    },
    methods:{
    async onQuery() {
      const param ={
        ...this.formInline,
        ...this.pageParam
      }
      console.log(param)
      this.loading=true
      const { data } = await requestList(param);
      this.pageParam.total=data.data.totalCount
      this.tableData = data.data.list;
      this.loading=false;
    },
    onClickEdit(row) {
      console.log(row);
      this.editDialogVisiable = true;
      this.selectData = row;
      this.edit = true;
    },
    onAdd() {
      this.editDialogVisiable = true;
      this.selectData = "";
      this.edit = false;
    },
    handlePageChange(currentPage){
      this.pageParam.page=currentPage;
      this.onQuery()
    }
    },
  setup() {},
};
</script>