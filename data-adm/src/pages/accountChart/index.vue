<template>
  <div class="main-container">
    <div class="panel-container">
      <el-card class="panel-item">
        <div slot="header" class="clearfix">总抓取量</div>
        <div class="panel-font">{{ total }}</div>
        <div class="time-font">最后更新时间:{{ dateformat }}</div>
      </el-card>
      <el-card class="panel-item">
        <div slot="header" class="clearfix">今日抓取量</div>
        <div class="panel-font">{{ today }}</div>
        <div class="time-font">最后更新时间:{{ dateformat }}</div>
      </el-card>
      <el-card class="panel-item" slot="header">
        <div slot="header" class="clearfix">
          <span>账号抓取量</span>
          <el-dropdown @command="getAccountData" style="float: right">
            <span class="el-dropdown-link">
              切换账号<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                v-for="value in account"
                :command="value"
                :key="value"
                >{{ value }}</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <div>
          <div class="panel-font">{{ accountNum.total }}</div>
          <div class="time-font">日抓取量: {{ accountNum.todayTotal }}</div>
        </div>
      </el-card>
      <el-card class="panel-item" slot="header">
        <div slot="header" class="clearfix">
          <span>代理IP抓取量</span>
          <el-dropdown @command="getProxyData" style="float: right">
            <span class="el-dropdown-link">
              切换IP<i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item
                v-for="value in proxyIp"
                :command="value"
                :key="value"
                >{{ value }}</el-dropdown-item
              >
            </el-dropdown-menu>
          </el-dropdown>
        </div>
        <div>
          <div class="panel-font">{{ proxyNum.total }}</div>
          <div class="time-font">日抓取量: {{ proxyNum.todayTotal }}</div>
        </div>
      </el-card>
    </div>
    <div class="chart-container">
      <el-card class="chart-item">
        <el-tabs v-model="activeName">
          <el-tab-pane label="账号统计" name="account">
            <div id="container"></div
          ></el-tab-pane>
          <el-tab-pane label="代理IP统计" name="proxyIp">
            <div id="container2"></div
          ></el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>
<script>
import { Line } from "@antv/g2plot";
import { requestData, getTotalData, getAccountData } from "./request";
import { dateFormat } from "../../util";
export default {
  data() {
    return {
      today: 0,
      total: 0,
      accountNum: {
        total: 0,
        todayTotal: 0,
      },
      proxyNum: {
        total: 0,
        todayTotal: 0,
      },
      selectAccount: "",
      selectProxyIp: "",
      account: ["112", "34341", "!23123", "123123"],
      proxyIp: ["2111", "123333", "12312313", "132213132"],
      activeName: "account",
    };
  },

  computed: {
    dateformat() {
      let date = new Date();
      return dateFormat("YYYY-MM-dd HH:mm:SS", date);
    },
  },
  methods: {
    async renderAccountLine() {
      const params = {
        type: 1,
        startDate: "2021-09-07 00:00:00",
      };
      const { data } = (await requestData(params)).data;
      const plot = new Line("container", {
        autoFit: true,
        height: 500,
        data,
        xField: "date",
        yField: "total",
        seriesField: "dimension",
        tooltip: { showMarkers: false },
      });
      plot.render();
    },
    async getAccountData(account) {
      const params = {
        type: 1,
        account,
      };
      const { data } = await getTotalData(params);
      this.accountNum = data.data;
    },
    async getProxyData(proxyIp) {
      const params = {
        type: 2,
        proxyIp,
      };
      const { data } = await getTotalData(params);
      this.proxyNum = data.data;
    },
    async getInitAccountData(type) {
      const params = {
        type,
      };
      const { data } = await getAccountData(params);
      return data;
    },
    async getAccountList() {
      const { data } = await this.getInitAccountData(1);
      this.account = data;
    },
    async getProxyIpList() {
      const { data } = await this.getInitAccountData(2);
      this.proxyIp = data;
    },
    async renderIpLine() {
      const params = {
        type: 2,
        startDate: "2021-09-07 00:00:00",
      };
      const { data } = (await requestData(params)).data;
      new Line("container2", {
        autoFit: true,
        height: 500,
        data,
        xField: "date",
        yField: "total",
        seriesField: "dimension",
        tooltip: { showMarkers: false },
      }).render();
    },
    async totalData() {
      const { data } = (await getTotalData()).data;
      this.total = data.total;
      this.today = data.todayTotal;
    },
  },
  async mounted() {
    await this.renderAccountLine();
    await this.renderIpLine();
    await this.totalData();
    await this.getAccountList();
    await this.getProxyIpList();
  },
  setup() {},
};
</script>
<style>
.panel-item {
  width: 280px;
  height: 180px;
  margin-left: 10px;
}
.panel-container {
  display: flex;
  justify-content: space-between;
}
.chart-container {
  margin-top: 50px;
}
.panel-font {
  font-size: 30px;
}
.time-font {
  margin-top: 10px;
  font-size: 13px;
  color: #999;
}
</style>