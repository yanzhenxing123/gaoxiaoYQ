(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-22e79049"],{"08da":function(t,e,s){},"12c1":function(t,e,s){},"47b0":function(t,e,s){"use strict";s("a161")},"6dfb":function(t,e,s){"use strict";s("08da")},"7bbd":function(t,e,s){"use strict";s("8b53")},"8b53":function(t,e,s){},"98ef":function(t,e,s){"use strict";s("12c1")},a161:function(t,e,s){},bb51:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"home"},[s("div",{staticClass:"news_map"},[s("singleMap")],1),s("div",{staticClass:"home_header"},[s("el-button",{staticClass:"cqupt item",attrs:{type:"primary"},on:{click:t.cqupt}},[t._v("重邮版")]),s("div",{staticClass:"top_bar"},[s("div",{staticClass:"center_content"},[s("div",{staticClass:"topleft"},[s("el-button",{staticClass:"subject item",attrs:{size:"medium"},on:{click:function(e){return t.change(1)}}},[t._v("学科建设")]),s("el-button",{staticClass:"enroll item",on:{click:function(e){return t.change(2)}}},[t._v("招生就业")]),s("el-button",{staticClass:"teach item",on:{click:function(e){return t.change(3)}}},[t._v("师风师德")])],1),s("el-button",{staticClass:"all",on:{click:function(e){return t.change(9)}}},[t._v("热点舆情总览")]),s("div",{staticClass:"topright"},[s("el-button",{staticClass:"school_construction item",on:{click:function(e){return t.change(4)}}},[t._v("校园基建")]),s("el-button",{staticClass:"bad item",on:{click:function(e){return t.change(5)}}},[t._v("学术不端")]),s("el-button",{staticClass:"epidemic_health item",on:{click:function(e){return t.change(6)}}},[t._v("疫情专题")])],1)],1)])],1),s("div",{staticClass:"home_content"},[s("div",{staticClass:"content_left"},[s("div",{staticClass:"news_index"},[s("newsindex",{ref:"sonMethod"})],1)]),s("div",{staticClass:"content_center"},[s("div",{staticClass:"news_num"},[s("newsNum",{ref:"sonNums"})],1)]),s("div",{staticClass:"contetn_right"},[s("div",{staticClass:"warn"},[s("trend")],1),s("div",{staticClass:"text_analyse"},[s("emotion")],1)])]),s("div",{staticClass:"change_page"},[s("changePage")],1)])},i=[],o=s("743d"),l=s("bec1"),r=s("e48f"),n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"new-container"},[s("div",{staticClass:"news_index_header"},[s("div",{staticClass:"viewpaper"},[s("div",{staticClass:"news_index_title"},[t._v("热度新闻指数")]),s("div",{staticClass:"marque",attrs:{id:"list"}},[t._m(0),t._l(t.allData,(function(e,a){return s("li",{key:a,staticClass:"row ",class:{active:t.isActive==a},on:{mouseover:function(e){return t.changeClass(a)},click:function(e){return t.toReport(a)}}},[s("span",{staticClass:"col"},[t._v(t._s(e.college))]),s("span",{staticClass:"col"},[t._v(t._s(e.raw_text.substring(0,13))+" ...")]),s("span",{staticClass:"col"},[t._v(t._s(e.hot_value))])])}))],2)])]),s("div",{staticClass:"news_index_footer"},[s("div",{staticClass:"viewpaper"},[s("div",{staticClass:"news_index_title"},[t._v("热度评论与走势")]),s("div",{staticClass:"marque"},[t._m(1),t._l(t.commentForm,(function(e,a){return s("li",{key:a,staticClass:"row "},[s("span",{staticClass:"col"},[t._v(t._s(e.comment_content.substring(0,15))+"...")]),s("span",{staticClass:"col"},[t._v(t._s(e.comment_id))])])}))],2),s("div",{ref:"trend_ref",staticClass:"com-chart"})])])])},c=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"row-title"},[s("span",{staticClass:"col"},[t._v("学校名称")]),s("span",{staticClass:"col"},[t._v("舆情内容")]),s("span",{staticClass:"col"},[t._v("新闻指数")])])},function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"row-title"},[s("span",{staticClass:"col"},[t._v("热点评论")]),s("span",{staticClass:"col"},[t._v("评论者ID")])])}],h=(s("1157"),{data(){return{myChart:null,allData:[{college:"",raw_text:"",hot_value:""},{college:"",raw_text:"",hot_value:""},{college:"",raw_text:"",hot_value:""}],isActive:0,commentForm:[{comment_content:"",comment_id:""},{comment_content:"",comment_id:""}],oldNews:[],converData:[],news:[]}},mounted(){this.getData()},updated(){},methods:{onClick(t){this.news=this.$store.state.screenData.data,this.allData=this.news,this.commentForm=this.news[this.isActive].hot_comments,this.oldNews=this.news[this.isActive].history_weibo;let e=[];this.oldNews.map(t=>{e.push(t.hot_value)}),this.converData=e.slice(0,6).reverse(),this.drawLine()},toReport(t){let e=this.allData[t],s={author_id:e.author_id,author_id_id:e.author_id_id,author_avatar:e.author_avatar,raw_text:e.raw_text,author_gender:e.author_gender,weibo_id:e.weibo_id,f:e.gender.f,m:e.gender.m,hot_comments:e.hot_comments,history_weibo:e.history_weibo,comment_word_cloud:e.comment_word_cloud,neg:e.comment_emotion_rate.neg,other:e.comment_emotion_rate.other};this.$store.commit("setNickName",s),this.$store.commit("setAuthor",s),this.$store.commit("setAvatar",s),this.$store.commit("setText",s),this.$store.commit("setGender",s),this.$store.commit("setHistoryWeibo",s),this.$store.commit("setGender",s),this.$store.commit("setCommit",s),this.$store.commit("setCommentCloud",s),this.$store.commit("setCommentEmotion",s),this.$store.commit("setWebId",s),this.$router.push("/manage/report")},getData(t){this.$url.get("news/hot3/").then(t=>{let e=t.data;this.$store.commit("setScreenData",e),this.news=this.$store.state.screenData.data,this.allData=this.news,this.commentForm=this.news[this.isActive].hot_comments,this.oldNews=this.news[this.isActive].history_weibo;let s=[];this.oldNews.map(t=>{s.push(t.hot_value)}),this.converData=s.slice(0,6).reverse(),this.drawLine()}).catch(t=>{}),this.changeClass(0)},drawLine(){this.myChart=this.$echarts.init(document.querySelector(".com-chart"));const t={title:{show:!0,text:"博主历史新闻热度",textStyle:{align:"center",color:"#98E3F1",top:5,fontSize:16,fontWeight:"normal"},top:"0",left:"0"},tooltip:{trigger:"axis",axisPointer:{lineStyle:{color:{type:"linear",x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:"rgba(0, 255, 233,0)"},{offset:.5,color:"rgba(255, 255, 255,1)"},{offset:1,color:"rgba(0, 255, 233,0)"}],global:!1}}}},grid:{top:"20%",left:"1%",right:"10%",bottom:"42%",containLabel:!0},xAxis:[{type:"category",axisLine:{show:!0},splitArea:{color:"#f00",lineStyle:{color:"#f00"}},axisLabel:{color:"#A9AFC7"},splitLine:{show:!0,lineStyle:{color:["#fff"],opacity:.06}},boundaryGap:!1,data:["-5","-4","-3","-2","-1","预测"]}],yAxis:[{type:"value",min:0,splitNumber:4,splitLine:{show:!0,lineStyle:{color:["#fff"],opacity:.06}},axisLine:{show:!0},axisLabel:{show:!0,margin:20,textStyle:{fontSize:10,color:"#A9AFC7"}},axisTick:{show:!0}}],series:[{type:"line",smooth:!1,showAllSymbol:!0,symbol:"circle",symbolSize:10,lineStyle:{normal:{color:"#2CABE3"}},label:{show:!0,position:"top",textStyle:{color:"#2CABE3"}},itemStyle:{color:"#fff",borderColor:"#2CABE3",borderWidth:2},tooltip:{show:!1},areaStyle:{normal:{color:new this.$echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:"rgba(61,234,255, 0.9)"},{offset:1,color:"rgba(61,234,255, 0)"}],!1),shadowColor:"rgba(53,142,215, 0.9)",shadowBlur:20}},data:this.converData}]};this.myChart.setOption(t)},changeClass(t){this.isActive=t,this.commentForm=this.allData[this.isActive].hot_comments,this.oldNews=this.allData[this.isActive].history_weibo;let e=[];this.oldNews.map(t=>{e.push(t.hot_value)}),this.converData=e.slice(0,6).reverse(),this.updataOption()},updataOption(){const t={series:[{type:"line",smooth:!1,showAllSymbol:!0,symbol:"circle",symbolSize:10,lineStyle:{normal:{color:"#2CABE3"}},label:{show:!0,position:"top",textStyle:{color:"#2CABE3"}},itemStyle:{color:"#fff",borderColor:"#2CABE3",borderWidth:2},tooltip:{show:!1},areaStyle:{normal:{color:new this.$echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:"rgba(61,234,255, 0.9)"},{offset:1,color:"rgba(61,234,255, 0)"}],!1),shadowColor:"rgba(53,142,215, 0.9)",shadowBlur:20}},data:this.converData}]};this.myChart.setOption(t)},resizeChart(){this.myChart&&this.myChart.resize()}}}),m=h,d=(s("6dfb"),s("2877")),u=Object(d["a"])(m,n,c,!1,null,"578886b6",null),_=u.exports,v=function(){var t=this,e=t.$createElement;t._self._c;return t._m(0)},p=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"bar-container"},[s("div",{staticClass:"title"},[t._v("各高校新闻情感分析")]),s("div",{staticClass:"com-chart4"})])}],w={name:"emotion",data(){return{myChart:null,allData:null,startValue:0,endValue:3,timeId:null}},mounted(){this.drawLine(),this.getData(),window.addEventListener("resize",this.resizeChart)},destroyed(){window.removeEventListener("resize",this.resizeChart),clearInterval(this.timeId)},methods:{drawLine(){this.myChart=this.$echarts.init(document.querySelector(".com-chart4"));const t={tooltip:{trigger:"axis",axisPointer:{type:"shadow",textStyle:{color:"#fff"}}},grid:{borderWidth:0,top:14,bottom:140,textStyle:{color:"#fff"}},calculable:!0,xAxis:[{type:"category",axisLine:{lineStyle:{color:"rgba(255,255,255,.5)"}},splitLine:{show:!1},axisTick:{show:!1},splitArea:{show:!1},axisLabel:{interval:0,color:"#fff",fontSize:12}}],yAxis:[{type:"value",splitLine:{show:!1},axisLine:{show:!1},axisTick:{show:!1},axisLabel:{interval:0,color:"#fff",fontSize:8},splitArea:{show:!1}}],series:[]};this.myChart.setOption(t),this.myChart.on("mouseover",()=>{clearInterval(this.timeId)}),this.myChart.on("mouseon",()=>{this.startInterval()})},async getData(){const{data:t}=await this.$url.get("news/emotionProportion/");this.allData=t.data,this.allData.sort((t,e)=>e.neg-t.neg),this.updateChart(),this.startInterval()},updateChart(){const t=this.allData.map(t=>t.college),e=this.allData.map(t=>t.neg),s=this.allData.map(t=>t.other),a=this.allData.map(t=>t.neg+t.other),i={xAxis:{data:t},dataZoom:{show:!1,startValue:this.startValue,endValue:this.endValue},series:[{name:"负面",type:"bar",stack:"总量",barMaxWidth:20,barGap:"10%",label:{show:!0},itemStyle:{normal:{color:{type:"linear",x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:"rgba(35, 157, 250, 1)"},{offset:1,color:"rgba(35, 157, 250, 0)"}],global:!1}}},data:e},{name:"正面",type:"bar",stack:"总量",itemStyle:{normal:{color:"rgb(35,250,187)",barBorderRadius:0}},data:s},{name:"总数",type:"line",symbolSize:7,symbol:"circle",label:{show:!0},itemStyle:{normal:{color:"rgba(255, 196, 53, 1)",barBorderRadius:0}},lineStyle:{normal:{width:4,color:{type:"linear",x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:"rgba(255, 67, 2, 1)"},{offset:1,color:"rgba(255, 196, 53, 1)"}],global:!1}}},data:a}]};this.myChart.setOption(i)},startInterval(){this.timeId&&clearInterval(this.timeId),this.timeId=setInterval(()=>{this.startValue++,this.endValue++,this.endValue>this.allData.length-1&&(this.startValue=0,this.endValue=3),this.updateChart()},2e3)},resizeChart(){this.myChart&&this.myChart.resize()}}},f=w,b=(s("47b0"),Object(d["a"])(f,v,p,!1,null,null,null)),C=b.exports,g=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("div",{staticClass:"now_news_num"},[s("div",{staticClass:"news_count"},[t._v("当前舆情总量")]),s("div",{staticClass:"no"},[s("div",{staticClass:"no-hd"},[s("ul",[s("li",[t._v(t._s(t.allnums))]),s("li",[t._v(t._s(t.allnums))])])])])])])},y=[],x={data(){return{allnums:""}},mounted(){this.getData()},methods:{onClick(t){this.allnums=this.$store.state.allNums},async getData(){const{data:t}=await this.$url("news/nums/");this.allnums=t.nums}}},S=x,$=(s("7bbd"),Object(d["a"])(S,g,y,!1,null,null,null)),D=$.exports,k=s("9792"),A=s("4928"),L={data(){return{text:"",isShow:!0,flag:"all",input:"",weibo_id:""}},name:"Home",components:{topBar:o["a"],singleMap:l["a"],trend:r["a"],newsindex:_,emotion:C,newsNum:D,changePage:k["a"],wordCloud:A["a"]},mounted(){this.all()},methods:{all(){this.flag="all",this.$url.get("news/hot3/").then(t=>{let e=t.data;this.allData=t.data,this.$store.commit("setScreenData",e),this.$refs.sonMethod.onClick()}).catch(t=>{})},cqupt(){this.$router.push("/Cqupt")},change(t){let e,s;switch(t){case 9:e=9;break;case 1:e="学科建设";break;case 2:e="招生就业";break;case 3:e="师风师德";break;case 4:e="校园基建";break;case 5:e="学术不端";break;case 6:e="疫情专题";break;default:break}s=9==e?"news/hot3/":"news/hot3/?aspect="+e,this.$url.get(s).then(t=>{let e=t.data;this.allData=t.data,this.$store.commit("setScreenData",e),this.$refs.sonMethod.onClick()}).catch(t=>{})}}},E=L,z=(s("98ef"),Object(d["a"])(E,a,i,!1,null,"5e820fa8",null));e["default"]=z.exports}}]);
//# sourceMappingURL=chunk-22e79049.a8d3a9f3.js.map