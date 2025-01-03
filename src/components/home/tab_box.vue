<template>
  <div class="tab_box">
    <el-tabs type="border-card">
      <el-tab-pane label="我的评论">
        <el-collapse v-model="activeNames" @change="handleChange">
          <div v-if="res_error !== undefined">
            请先<a href="login">登录</a>
          </div>
          <div v-else v-for="(posted_comment, index) in posted_comments" :key="posted_comment.id">
            <el-collapse-item :title="`评论条目:${posted_comment.entry_title}`" :name="'comment-' + index">
              <div class="comment-meta">
                于 {{ posted_comment.created }} 创建，
                
              </div>
              <div class="comment-body">
                {{ posted_comment.title }}:
                <span>{{ posted_comment.body }}</span>
              </div>
            </el-collapse-item>
          </div>
        </el-collapse>

      </el-tab-pane>
      <el-tab-pane label="访问记录">
        <el-collapse v-model="activeNames" @change="handleChange">
          <div v-if="res_error !== undefined">
            请先<a href="login">登录</a>
          </div>
          <div v-else v-for="(record, index) in records" :key="index">
            <el-collapse-item :title="record.title" :name="record.entry_id.toString()"> <!-- 使用唯一的 entry_id -->
              <div class="comment-meta">
                于 {{ record.created }} 访问
              </div>
              <div class="comment-body">
                <span>{{ record.description }}</span>
              </div>
            </el-collapse-item>
          </div>
        </el-collapse>
      </el-tab-pane>
    </el-tabs>
  </div>
  <div style="margin: 20px 0"></div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref } from 'vue'
export default {
  name: 'tab_box',
  setup() {
    const posted_comments = ref();
    const res_error = ref();
    const records = ref();
    const activeNames = ref(['1']);
    const handleChange = (val) => {
      console.log(val)
    };
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/get_posted_comments', { withCredentials: true });
        console.log('get_posted_comments response data:', response);
        const data = response.data;
        posted_comments.value = data.comments;
        res_error.value = data.error;
        const his_response = await axios.get('/api/get_history', { withCredentials: true });
        records.value = his_response.data.records;
        console.log('get_posted_comments response comments:', posted_comments.value);
        console.log('get_posted_comments response error:', res_error.value);
        console.log('get_history response records:', records.value);
      } catch (error) {
        console.error('get_posted_comments error:', error);
      }
    };
    onMounted(() => {
      fetchData();
    });
    return {
      activeNames,
      posted_comments,
      records,
      res_error,
      handleChange
    }
  }
}
</script>



<style scoped></style>
