<template>
    <div class="base">
        <!-- 注册登录界面 -->
        <div class="loginAndRegist">
            <!--登录表单-->
            <div class="loginArea">
                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <!-- 标语 -->
                    <div v-show="isShow" class="title">
                        <RouterLink to="/rate"> SIGN&nbsp;&nbsp;IN </RouterLink>
                    </div>
                </transition>
                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <!-- 密码框和用户名框 -->
                    <div v-show="isShow" class="pwdArea">
                        <div style="flex: 1; justify-content: center; display: flex; margin-top: 70px; ">
                            <el-input class="username" v-model="loginUser.name"
                                style="width: 250px; height: 50px; border-radius: " clearable
                                placeholder="用户名"></el-input>
                        </div>
                        <div style="flex: 1; justify-content: center; display: flex;">
                            <el-input placeholder="密码" v-model="loginUser.password" style="width: 250px; height: 50px;"
                                show-password></el-input>
                        </div>
                    </div>
                </transition>
                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <!-- 登录注册按钮 -->
                     <div class="btnArea">
                        <div v-show="isShow" >               
                                <el-button type="success" round style="background-color: #257B5E;letter-spacing: 5px"
                                @click="UserLogin">用户登录</el-button>        
                        </div>
                        <div v-show="isShow" >               
                            <el-button type="success" round style="background-color: #257B5E;letter-spacing: 5px"
                            @click="goToHome">游客登录</el-button>        
                        </div>
                    </div>
                </transition>               
            </div>
            <!-- 注册表单 -->
            <div class="registArea">
                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <!--  注册表头-->
                    <div v-show="!isShow" class="rigestTitle">
                        SIGN&nbsp;&nbsp; UP
                    </div>
                </transition>
                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <!--            注册表单-->
                    <div v-show="!isShow" class="registForm">
                        <div style="flex: 1;display: flex;justify-content: center;align-items: center">
                            用&nbsp;&nbsp;&nbsp;户&nbsp;&nbsp;&nbsp;名:
                            <el-input placeholder="请输入用户名" v-model="regUser.regUsername"
                                style="width: 250px; height: 40px; margin-left: 10px;font-size: 18px;" clearable>
                            </el-input>
                        </div>
                        <el-alert
                            v-if="showUsernameWarning"
                            title="用户名必须是3到20个字符，只能包含字母、数字、下划线、点和中文字符，且不能以特殊字符开头或结尾"
                            type="warning"
                            show-icon
                            style="margin-top: 10px;"
                        ></el-alert>
                        <div style="flex: 1;display: flex;justify-content: center;align-items: center">
                            密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码:
                            <el-input placeholder="请输入密码"
                                style="width: 250px; height: 40px; margin-left: 10px;font-size: 18px;"
                                maxlength="20"
                                minlength="6"
                                show-word-limit
                                @input="handleInput('regPwd', $event)"
                                v-model="regUser.regPwd" show-password></el-input>
                        </div>
                        <el-alert
                        v-if="showWarning1"
                        title="输入的密码长度必须至少为6个字符"
                        type="warning"
                        show-icon
                        style="margin-top: 10px;"
                        ></el-alert>
                        <el-alert
                        v-if="showMaxLengthWarning1"
                        title="输入的密码长度已达到最大长度"
                        type="warning"
                        show-icon
                        style="margin-top: 10px;"
                        ></el-alert>
                        <div style="flex: 1;display: flex;justify-content: center;align-items: center;">
                            确&nbsp;认&nbsp;密&nbsp;码:
                            <el-input placeholder="请再次输入密码"
                                style="width: 250px; height: 40px; margin-left: 10px;font-size: 18px;"
                                maxlength="20"
                                minlength="6"
                                show-word-limit
                                @input="handleInput('regRePwd', $event)"
                                v-model="regUser.regRePwd" show-password></el-input>
                        </div>
                        <el-alert
                        v-if="showWarning2"
                        title="输入的密码长度必须至少为6个字符"
                        type="warning"
                        show-icon
                        style="margin-top: 10px;"
                        ></el-alert>
                        <el-alert
                        v-if="showMaxLengthWarning2"
                        title="输入的密码长度已达到最大长度"
                        type="warning"
                        show-icon
                        style="margin-top: 10px;"
                        ></el-alert>
                        <el-alert 
                        v-if="showMismatchWarning"
                        title="两次输入的密码不一致"
                        type="warning"
                        show-icon
                        style="margin-top: 10px;"
                        ></el-alert>
                        <div style="flex: 1;display: flex;justify-content: center;align-items: center;">
                            邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;箱:
                            <el-input placeholder="请输入邮箱"
                                style="width: 250px; height: 40px; margin-left: 10px;font-size: 18px;"
                                v-model="regUser.email" ></el-input>
                        </div>
                        <div style="flex: 1;display: flex;justify-content: center;align-items: center">
                            验&nbsp;&nbsp;&nbsp;证&nbsp;&nbsp;&nbsp;码:
                            <el-input placeholder="请输入验证码" v-model="regUser.verification_code"
                                style="width: 140px; height: 40px; margin-left: 10px;font-size: 18px;" clearable>
                            </el-input>
                            <el-button @click="sendVerificationCode" style="margin-left: 10px">发送验证码</el-button>
                        </div>

                    </div>
                 
                </transition>
                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <!--            注册按钮-->
                    <div v-show="!isShow" class="registBtn">
                        <el-button type="success" round style="background-color: #257B5E;letter-spacing: 5px"
                            @click="userRegister">注册</el-button>
                    </div>
                </transition>
            </div>
            <!-- 信息展示界面 -->
            <div id="aaa" class="showInfo" :style="{
                borderTopRightRadius: styleObj.bordertoprightradius,
                borderBottomRightRadius: styleObj.borderbottomrightradius,
                borderTopLeftRadius: styleObj.bordertopleftradius,
                borderBottomLeftRadius: styleObj.borderbottomleftradius,
                right: styleObj.rightDis
            }" ref="showInfoView">

                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <div v-show="isShow"
                        style="display: flex;flex-direction: column;align-items: center;justify-content: center;width: 100%;height: 100%">
                        <!-- 欢迎语 -->
                        <div
                            style="flex: 2;display: flex;align-items: center;font-size: 22px;color: #000000;font-weight: bold">
                            欢迎登入TJ Life forum系统
                        </div>
                        <!-- 欢迎图片 -->
                        <div style="flex: 2">
                            <el-button type="success" style="background-color:#257B5E;border: 1px solid #ffffff;" round
                                @click="changeToRegiest">还没有账户？点击注册</el-button>
                        </div>
                    </div>
                </transition>

                <transition name="animate__animated animate__bounce" enter-active-class="animate__fadeInUp"
                    leave-active-class="animate__zoomOut" appear>
                    <div v-show="!isShow"
                        style="display: flex;flex-direction: column;align-items: center;justify-content: center;width: 100%;height: 100%">
                        <!-- 欢迎语 -->
                        <div
                            style="flex: 2;display: flex;align-items: center;font-size: 22px;color: #FFFFFF;font-weight: bold">
                            欢迎注册
                        </div>
                        <!-- 欢迎图片 -->
                        <div style="flex: 2">
                            <el-button type="success" style="background-color:#257B5E;border: 1px solid #ffffff;" round
                                @click="changeToLogin">已有账户？点击登录</el-button>
                        </div>
                    </div>
                </transition>
            </div>
        </div>

    </div>
    <div class="xxxx">
        <RouterView></RouterView>
    </div>
</template>
<script>
import { ref ,watch} from 'vue'
import { RouterView,RouterLink } from 'vue-router'
import axios from 'axios';

const value = ref('')
const options = [
    {
        value: 'YES',
        label: 'YES',
    },
    {
        value: 'NO',
        label: 'NO',
    },

]
const input = ref('')

export default {
    
    data() {
        return {
            loginUser: {
                name: "",
                password: ""
            },
            admins: {},
            regUser: {
                regUsername: '',
                regRePwd: '',
                regPwd: '',
                email: '',
                verification_code: ''
            },
            styleObj: {
                bordertoprightradius: '15px',
                borderbottomrightradius: '15px',
                bordertopleftradius: '0px',
                borderbottomleftradius: '0px',
                rightDis: '0px'
            },
            isShow: true,
            showWarning1: false,
            showWarning2: false,
            showMaxLengthWarning1: false,
            showMaxLengthWarning2: false,
            showMismatchWarning: false,
            showUsernameWarning: false,
            maxLength: 20
        }
    },
    watch: {
        'regUser.regPwd'(newVal) {
            if (newVal.length > 0 && newVal.length < 6) {
                this.showWarning1 = true
            } else {
                this.showWarning1 = false
            }
            // 在用户输入密码时，不显示密码不一致的警告
            this.showMismatchWarning = false
        },
        'regUser.regRePwd'(newVal) {
            if (newVal.length > 0 && newVal.length < 6) {
                this.showWarning2 = true
            } else {
                this.showWarning2 = false
            }
            // 在用户输入确认密码时，检查密码是否一致
            if (newVal !== this.regUser.regPwd) {
                this.showMismatchWarning = true
            } else {
                this.showMismatchWarning = false
            }
        },
        'regUser.regUsername'(newVal) {
            this.validateUsername()
        }
    }, 
    methods: {
        handleInput(field, value) {
            if (field === 'regPwd') {
                if (value.length >= this.maxLength) {
                this.showMaxLengthWarning1 = true;
                } else {
                this.showMaxLengthWarning1 = false;
                }
            } else if (field === 'regRePwd') {
                if (value.length >= this.maxLength) {
                this.showMaxLengthWarning2 = true;
                } else {
                this.showMaxLengthWarning2 = false;
                }
            }
        },
        validateUsername() {
            const username = this.regUser.regUsername
            const usernameRegex = /^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{2,19}$|^[\u4e00-\u9fa5]{3,20}$/ 
            // 3-20个字符，只能包含字母、数字、下划线、点和中文字符，且不能以特殊字符开头或结尾
            this.showUsernameWarning = !usernameRegex.test(username)
        },
        changeToRegiest() {
            this.styleObj.bordertoprightradius = '0px'
            this.styleObj.borderbottomrightradius = '0px'
            this.styleObj.bordertopleftradius = '15px'
            this.styleObj.borderbottomleftradius = '15px'
            this.styleObj.rightDis = '50%'
            this.isShow = !this.isShow
        },
        changeToLogin() {
            this.styleObj.bordertoprightradius = '15px'
            this.styleObj.borderbottomrightradius = '15px'
            this.styleObj.bordertopleftradius = '0px'
            this.styleObj.borderbottomleftradius = '0px'
            this.styleObj.rightDis = '0px'
            this.isShow = !this.isShow
        },
        async UserLogin() {
            try {
                const response = await axios.post('/auth/login', {
                    username: this.loginUser.name,  // 确保传递正确的用户名
                    password: this.loginUser.password  // 确保传递正确的密码
                },{
                    withCredentials: true  // 确保每个请求都带上 cookie
                });

                if (response.data.status === "success") {
                    if (this.loginUser.name == "admin") {
                        // 跳转到管理员页面
                        window.location.replace('http://113.44.59.183:5000/auth/admin_dashboard');
                    } else {
                        // 跳转到普通用户页面
                        this.$router.push('/');
                    }
                } else {
                    alert(response.data.message || "Login failed");
                }   
            } catch (error) {
                console.error("Login failed:", error.response?.data?.message || error.message);
                alert(error.response?.data?.message || "Login failed");
            }
        },

        // 跳转到主页
        goToHome() {
            this.$router.push('/home');  // 跳转到 /home 路由
        },
        async sendVerificationCode() {
            // 检查密码和确认密码长度是否一致且符合要求
            if (
                this.regUser.regPwd.length < 6 ||
                this.regUser.regPwd.length > this.maxLength ||
                this.regUser.regPwd !== this.regUser.regRePwd ||
                this.showUsernameWarning === true
            ) {
                alert('存在输入格式错误，请检查输入！');
                return
            }
            try {
                const response = await axios.post('/auth/send_verification_code', {
                    email: this.regUser.email
                });
                alert(response.data.message);  // 显示验证码发送成功信息
                // 保存验证码以便注册时使用
                this.sentVerificationCode = response.data.verification_code;
                console.log("Verification code sent:", this.sentVerificationCode);  // Debugging line
            } catch (error) {
                alert(error.response?.data?.message || 'Failed to send verification code.');
            }
        },

        userRegister() {
            // 表单验证逻辑
            if (this.regUser.regPwd !== this.regUser.regRePwd) {
                alert("Passwords do not match!");
                return;
            }

            // 检查是否输入了验证码
            if (!this.regUser.verification_code) {
                alert("Verification code is required!");
                return;
            }

            // 发送注册数据
            axios.post("/auth/register", {
                regUsername: this.regUser.regUsername,
                regPwd: this.regUser.regPwd,
                regRePwd: this.regUser.regRePwd,
                email: this.regUser.email,
                verification_code: this.regUser.verification_code,  // 用户输入的验证码
                sent_verification_code: this.sentVerificationCode  // 发送的验证码
            }, { withCredentials: true })
            .then(response => {
                const data = response.data;
                if (data.status === "success") {
                    alert("注册成功！");
                    this.$router.push("/login");
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error("Registration error:", error.response || error);
                alert("An error occurred during registration.");
            });
        }

    },
}
</script>

<style scoped>
/* @import '../assets/css/Login.css' */
.base {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-image: url("../images/用户注册.jpg");
    background-size: cover;
    /* 使用 cover 使背景图片填充整个页面 */
    background-position: center;
    /* 使背景图片居中 */
    background-size: 100%;
}

.loginAndRegist {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.loginArea {
    background-color: rgba(255, 255, 255, 0.5);
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
    height: 500px;
    width: 400px;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
}

.registArea {
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
    height: 500px;
    width: 400px;
    background-color: rgba(255, 255, 255, 0.8);
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.showInfo {
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
    position: absolute;
    height: 500px;
    width: 400px;
    z-index: 2;
    top: 0;
    right: 0;
    background-image: url("../images/放大.jpg");
    background-color: rgba(255, 255, 255, 0.5);
    /* 半透明背景 */
    background-size: cover;
    /* 改为 cover */
    background-position: center;
    /* 背景居中 */
    transition: background-size 1.0s ease-in-out;
    /* 添加平滑过渡 */
    background-size: 100%;
}


.showInfo:hover {
    background-size: 120%;
    
}

.title {
    width: 100%;
    flex: 1;
    border-bottom: 1px solid #257B5E;
    display: flex;
    align-items: center;
    color: #257B5E;
    ;
    font-weight: bold;
    font-size: 36px;
    display: flex;
    justify-content: center;
}

#aaa {
    transition: 0.3s linear;
}

.pwdArea {
    width: 100%;
    flex: 2;
    display: flex;
    flex-direction: column;
    display: flex;
    flex-direction: column;


}

.pwdArea input {
    outline: none;
    height: 30%;
    border-radius: 500px;
    padding-left: 50px;
    font-size: 10px;
    border: 1px solid gray;
}

.pwdArea input:focus {
    border: 2px solid #257B5E;
}

.btnArea {
    flex: 1;
    width: 100%;
    display: flex;
    justify-content: space-around;
    align-items: center;
    flex-direction: row;
}

.rigestTitle {
    width: 70%;
    flex: 1;
    color: #257B5E;
    font-weight: bold;
    font-size: 36px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 1px solid #257B5E;
}

.registForm {
    flex: 2;
    display: flex;
    flex-direction: column;
    color: #257B5E;
    font-size: 16px;
}

.registForm input {
    outline: none;
    height: 30%;
    border-radius: 13px;
    padding-left: 10px;
    font-size: 12px;
    border: 1px solid gray;
}

.registForm input:focus {
    border: 2px solid #257B5E;
}

#elselect:focus {
    border: 2px solid #257B5E;
}

.registBtn {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}
.xxxx {
    /* 设置背景颜色 */
    background-color: rgba(255, 255, 255, 0.8);
    /* 设置边距 */
    margin: 0;
    /* 设置填充 */
    padding: 20px;
    /* 设置其他样式 */
    border: 1px solid #ccc;
}
</style>
