(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-21e63821"],{"0798":function(e,r,s){"use strict";s("e00b")},"73cf":function(e,r,s){"use strict";s.r(r);var t=function(){var e=this,r=e.$createElement,s=e._self._c||r;return s("div",{staticClass:"reg"},[s("div",{staticClass:"reg-box"},[s("h1",[e._v("高校舆情管理系统")]),s("el-form",{ref:"ruleForm",staticClass:"register-form",attrs:{model:e.registerForm,rules:e.registerRules}},[s("el-form-item",{attrs:{prop:"username"}},[s("el-input",{attrs:{placeholder:"请输入您的账户"},model:{value:e.registerForm.username,callback:function(r){e.$set(e.registerForm,"username",r)},expression:"registerForm.username"}})],1),s("el-form-item",{attrs:{prop:"email"}},[s("el-input",{attrs:{placeholder:"请输入您邮箱"},model:{value:e.registerForm.email,callback:function(r){e.$set(e.registerForm,"email",r)},expression:"registerForm.email"}})],1),s("el-form-item",{attrs:{prop:"password"}},[s("el-input",{attrs:{placeholder:"请输入您的密码",type:"password"},model:{value:e.registerForm.password,callback:function(r){e.$set(e.registerForm,"password",r)},expression:"registerForm.password"}})],1),s("el-button",{staticClass:"btn",attrs:{type:"primary",size:"small"},on:{click:function(r){return e.sendRegister()}}},[e._v("注册")]),s("div",{staticClass:"go-login",on:{click:e.goLogin}},[e._v("已有帐号，去登录")])],1)],1)])},i=[],a={name:"register",data(){return{registerForm:{username:"",password:"",email:""},registerRules:{username:[{required:!0,message:"请输入你的帐号",trigger:"blur"},{min:6,max:10,trigger:"blur"}],password:[{required:!0,message:"请输入密码",trigger:"blur"},{min:6,max:15,message:"长度在 6 到 15 个字符",trigger:"blur"}],email:[{required:!0,message:"请输入邮箱地址",trigger:"blur"},{type:"email",message:"请输入正确的邮箱地址",trigger:["blur","change"]}]}}},methods:{goLogin(){this.$router.push("/login")},sendRegister(){let e={username:this.registerForm.username,password:this.registerForm.password,email:this.registerForm.email};this.$url.post("user/register/",e).then(e=>{200==e.data.code&&(this.$message({showClose:!0,message:"恭喜你，注册成功",type:"success"}),this.$router.push("/login")),40003==e.data.code&&this.$message({showClose:!0,message:"信息填写不符合规范",type:"error"})}).catch(e=>{})}}},o=a,l=(s("0798"),s("2877")),m=Object(l["a"])(o,t,i,!1,null,null,null);r["default"]=m.exports},e00b:function(e,r,s){}}]);
//# sourceMappingURL=chunk-21e63821.e830a71f.js.map