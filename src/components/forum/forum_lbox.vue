<template>
  <div class="common-layout whitebg">
    <h2 class="htitle">
      <span class="hnav"></span> 当前论坛 >> {{ cur_forum.forum_name }}
    </h2>
    
    <div v-for="topic in topics" :key="topic.topic_id">
      <div class="topic-card">
        <h3>
          <span style="font-size: 22px; color: #333;">当前话题：</span>
          <router-link :to="`/topic/${topic.topic_id}`" class="topic-link">
            #{{ topic.topic_name }}
          </router-link>
        </h3>

        <div v-for="post in posts.filter(post => post.topic_id === topic.topic_id).slice(0, 3)" :key="post.entry_id" class="comment-box">
          <router-link :to="`/entry/${post.entry_id}`" class="entry-link">
            <h4>{{ post.title }}</h4>

            <el-rate :model-value="getComputedValue(post.avg_rate)" disabled show-score text-color="#ff9900" :max="5"
              :score-template="getScoreTemplate(post.avg_rate)" />

            <div class="popconfirm-container">
              <el-popconfirm title="是否屏蔽" @confirm="handleConfirm('屏蔽')" @cancel="handleCancel('屏蔽')">
                <template #reference>
                  <el-icon><Hide /></el-icon>
                </template>
              </el-popconfirm>
              <el-popconfirm title="是否举报" @confirm="handleConfirm('举报')" @cancel="handleCancel('举报')">
                <template #reference>
                  <el-icon><Tickets /></el-icon>
                </template>
              </el-popconfirm>
            </div>
          </router-link>
        </div>

        <li>
          <router-link :to="{ name: 'topic', params: { topicId: topic.topic_id } }" class="readmore">
            进入话题
          </router-link>
        </li>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { h } from 'vue'
import { Hide, Tickets } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios';

export default {
  components: {
    Hide,
    Tickets,
  },
  setup() {
    const posts = ref([]);
    const topics = ref([]);
    const cur_forum = ref([]);
    const route = useRoute();
    const forumId = route.params.forumId;

    const fetchData = async () => {
      try {
        console.log(forumId);

        const response = await axios.get(`/f/${forumId}`); // 替换为你的后端 API 路径
        posts.value = response.data.posts;
        cur_forum.value = response.data.cur_forum;
        topics.value = response.data.topics;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    onMounted(() => {
      fetchData();
    });

    const getComputedValue = (avgRate) => (avgRate / 2).toFixed(1);
    const getScoreTemplate = (avgRate) => `${avgRate.toFixed(1)} 分`;

    const handleConfirm = (action) => {
      ElMessageBox({
        title: 'Message',
        message: `确认 ${action}`,
        showCancelButton: true,
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then((action) => {
        ElMessage({
          type: 'info',
          message: `执行操作：${action}`,
        });
      });
    };

    const handleCancel = (action) => {};

    return {
      posts,
      topics,
      cur_forum,
      getComputedValue,
      getScoreTemplate,
      handleConfirm,
      handleCancel,
    };
  },
};
</script>

<style scoped>
/* 整体布局 */
.common-layout {
  margin: 0 auto;
  width: 80%;
  padding: 20px;
  background-color: #f8f8f8;
}

.whitebg {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

/* 标题 */
.htitle {
  font-size: 20px;
  color: #333;
  font-weight: 600;
  margin-bottom: 20px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 5px;
}

/* 话题卡片 */
.topic-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.topic-link {
  color: #409EFF;
  text-decoration: underline;
  font-weight: bold;
}

.topic-link:hover {
  color: #66b1ff;
  text-decoration: none;
}

/* 评论框 */
.comment-box {
  background-color: #fafafa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  margin-bottom: 15px;
}

.entry-link h4 {
  font-size: 18px;
  color: #333;
  font-weight: 500;
}

.popconfirm-container {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

/* 评论评分 */
.el-rate {
  margin-top: 10px;
}

.readmore {
  margin-top: 20px;
  color: #096;
  font-size: 14px;
  text-decoration: none;
}

.readmore:before {
  content: "+";
  color: #063;
}

.readmore:hover {
  color: #007bff;
  text-decoration: underline;
}

.readmore:active {
  color: #0056b3;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .common-layout {
    width: 95%;
    padding: 15px;
  }

  .topic-card {
    padding: 15px;
  }

  .comment-box {
    padding: 10px;
  }
}
</style>
