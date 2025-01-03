<template>
  <header id="header">
    <div class="navbox">
      <div class="logo">TJ Life forum</div>
      <nav>
        <ul id="starlist">
          <li><router-link to="/home">论坛首页</router-link></li>
          <li><router-link to="/hottest_posts">热帖排行</router-link></li>
          <li class="menu">
            <router-link to="/forum">论坛分类</router-link>
            <ul class="sub">
              <li v-for="forum in forums" :key="forum.forum_id">
                <a href="/forum/${forum.forum_id}" @click.prevent="navigateToForum(forum.forum_id)">
                  {{ forum.forum_name }}
                </a>
              </li>
            </ul>
            <span></span>
          </li>
          <li><router-link to="/message">消息中心</router-link></li>
          <li><router-link to="/about_me">关于我</router-link></li>
        </ul>
      </nav>

      <!--搜索框flex-->
      <div class="flex gap-4 items-center">
        <el-input v-model="input1" style="width: 300px" size="large" placeholder="Please Input" :prefix-icon="Search"
          clearable />
      </div>
      <div class="user">
        <!-- 如果用户已经登录，显示头像和退出按钮，否则显示登录链接 -->
        <template v-if="user">
          <el-avatar class="avatar-icon" :src="user.avatar ? `http://localhost:5000/static/${user.avatar}` : defaultAvatar">user</el-avatar>
          <el-button @click="logout" type="primary" size="small" style="margin-left: 10px;">Log out</el-button>
        </template>
        <template v-else>
          <router-link to="/login">
            <el-avatar class="avatar-icon">user</el-avatar>
          </router-link>
          <router-link to="/login">
            <el-button type="primary" size="small" style="margin-left: 10px;">Log in</el-button>
          </router-link>
        </template>
      </div>
    </div>

  </header>

</template>

<script>
import { UserFilled } from '@element-plus/icons-vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
// 引入默认头像图片
import defaultAvatar from '../images/default-avatar.png';

export default {
  name: 'Header',
  setup() {
    const input1 = ref('');
    const forums = ref([]);
    const user = ref(null);
    const defaultAvatar = '/src/images/default-avatar.png';  // 定义默认头像的路径

    // 获取论坛数据
    const fetchForums = async () => {
      try {
        const response = await axios.get('/api/forums', { withCredentials: true });  // 获取论坛数据
        forums.value = response.data.forums;  // 假设后端返回的数据格式是一个包含论坛对象的数组
        console.log('获取的论坛数据:', response.data);
      } catch (error) {
        console.error('获取论坛数据失败:', error);
      }
    };

    // 获取用户数据
    const fetchUser = async () => {
      try {
        const response = await axios.get('/api/user', { withCredentials: true });  // 假设获取用户数据的接口是 '/api/user'
        user.value = response.data.user;  // 假设后端返回的用户数据存储在 response.data.user
        console.log('获取的用户数据:', response.data);
      } catch (error) {
        console.error('获取用户数据失败:', error);
      }
    };
    const logout = async () => {
      try {
        await axios.post('/auth/logout', {}, { withCredentials: true }); // 假设有一个 /auth/logout 接口来处理登出
        user.value = null; // 清除用户信息
        ElMessage.success('Logged out successfully');
        window.location.href = '/login';  // 重定向到登录页面
      } catch (error) {
        console.error('Logout failed:', error);
        ElMessage.error('Logout failed');
      }
    };
    // 在组件挂载时获取数据
    onMounted(() => {
      fetchForums();
      fetchUser();  // 调用获取用户数据的方法
    });

    return {
      input1,
      Search,
      forums,
      user,
      defaultAvatar, // 返回给模板使用
      logout 
    };
  },
  methods: {
    navigateToForum(forumId) {
      this.$router.push({ name: 'forum', params: { forumId: forumId } });
      window.location.href = `/forum/${forumId}`;
      console.log("navigate to forum: ", forumId);
    }
  }
};
</script>

<style scoped>
.avatar-icon {
  display: flex;
  align-items: center;
  margin-left: 20px;
}

/*header*/
header {
  width: 100%;
  padding: 15px 0;
  background: #1C2327;
  height: 80px;
}

header::before {
  background: #000 linear-gradient(to left, #4cd964, #5ac8fa, #007aff, #34aadc, #5856d6, #ff2d55);
  content: "";
  height: 5px;
  position: absolute;
  top: 0;
  width: 100%;
}

#header {
  position: relative;
  z-index: 1;
  /* 确保header在其他元素之上 */
  display: flex;
}

.logo {
  float: left;
  margin-right: 60px;
  line-height: 50px;
  color: #FFF;
  font-size: 22px
}

/*nav 导航*/

nav {
  float: left;
  height: 50px;
  line-height: 50px;
  text-align: center;
  position: relative;
  z-index: 2;
  /* 确保nav在header之上 */
}

.navbox {
  display: flex;
  align-items: center;
}

.flex {
  display: flex;
  align-items: center;
  margin-left: 20px;
  margin-right: 20px;
}

#starlist li {
  position: relative;
  display: inline;
  float: left;
  width: max-content;
}

#starlist li a {
  display: inline;
  float: left;
  padding: 0 20px;
  color: #fbf7f7
}

#starlist li a:hover,
#starlist #selected,
.selected>a,
#starlist li:hover {
  color: #00c1de;
}

#starlist li:hover a {
  color: #00c1de
}

#starlist ul.sub {
  overflow: hidden;
  position: absolute;
  left: 0;
  top: 50px;
  background: #1C2327;
  display: none;
  z-index: 9
}

#starlist ul.sub li {
  height: 30px;
  line-height: 30px;
  font-size: 14px;
}

#starlist ul.sub li:last-child {
  padding-bottom: 10px
}

#starlist ul.sub li a {
  color: #f8f8f8
}

#starlist ul.sub li a:hover {
  color: #00c1de
}

#starlist li:hover ul.sub {
  display: block
}

/*子菜单*/

#starlist ul.sub {
  overflow: hidden;
  position: absolute;
  left: 0;
  top: 50px;
  background: #1C2327;
  display: none;
  z-index: 9
}

#starlist ul.sub li {
  height: 30px;
  line-height: 30px;
  font-size: 14px;
}

#starlist ul.sub li:last-child {
  padding-bottom: 10px
}

#starlist ul.sub li a {
  color: #f8f8f8
}

#starlist ul.sub li a:hover {
  color: #00c1de
}

#starlist li:hover ul.sub {
  display: block
}
</style>
