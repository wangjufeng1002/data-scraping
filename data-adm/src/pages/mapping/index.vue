<template>
  <div>
    <el-card>
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="当当商品ID">
          <el-input
            v-model="formInline.ddProductId"
            placeholder="当当商品ID"
          ></el-input>
        </el-form-item>
        <el-form-item label="外部商品ID">
          <el-input
            v-model="formInline.outerProductId"
            placeholder="外部商品ID"
          ></el-input>
        </el-form-item>
        <el-form-item label="匹配状态">
          <el-select v-model="formInline.status" placeholder="匹配状态">
            <el-option label="匹配成功" value="10"></el-option>
            <el-option label="待确认" value="1"></el-option>
            <el-option label="未匹配" value="0"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onQuery">查询</el-button>
          <el-button type="danger" @click="onAdd">新增</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card style="margin-top: 20px">
      <el-table :data="tableData" style="width: 100%" v-loading="loading">
        <el-table-column prop="productId" label="当当ID" width="100" />
        <el-table-column prop="productName" label="商品名称" width="130">
          <template slot-scope="scope">
            <div class="title">
              {{ scope.row.productName }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="isbn" label="ISBN" />
        <el-table-column prop="fixPrice" label="定价" />
        <el-table-column prop="press" label="出版社" />
        <el-table-column prop="outerShopName" label="外店名称" />
        <el-table-column prop="outerProductId" label="外部商品ID" />
        <el-table-column prop="outerProductSkuId" label="外部商品SKU" />
        <el-table-column prop="outerProductName" label="外部商品名称">
          <template slot-scope="scope">
            <div class="title">
              {{ scope.row.productName }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="outerIsbn" label="外部商品ISBN" />
        <el-table-column prop="outerFixPrice" label="外部商品定价" />
        <el-table-column prop="outerPress" label="外部商品出版社" />
        <el-table-column prop="statusDesc" label="匹配状态"> </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status == 1"
              @click="handleClick(scope.row)"
              type="text"
              size="small"
              >确认</el-button
            >
            <el-button
              v-if="scope.row.status == 0"
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
        :edit="edit"
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
import { requestList } from "./request";
import edit from "./edit.vue";
export default {
  components: {
    edit,
  },
  data() {
    return {
      formInline: {
        ddProductId: "",
        outerProductId: "",
        status: "",
      },
      pageParam: {
        page: 1,
        size: 10,
        total: 10,
      },
      editDialogVisiable: false,
      selectData: {},
      edit: false,
      tableData: [],
      loading:false
    };
  },
  methods: {
    async onQuery() {
      const param ={
        ...this.formInline,
        ...this.pageParam
      }
      this.loading=true
      const { data } = await requestList(param);
      this.pageParam.total=data.data.totalPage
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
};
</script>
<style>
.title {
  max-width: 165px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>