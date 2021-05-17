<template>
    <div class="login-box">
        <!-- 通过:rules="loginFormRules"来绑定输入内容的校验规则 -->
        <el-form :rules="loginFormRules" ref="loginForm" :model="loginForm" label-position="right" label-width="auto" show-message>
            <div class="title-postion"><span class="login-title">欢迎登录</span></div>
            <div style="margin-top: 5px"></div>
            <el-form-item label="用户名" prop="loginName">
                <el-col :span="22">
                    <el-input type="text" v-model="loginForm.loginName"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item label="密码" prop="loginPassword">
                <el-col :span="22">
                    <el-input type="password" v-model="loginForm.loginPassword"></el-input>
                </el-col>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="loginSubmit('loginForm')">登录</el-button>
                <el-button type="primary" @click="resetForm('loginForm')">重置</el-button>

            </el-form-item>
        </el-form>
    </div>
</template>
<script>

    import axios from 'axios'; 
    export default {
        
        name: "login",
        data() {
            return {
                logiinstatus: 0,
                loginForm: {
                    loginName: '',
                    loginPassword: ''
                },
                // 表单验证，需要在 el-form-item 元素中增加 prop 属性
                loginFormRules: {
                    loginName: [
                        {required: true, message: '账号不可为空', trigger: 'blur'}
                    ],
                    loginPassword: [
                        {required: true, message: '密码不可为空', trigger: 'blur'}
                    ]
                }
            }
        },
        methods: {
            open1() {
        this.$message({
          message: '登陆成功',
          type: 'success'
        });
        },
              getStatus() {
        const url = 'http://127.0.0.1:5000/getstatus';
        axios.get(url).then((res) => {
          this.logiinstatus = res.data.status
          if(this.logiinstatus == 1){
              this.$router.replace("/Admin");
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },  
            loginSubmit(formName) {
                // 为表单绑定验证功能
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        // 使用 vue-router 路由到指定页面，该方式称之为编程式导航
                        const url = 'http://127.0.0.1:5000/pass'
                        axios.post(url,                              
                        {
                            userName: this.loginForm.loginName,
                            password: this.loginForm.loginPassword,   
                            status: 1                 
                        }).then((res) => {
                            if(res.data.code == 'success'){
                                this.open1();
                                console.log("to Admin");
                                this.$router.replace("/Admin");
                            }
                            else { 
                                this.$message.error('账号不存在或者密码错误'); 
                                this.resetForm(formName)  
                            }
                        }).catch((error) => {

                        console.error(error);})


                    } else {
                        return false;
                    }
                });
            },

            
            
      resetForm(formName) {
        console.log("reset")
        this.$refs[formName].resetFields();
      }
        },
        created() {
this.getStatus()
        }
    }
</script>
<style scoped>
    .login-box {
        position: absolute;
        top: 30%;
        left: 35%;
        border: 1px solid #DCDFE6;
        width: 350px;
        padding: 15px 35px 15px 35px;
        border-radius: 5px;
        -webkit-border-radius: 5px;
        -moz-border-radius: 5px;
        box-shadow: 0 0 25px white;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-title {
        color: #66CD00;
        font-size: 30px;
        font-weight: bold;
    }
    .title-postion {
        padding: 35px 35px 30px 35px;
        display: flex;
        justify-content: center;        
    }

</style>
