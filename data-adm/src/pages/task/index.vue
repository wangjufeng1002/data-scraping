<template>
  <div>
    <el-card>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column label="任务id" prop="id"> </el-table-column>
        <el-table-column label="任务名称" prop="taskName"> </el-table-column>
        <el-table-column label="平台" prop="taskPlatform"> </el-table-column>
        <el-table-column label="任务类别" prop="taskType"> </el-table-column>
        <el-table-column label="任务状态" prop="taskStatus"> </el-table-column>
        <el-table-column label="创建时间" prop="createTime"> </el-table-column>
        <el-table-column
          label="开始时间"
          prop="taskStartTime"
        ></el-table-column>
        <el-table-column label="结束时间" prop="taskEndTime"> </el-table-column>
        <el-table-column label="详情">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="text" size="small"
              >查看</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        style="float: right"
        layout="prev, pager, next"
        :total="TaskListPageParam.total"
        @current-change="handleListPageChange"
      />
    </el-card>
    <el-dialog title="任务详情" :visible.sync="dialogTableVisible">
      <el-table :data="detailData">
        <el-table-column label="标签" prop="taskLabel" />
        <el-table-column label="开始时间" prop="taskStartTime" />
        <el-table-column label="完成时间" prop="taskCompleteTime" />
        <el-table-column label="邮件发送时间" prop="taskMailTime" />
        <el-table-column label="状态" prop="status" />
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
            v-if="scope.row.status>=10"
              @click="handleDownload(scope.row)"
              type="text"
              size="small"
              >下载</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        style="float: right"
        layout="prev, pager, next"
        :total="detailPageParam.total"
        @current-change="handleDetailPageChange"
      />
    </el-dialog>
  </div>
</template>
<script>
import { requestList, requestDetail,download } from "./request";
import {convertRes2Blob} from '../../util'
export default {
  setup() {},
  data() {
    return {
      TaskListPageParam: {
        total: 1,
        page: 1,
        size: 10,
      },
      detailPageParam: {
        total: 1,
        page: 1,
        size: 5,
      },
      dialogTableVisible: false,
      selectTaskId: 100,
      tableData: [],
      detailData: [],
    };
  },
  methods: {
    async handleClick(row) {
      console.log(row);
      this.dialogTableVisible = true;
      this.selectTaskId = row.taskId;
      await this.getDetail();
    },
    async getTaskList() {
      const params = {
        ...this.TaskListPageParam,
      };
      const { data } = await requestList(params);
      this.tableData = data.data.list;
      this.TaskListPageParam.total = data.data.totalCount;
    },
    async handleListPageChange(page) {
      this.TaskListPageParam.page = page;
      await this.getTaskList();
    },
    async handleDetailPageChange(page) {
      this.detailPageParam.page = page;
      await this.getDetail();
    },
    handleDownload(row){
        const params={
            taskId:row.taskId,
            taskLabel:row.taskLabel
        }
        download(params).then(res =>{
        convertRes2Blob(res)
        })
        
        
    },
    async getDetail() {
      const params = {
        ...this.detailPageParam,
        taskId: this.selectTaskId,
      };
      const { data } = await requestDetail(params);
      this.detailData = data.data.list;
      this.detailPageParam.total = data.data.totalCount;
    },
  },
  async mounted() {
    await this.getTaskList();
  },
  computed: {},
};
</script>