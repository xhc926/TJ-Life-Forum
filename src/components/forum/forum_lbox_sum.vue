<template>
  <div class="common-layout whitebg">
    <h2 class="htitle">
        <span class="hnav">
        </span>论坛
    </h2>
    <div v-for="forum in forums" :key="forum.forum_id">
      <div class="forum-card">
        <h3 class="forum-title">{{forum.forum_name}}</h3>
        <div class="forum-meta">
          <span class="created-at">创建时间：<strong>{{forum.created_at}}</strong></span>
        </div>
        <p class="forum-description">{{forum.description}}</p>
        <router-link :to="{ name: 'forum', params: { forumId: forum.forum_id } }" class="readmore">
          进入论坛
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const forums = ref([]);

    const fetchData = async () => {
      try {
        const response = await axios.get(`/api/forums`); // 替换为你的后端 API 路径
        forums.value = response.data.forums;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    onMounted(() => {
      fetchData();
    });

    return {
      forums,
    };
  }
};
</script>

<style scoped>
/* 整体页面布局 */
.common-layout {
  margin: 0 auto;
  width: 80%;
  padding: 20px;
  background-color: #f9f9f9;
}

.whitebg {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2.htitle {
  font-size: 24px;
  color: #333;
  font-weight: bold;
  position: relative;
  margin-bottom: 20px;
}

h2.htitle:after {
  content: "";
  position: absolute;
  width: 80px;
  height: 2px;
  background: #007bff;
  left: 0;
  bottom: 0;
  transition: all .3s ease;
}

h2.htitle:hover:after {
  width: 100px;
}

/* 每个论坛的卡片布局 */
.forum-card {
  background-color: #fff;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.forum-title {
  font-size: 22px;
  color: #333;
  font-weight: bold;
  margin-bottom: 10px;
}

.forum-meta {
  font-size: 14px;
  color: #777;
  margin-bottom: 10px;
}

.created-at {
  color: #999;
}

.forum-description {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 20px;
}

.readmore {
  display: inline-block;
  padding: 8px 15px;
  background-color: #007bff;
  color: #fff;
  border-radius: 30px;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.readmore:before {
  content: "+";
  margin-right: 5px;
}

.readmore:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.readmore:active {
  transform: translateY(2px);
}
</style>
