<template>
  <div>
    <div id="title">全球疫情实时追踪</div>
    <div id="tim">{{realtime}}</div>
    <div id="l1">
      <div id="line" style="weight:90%;height: 90%"></div>
    </div>
    <div id="l2">
      <div id="line2" style="weight:90%;height: 90%"></div>
    </div>
    <div id="m1">
      <div id="globalmap" style="weight:100%;height: 100%;"></div>
    </div>
    <div id="m2">   
      <div class="num"><h2>{{nowconfirm}}</h2></div>
      <div class="num"><h2>{{confirm}}</h2></div>
      <div class="num"><h2>{{dead}}</h2></div>
      <div class="num"><h2>{{heal}}</h2></div>
      <div class="txt"><h2>现存确诊</h2></div>
      <div class="txt"><h2>累计确诊</h2></div>
      <div class="txt"><h2>累计死亡</h2></div>
      <div class="txt"><h2>累计治愈</h2></div>
      
    </div>
    <div id="r1">
      <div id="bar" style="weight:90%;height: 90%"></div>
    </div>
    <div id="r2">
      <div id="pie" style="weight:90%;height: 90%"></div>
    </div>
    <div id="left-nav">
      <div class="head"><h3>页面选择</h3></div>
      <div class="hide">
     
        <div><el-link icon="el-icon-map-location"> 全球疫情</el-link></div>
        <div @click="go(0)"><el-link icon="el-icon-position"> 全国疫情</el-link></div>
        <div @click="go(1)"><el-link icon="el-icon-chat-line-round"> 时事新闻</el-link></div>
        <div @click="go(3)"><el-link icon="el-icon-user"> 后台登陆</el-link></div>
      </div>
      <div class="show" @click="hide_show">
        <span class="el-icon-menu"></span>
      </div>
    </div>
  </div>
</template>




<style scoped>
@import '../assets/css/main.css';
@import '../assets/css/nav.css';
</style>
<script>
  import echarts from "echarts";
  import axios from 'axios'; 
  import gary from '../assets/json/gray';
  import {lineoption,baroption,pieoption,line2option,globaloption} from '../assets/js/chartoption';
  let flag=0;

  export default {
    data () {
    return {
      realtime: '',
      nowconfirm: '',
      confirm: '',
      dead: '',
      heal: '',
    };
  },
    methods:{  
    // 跳转页面  
      go(page) {
        if (page==0){
          this.$router.push('/China')
          } 
        else if (page==1){
          this.$router.push('/News')
        }

        else if (page == 3){
          this.$router.push('/Load')
        }
    },


      // 获取时间
      getTime() {
        const url = 'http://127.0.0.1:5000/gettime';
        axios.get(url).then((res) => {
          this.realtime = res.data
        })
        .catch((error) => {
          console.error(error);
        });
    },  

    // 获取全球数据
      getGlobaldata() {
        const url = 'http://127.0.0.1:5000/getGlobalStasis';
        axios.get(url).then((res) => {
          this.nowconfirm = res.data.globaldata.nowConfirm
          this.confirm = res.data.globaldata.confirm
          this.dead = res.data.globaldata.dead
          this.heal = res.data.globaldata.heal
        })
        .catch((error) => {
          console.error(error);
        })
      },

      // echarts图
      drawcharts(){
        let obj = gary
        echarts.registerTheme('gray',obj)
        var barChart = echarts.init(document.getElementById("bar"),'gray');
        barChart.setOption(baroption)
        barChart.showLoading();

        var pieChart = echarts.init(document.getElementById("pie"),'gray');
        pieChart.setOption(pieoption)
        pieChart.showLoading();

        var lineChart = echarts.init(document.getElementById("line"),'gray');
        lineChart.setOption(lineoption)
        lineChart.showLoading();

        var line2Chart = echarts.init(document.getElementById("line2"),'gray');
        line2Chart.setOption(line2option)
        line2Chart.showLoading();

        const path = 'http://127.0.0.1:5000/getGlobalData';
        axios.get(path).then((res) =>{
        setTimeout(() => {
          barChart.hideLoading();
          barChart.setOption({
            xAxis: [{
                data: res.data.global_confirm8.country
              }],
              series: [{
                  data: res.data.global_confirm8.confirm_add
                }]
                });

          pieChart.hideLoading();
          pieChart.setOption({
            series: [{
              data: res.data.continent_confirm
            }]
          })

          lineChart.hideLoading();
          lineChart.setOption({
            xAxis: [{
                data: res.data.globalhistory.day
              }],
            series:[
              {data:res.data.globalhistory.confirm},
              {data:res.data.globalhistory.nowconfirm},
              {data:res.data.globalhistory.newAddConfirm},
              {data:res.data.globalhistory.dead},
              {data:res.data.globalhistory.heal},
              ]
          })

          line2Chart.hideLoading();
          line2Chart.setOption({
            xAxis: [{
                data: res.data.globalrate.day
              }], 
            series:[
              {data: res.data.globalrate.deadRate},
              {data: res.data.globalrate.healRate}
            ]           
          })      
                },500);})
            .catch((error) => {
              console.error(error);
            });},
      // 画地图
      drawmap(){
                let obj = gary
                echarts.registerTheme('gray',obj)
                var myChart = echarts.init(document.getElementById('globalmap'),'gray');
              myChart.setOption(globaloption);

              myChart.showLoading();
              const path = 'http://127.0.0.1:5000/getWorldMap';
              axios.get(path).then((res) =>{
                setTimeout(() => {
                  myChart.hideLoading();
                  myChart.setOption({
                    series: [{data:res.data}]
                  })
                  },500);})
                  .catch((error) => {
                    console.error(error);
                  });
      },
    // 点击按钮隐藏或者显示
    hide_show(){
          if(flag===0){
      this.startMove(0)
      flag=1
    }
    else{
      this.startMove(-140)
      flag=0
    }
    },
    // 侧边栏动画
      startMove(end){
        var timer;
      var oDiv=document.getElementById('left-nav');
      clearInterval(timer);
      timer=setInterval(function(){
        var speed=0;
        //从-140到0,速度为正，从0到-140，速度为负
        if(oDiv.offsetLeft>end){
          speed=-10;
        }else{
          speed=10;
        }
        if(oDiv.offsetLeft==end){
          clearInterval(timer);
        }else{
          oDiv.style.left=oDiv.offsetLeft+speed+'px';
        }
      },30);
    },
    // 定时加载
    currentTime(){
      setInterval(this.getTime,1000)
      setInterval(this.getGlobaldata,300000)
      setInterval(this.drawcharts,600000)
      setInterval(this.drawmap,600000)
    },
   
    },
    created() {
      this.getGlobaldata();
      this.currentTime();
    },
    mounted() {
  	  this.drawcharts();
      this.drawmap();
  },
  beforeDestroy() {
    clearInterval(this.getTime);
    this.currentTime();
    this.getTime();
  }
  
  }
</script>
 




