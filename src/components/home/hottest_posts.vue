<template>
    
    <div class="whitebg bloglist common-layout">
    <el-tabs type="border-card" >
      <el-tab-pane label="热帖排行">
        <ul>
          <!-- 遍历帖子 -->
          <li v-for="post in posts" :key="post.entry_id">
            <!--帖子标题-->
            <h3 class="blogtitle">
            <router-link :to="{ name: 'entry', params: { entryId: post.entry_id } }" class="readmore">
              {{ post.title }}
            </router-link>
            </h3>
            <!--楼主头像-->
            <span class="blogpic imgscale">
              <i>
                <a :href="post.link">{{ post.category }}</a>
              </i>
              <a :href="post.link" title=""><img :src="post.image" alt="">
              </a>
            </span>
            <!--帖子内容-->
            <p class="blogtext">{{ post.content }}</p>
            <!--帖子标签-->
            <p><small>tags:</small>
              <span v-for="tag in entryTags[post.entry_id]" :key="tag" class="tag">
                <el-tag type="primary">{{tag}}</el-tag>
              </span>
            </p>
            <!--帖子评分-->
            <el-rate
              :model-value="getComputedValue(post.avg_rate)"
              disabled
              show-score
              text-color="#ff9900"
              :max="5"
              :score-template="getScoreTemplate(post.avg_rate)"
            />

            <!--帖子信息-->
            <p class="bloginfo">
                <span>
                  创建于：{{ formatDatetime(post.created) }}</span>
                <span>
                  最新更新：{{ formatDatetime(post.updated) }}</span>
            </p>
            <p>
                <span>
                    【{{ post.forum_name }}】
                </span>
                <span>
                    【{{ post.topic_name }}】
                </span>
            </p>
            <router-link :to="{ name: 'entry', params: { entryId: post.entry_id } }" class="readmore">
                阅读更多
            </router-link>
          </li>
        </ul> 
      </el-tab-pane>
    </el-tabs>

  </div>

</template>

<script>
import image1 from '../../images/1.jpg';
import axios from 'axios';
import { ref, onMounted} from 'vue'

export default {
  name: 'hottest_posts',
  components: {
    image1
  },
  methods: {
    formatDatetime(datetime) {
      const date = new Date(datetime); // 创建一个 Date 对象，假设是 UTC 时间
      date.setHours(date.getHours()); 
      return date; // 格式化为本地日期时间字符串
    }
  },
  setup(){
    const posts = ref([]);
    const comments = ref([]);
    const entryTags = ref([]);

    const fetchData = async () => {
      try {
        const response = await (
          axios.get('/api/get_hottest_posts')
        )
        posts.value = response.data.posts;
        comments.value = response.data.comments;
        entryTags.value = response.data.entry_tags;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    const filteredComments = (entryId) => {
      return comments.value.filter(comment => comment.entry_id === entryId);
    };
    onMounted(() => {
      fetchData();
    });
  // 计算属性，用于将评分值除以 2
  const getComputedValue = (avgRate) => {
      return avgRate / 2;
  };

  // 计算显示的评分值，将评分值乘以 2
  const getScoreTemplate = (avgRate) => {
      return `${avgRate} 分`;
    };
  
  return {
      posts,
      comments,
      entryTags,
      filteredComments,
      getComputedValue,
      getScoreTemplate,
    };
}

}
</script>

<style>
.bloglist li:hover .blogtitle a {
  color: #337ab7;
  cursor: pointer; /* 鼠标悬浮时显示为选择的光标 */
}

.common-layout {
    margin: 0 auto;
    width: 80%;
    padding: 0 10px;
    overflow: hidden;
}

.common-layout ul {
    padding: 10px 0 0
}

.common-layout li {
    overflow: hidden;
    margin-bottom: 20px;
    border-bottom: #eee 1px dashed;
    padding-bottom: 20px;
    position: relative;
}
</style>