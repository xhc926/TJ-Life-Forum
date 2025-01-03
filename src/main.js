import './assets/main.css'
import './assets/base.css'
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import  zhCn  from 'element-plus/dist/locale/zh-cn.mjs'
import 'element-plus/dist/index.css'
import App from './App.vue'

import './comm.js'
import './jquery-1.8.3.min.js'
import router from './router'
import axios from 'axios'
//import axios from './axios/index.js'
//import Vue from 'vue'

//Vue.prototype.$axios = axios;
axios.defaults.baseURL = 'http://localhost:5000'; // Flask 后端的基本 URL
axios.defaults.headers.post['Content-Type'] = 'application/json';


const app=createApp(App)
app.use(ElementPlus,{
    locale:zhCn
})
app.use(router)
app.mount('#app')
