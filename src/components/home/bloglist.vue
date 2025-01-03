<template>
    
  <div class="whitebg bloglist">
  <el-tabs type="border-card" >
    <el-tab-pane label="许多人看过">
      <ul>
        <!-- 遍历帖子 -->
        <li v-for="post in posts1" :key="post.entry_id">
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
            <span v-for="tag in entryTags1[post.entry_id]" :key="tag" class="tag">
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
    <el-tab-pane label="推荐帖子">
      <ul>
        <!-- 遍历帖子 -->
        <li v-for="post in posts2" :key="post.avg_rate">
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
            <span v-for="tag in entryTags2[post.entry_id]" :key="tag" class="tag">
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
                  【{{post.topic_name}}】
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
name: 'Bloglist',
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
  const posts1 = ref([]);
  const posts2 = ref([]);
  const comments1 = ref([]);
  const comments2 = ref([]);
  const entryTags1 = ref([]);
  const entryTags2 = ref([]);

  const fetchData = async () => {
    try {
      const [response1, response2] = await Promise.all([
        axios.get('/api/get_most_viewed_posts', { withCredentials: true }), // 替换为你的第一个后端 API 路径
        axios.get('/api/get_recommend_posts', { withCredentials: true }) // 推荐算法接口
      ])
      posts1.value = response1.data.posts;
      comments1.value = response1.data.comments;
      entryTags1.value = response1.data.entry_tags;
      posts2.value = response2.data.posts;
      comments2.value = response2.data.comments;
      entryTags2.value = response2.data.entry_tags;
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const filteredComments = (entryId) => {
    return comments1.value.filter(comment => comment.entry_id === entryId);
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
    posts1,
    comments1,
    entryTags1,
    posts2,
    comments2,
    entryTags2,
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
</style>