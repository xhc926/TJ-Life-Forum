<template>
  <div class="common-layout whitebg">
    <h2 class="htitle">
      <span class="hnav"></span>{{ cur_topic.forum_name }} >> {{ cur_topic.topic_name }} >>
    </h2>

    <!-- 创建条目表单 -->
    <div class="create-entry">
      创建一个条目？
      <el-input
        v-model="title"
        class="entry-input"
        placeholder="请输入新创建的条目标题"
        show-word-limit
      />
      <el-input
        v-model="body"
        type="textarea"
        class="entry-input"
        placeholder="请输入条目的内容"
        show-word-limit
      />

      <div class="tag-container">
        添加标签：
        <el-checkbox-group v-model="selectedTags">
          <el-checkbox
            v-for="tag in tags"
            :key="tag.tag_id"
            :label="tag.name"
          ></el-checkbox>
        </el-checkbox-group>
      </div>

      <el-button
        type="primary"
        class="submit-btn"
        @click="submitApply"
      >提交申请！</el-button>
    </div>

    <!-- 已创建的条目 -->
    <div class="entries-list">
      <div
        v-for="post in posts"
        :key="post.entry_id"
        class="entry-card"
      >
        <div v-if="!is_blocked[post.entry_id]">
          <router-link
            :to="`/entry/${post.entry_id}`"
            class="entry-link"
          >
            <h2 class="entry-title">
              <span class="entry-name">{{ post.title }}</span>
              <span class="entry-rating">
                <el-rate
                  :model-value="getComputedValue(post.avg_rate)"
                  disabled
                  show-score
                  text-color="#ff9900"
                  :max="5"
                  :score-template="getScoreTemplate(post.avg_rate)"
                />
              </span>
            </h2>

            <div class="entry-meta">
              <span>更新时间：{{ formatDatetime(post.updated) }}&nbsp;&nbsp;&nbsp;</span>
              <span>评论次数：{{ post.commented }}&nbsp;&nbsp;&nbsp;</span>
              <span>浏览次数：{{ post.views }}</span>
            </div>
          </router-link>

          <!-- 评论列表 -->
          <div
            v-for="comment in filteredComments(post.entry_id).slice(0, 3)"
            :key="comment.comment_id"
            class="comment-box"
          >
            <div v-if="!is_comment_blocked[comment.comment_id]">
              <h3 class="comment-header">
                {{ comment.title }}
                <el-rate
                  :model-value="getComputedValue(comment.avg_rate)"
                  disabled
                  show-score
                  text-color="#ff9900"
                  :max="5"
                  :score-template="getScoreTemplate(comment.avg_rate)"
                />
              </h3>
              <div class="comment-meta">创建于 {{ formatDatetime(comment.created) }}，作者：{{ comment.username }}</div>
              <div class="comment-body">{{ comment.body }}</div>

              <div class="comment-actions">
                <el-popconfirm
                  title="是否屏蔽"
                  @confirm="handleBlockConfirm(comment.comment_id)"
                >
                  <template #reference>
                    <el-icon>
                      <Hide />
                    </el-icon>
                  </template>
                </el-popconfirm>
                <el-popconfirm
                  title="是否举报"
                  @confirm="handleReportConfirm(comment.comment_id)"
                >
                  <template #reference>
                    <el-icon>
                      <Tickets />
                    </el-icon>
                  </template>
                </el-popconfirm>
              </div>
            </div>
          </div>

          <router-link
            :to="{ name: 'entry', params: { entryId: post.entry_id } }"
            class="readmore"
          >
            进入条目
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, h } from "vue";
import { useRoute } from "vue-router";
import { Hide, Tickets } from "@element-plus/icons-vue";
import {
  ElRadio,
  ElRadioGroup,
  ElMessageBox,
  ElInput,
  ElMessage,
} from "element-plus";
import axios from "axios";

export default {
  data() {
    return {
      title: "",
      body: "",
      reason: "",
      selectedTags: [],
    };
  },
  methods: {
    formatDatetime(datetime) {
      const date = new Date(datetime); // 创建一个 Date 对象，假设是 UTC 时间
      date.setHours(date.getHours());
      return date; // 格式化为本地日期时间字符串
    },
  },
  components: {
    Hide,
    Tickets,
  },
  setup() {
    const title = ref("");
    const body = ref("");
    const reason = ref("");
    const selectedTags = ref([]);
    const posts = ref([]);
    const comments = ref([]);
    const tags = ref([]);
    const cur_topic = ref([]);
    const route = useRoute();
    const topicId = route.params.topicId;

    const is_blocked = ref({});
    const is_comment_blocked = ref({});

    const isBlocked = async (entryId) => {
      const [response1, response2] = await Promise.all([
        axios.get("/profile", { withCredentials: true }),
        axios.get(`/api/get_block_list/${entryId}`, { withCredentials: true }),
      ]);
      const user = response1.data.user;
      const block_list = response2.data.block_list;
      console.log("user: ", user.id);
      console.log("block list: ", block_list);
      console.log(
        "isBlocked: ",
        block_list.some((block) => block.user_id === user.id)
      );
      return block_list.some((block) => block.user_id === user.id);
    };
    const isCommentBlocked = async (commentId) => {
      const [response1, response2] = await Promise.all([
        axios.get("/profile", { withCredentials: true }),
        axios.get(`/api/get_block_comments_list/${commentId}`, { withCredentials: true }),
      ]);
      const user = response1.data.user;
      const block_list = response2.data.block_list;
      console.log("user: ", user.id);
      console.log("block list: ", block_list);
      console.log(
        "isBlocked: ",
        block_list.some((block) => block.user_id === user.id)
      );
      return block_list.some((block) => block.user_id === user.id);
    };

    const fetchData = async () => {
      try {
        const response = await axios.get(`/t/${topicId}`, { withCredentials: true });
        posts.value = response.data.posts;
        comments.value = response.data.comments;
        const tag_response = await axios.get("/api/get_tags");
        tags.value = tag_response.data.tags;
        cur_topic.value = response.data.cur_topic;
        console.log("get tags: ", tag_response.data);

        // 使用 Promise.all 来异步处理所有 posts 的 blocked 状态
        const blockedStatuses = await Promise.all(
          posts.value.map(async (post) => {
            // 对每个 post.entry_id 调用 isBlocked，并将结果作为键值对保存在 is_blocked 中
            const blocked = await isBlocked(post.entry_id);
            return { [post.entry_id]: blocked };
          })
        );

        // 将 blockedStatuses 合并为一个对象，更新 is_blocked
        is_blocked.value = Object.assign({}, ...blockedStatuses);

        // 使用 Promise.all 来异步处理所有 posts 的 blocked 状态
        const blockedCommentStatuses = await Promise.all(
          comments.value.map(async (comment) => {
            // 对每个 post.entry_id 调用 isBlocked，并将结果作为键值对保存在 is_blocked 中
            const blocked = await isCommentBlocked(comment.comment_id);
            return { [comment.comment_id]: blocked };
          })
        );

        // 将 blockedStatuses 合并为一个对象，更新 is_blocked
        is_comment_blocked.value = Object.assign({}, ...blockedCommentStatuses);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    onMounted(async () => {
      await fetchData();
    });

    const submitApply = async () => {
      try {
        const response = await axios.get("/profile/", {
          withCredentials: true,
        });
        const user = response.data.user;

        if (!user) {
          ElMessage.error("用户信息未找到");
          return;
        }

        const user_id = user.id;

        if (!title.value.trim()) {
          ElMessage.error("标题不能为空");
          return;
        }
        if (!body.value.trim()) {
          ElMessage.error("内容不能为空");
          return;
        }

        const data = {
          title: title.value,
          body: body.value,
          tags: selectedTags.value,
          id: user_id,
        };
        const topicId = route.params.topicId;
        const postResponse = await axios.post(`/t/${topicId}`, data, { withCredentials: true });
        if (postResponse.data.success) {
          ElMessage.success("条目申请提交成功，请等待管理员审核");
          title.value = "";
          body.value = "";
          selectedTags.value = [];
        } else {
          ElMessage.error("条目申请提交失败");
        }
      } catch (error) {
        console.error(error);
        ElMessage.error("条目提交失败，请重试");
      }
    };

    const handleBlockConfirm = async (comment_id) => {
      try {
        const response = await axios.get("/profile/", {
          withCredentials: true,
        });
        const user = response.data.user;

        if (!user) {
          ElMessage.error("屏蔽失败，请先登录！");
          return;
        }

        const user_id = user.id;
        const blockResponse = await axios.post("block_comment", {
          user_id: user_id,
          comment_id: comment_id,
        }, { withCredentials: true });
        if (blockResponse.data.success) {
          ElMessage.success("评论已屏蔽");
          setTimeout(() => {
            window.location.reload();
          }, 500);
        } else {
          ElMessage.error("操作失败，请重试");
        }
      } catch (error) {
        console.error(error);
        ElMessage.error("请求失败，请重试");
      }
    };

    const handleReportConfirm = async (comment_id) => {
      try {
        const response = await axios.get("/profile/", {
          withCredentials: true,
        });
        const user = response.data.user;

        if (!user) {
          ElMessage.error("用户信息未找到");
          return;
        }

        const user_id = user.id;
        ElMessageBox.prompt("请输入举报理由：", "举报评论", {
          confirmButtonText: "提交举报",
          cancelButtonText: "取消",
          inputPattern: /.+/,
          inputErrorMessage: "举报理由不能为空",
        })
          .then(({ value }) => {
            reason.value = value;
            submitReport(comment_id, user_id);
          })
          .catch(() => {
            ElMessage({
              type: "info",
              message: "举报已取消",
            });
          });
      } catch (error) {
        console.error(error);
        ElMessage.error("请求失败，请重试");
      }
    };

    const submitReport = async (comment_id, user_id) => {
      try {
        const response = await axios.post("/report_comment", {
          user_id: user_id,
          comment_id: comment_id,
          reason: reason.value,
        }, { withCredentials: true });
        if (response.data.success) {
          ElMessage.success("举报成功");
        } else {
          ElMessage.error("举报失败，请稍后再试");
        }
      } catch (error) {
        console.error(error);
        ElMessage.error("请求失败，请稍后再试");
      }
    };

    const filteredComments = (entryId) => {
      return comments.value.filter((comment) => comment.entry_id === entryId);
    };

    const getComputedValue = (avgRate) => (avgRate / 2).toFixed(1);

    const getScoreTemplate = (avgRate) => `${avgRate.toFixed(1)} 分`;

    return {
      title,
      body,
      reason,
      selectedTags,
      posts,
      comments,
      cur_topic,
      tags,
      is_blocked,
      is_comment_blocked,
      submitApply,
      filteredComments,
      getComputedValue,
      getScoreTemplate,
      handleBlockConfirm,
      handleReportConfirm
    };
  },
};
</script>

<style scoped>
/* 基础布局 */
.common-layout {
  width: 90%;
  margin: 0 auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 8px;
}

.whitebg {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 标题样式 */
.htitle {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.entry-input {
  margin-bottom: 20px;
  padding: 10px;
  border-radius: 5px;
  background-color: #fafafa;
}

.submit-btn {
  width: 15%;
  padding: 10px;
  font-size: 16px;
  background-color: #409eff;
  color: white;
  border-radius: 5px;
}

.submit-btn:hover {
  background-color: #66b1ff;
}

/* 条目样式 */
.entries-list {
  margin-top: 40px;
}

.entry-card {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.entry-title {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
}

.entry-meta {
  font-size: 14px;
  color: #666;
  margin-top: 10px;
}

.comment-box {
  margin-top: 20px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.comment-header {
  font-size: 16px;
  font-weight: bold;
}

.comment-meta {
  font-size: 12px;
  color: #999;
  margin-bottom: 10px;
}

.comment-body {
  font-size: 14px;
  color: #333;
}

.comment-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}

/* 标签样式 */
.tag-container {
  margin-top: 15px;
  font-size: 14px;
}

.readmore {
  display: inline-block;
  margin-top: 15px;
  color: #409eff;
  font-weight: bold;
}

.readmore:hover {
  color: #66b1ff;
}
</style>
