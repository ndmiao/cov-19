<template>
    <div id="AllBack">
        <div id="NewsBack">
            <div class="NewsTitle"><h1>国内外疫情资讯</h1></div>
            
            <div class="Card">
                  <el-carousel :interval="4000" type="card" height="200px">
                        <el-carousel-item v-for="item in img_list" :key="item">                         
                            <a :href="item.url" target=_blank><img :src="item.pic" alt=""></a>
                            <div class="showtitle"><div class="cardtitle">{{item.title}}</div></div>
                        <!-- <h3 class="medium">{{ item }}</h3> -->
                        </el-carousel-item>
                  </el-carousel>
            </div>
            <div class="China">
                <div class="infinite-list-wrapper" style="overflow:auto;height:100%;width:100%">
                    <ul
                    class="list"
                    v-infinite-scroll="load"
                    infinite-scroll-disabled="disabled">
                    <li v-for="i in count" :key="i" class="list-item">
                        <div class="cardstyle">
                            <a :href="ChinaNews[i-1].url" target=_blank><div class="card_pic"><img :src="ChinaNews[i-1].galleryphoto" alt=""></div></a>
                            <div class="card_title"><h4>{{ChinaNews[i-1].title}}</h4></div>
                            <div class="card_source">{{ChinaNews[i-1].content_y}}</div>
                            <div class="card_time">{{ChinaNews[i-1].pubtime}}</div>
                        </div>
                      
                        <hr>
                    </li>
                    </ul>
                    <p v-if="loading">加载中...</p>
                    <p v-if="noMore">没有更多了</p>
                </div>
            </div>
            <div class="World">
                <div class="infinite-list-wrapper" style="overflow:auto;height:100%">
                    <ul
                    class="list"
                    v-infinite-scroll="Worldload"
                    infinite-scroll-disabled="Worlddisabled">
                    <li v-for="i in WorldCount" :key="i" class="list-item">
                        <div class="cardstyle">
                            <a :href="WorldNews[i-1].url" target=_blank><div class="card_pic"><img :src="WorldNews[i-1].galleryphoto" alt=""></div></a>
                            <div class="card_title"><h4>{{WorldNews[i-1].title}}</h4></div>
                            <div class="card_source">{{WorldNews[i-1].content_y}}</div>
                            <div class="card_time">{{WorldNews[i-1].pubtime}}</div>
                        </div>
                        <hr>                      
                    </li>
                    </ul>
                    <p v-if="Worldloading">加载中...</p>
                    <p v-if="WorldnoMore">没有更多了</p>
                </div>                
            </div>
        </div>
            <div id="left-nav">
                <div class="head"><h3>页面选择</h3></div>
                <div class="hide">
                
                    <div @click="go(0)"><el-link icon="el-icon-map-location"> 全球疫情</el-link></div>
                    <div @click="go(1)"><el-link icon="el-icon-position"> 全国疫情</el-link></div>
                    <div><el-link icon="el-icon-chat-line-round"> 时事新闻</el-link></div>
                    <div @click="go(3)"><el-link icon="el-icon-user"> 后台登陆</el-link></div>
                </div>
            <div class="show" @click="hide_show">
                <span class="el-icon-menu"></span>
            </div> 
            </div>     
    </div>
</template>

<style scoped>
@import '../assets/css/news.css';
@import '../assets/css/nav.css';
</style>

<style>
  .infinite-list-wrapper {
    overflow-x: hidden !important;
  }
</style>


<script>
let flag=0;
import axios from 'axios'; 
export default {
    data () {
      return {
        count: 5,
        WorldCount: 5,
        loading: false,
        Worldloading: false,
        img_list:[

            ],
        ChinaNews: [],
        WorldNews: [],
      }
    },
    computed: {
      noMore () {
        return this.count >= 100
      },
      disabled () {
        return this.loading || this.noMore
      },
      WorldnoMore () {
        return this.WorldCount >= 100
      },
      Worlddisabled () {
        return this.Worldloading || this.WorldnoMore
      }
    },
    methods:{ 
      // 获取新闻
      getNews() {
        const url = 'http://127.0.0.1:5000/getnews';
        axios.get(url).then((res) => {
          this.img_list = res.data
        })
        .catch((error) => {
          console.error(error);
        });
    },       
    // 无限加载 
      load () {
        this.loading = true
        setTimeout(() => {
          this.count += 5
          this.loading = false
        }, 2000)
      },
      Worldload () {
        this.Worldloading = true
        setTimeout(() => {
          this.WorldCount += 5
          this.Worldloading = false
        }, 2000)
      },

    GetNews() {
      const url = 'http://127.0.0.1:5000/News';
      axios.get(url).then((res) => {
        this.ChinaNews = res.data.ChinaNews;
        this.WorldNews = res.data.WorldNews;
      })
      .catch((error) => {
        console.error(error);
      })
    },
    // 跳转页面  
      go(page) {
        if (page==0){
          this.$router.push('/')}
        else if (page==1){
          this.$router.push('/China')
        }

        else if (page == 3){
          this.$router.push('/Load')
        }
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
    },
    created() {
      this.GetNews();
      this.getNews();
    },
}
</script>


