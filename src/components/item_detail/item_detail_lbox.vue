<template>
  <div class="common-layout whitebg">
    <h1 class="post-title">{{ cur_post.title }}</h1>

    <!-- 帖子信息 -->
    <div class="title_detail">
      <h4 class="detail1">
        <span>更新时间：<span>{{ formatDatetime(cur_post.updated) }}&nbsp;&nbsp;&nbsp;</span></span>
        <span>评论次数：<span>{{ cur_post.commented }}&nbsp;&nbsp;&nbsp;</span></span>
        <span>浏览次数：<span>{{ cur_post.views }}</span></span>
      </h4>
      <!-- 帖子标签 -->
      <p><small>标签：</small>
        <span>
          <el-tag
            v-for="tag in entry_tags"
            :key="tag.id"
            type="primary"
          >{{ tag.name }}</el-tag>
        </span>
      </p>

      <!-- 帖子评分 -->
      <div class="post-rating">
        <span>平均评分：</span>
        <el-rate
          :model-value="getComputedValue(cur_post.avg_rate)"
          disabled
          show-score
          text-color="#ff9900"
          :max="5"
          :score-template="getScoreTemplate(cur_post.avg_rate)"
        />
      </div>

      <div class="popconfirm-container">
        <el-popconfirm
          title="是否屏蔽"
          @confirm="handleBlockEntryConfirm(cur_post.entry_id)"
        >
          <template #reference>
            <el-icon>
              <Hide />
            </el-icon>
          </template>
        </el-popconfirm>
        <el-popconfirm
          title="是否举报"
          @confirm="handleReportEntryConfirm(cur_post.entry_id)"
        >
          <template #reference>
            <el-icon>
              <Tickets />
            </el-icon>
          </template>
        </el-popconfirm>
      </div>
    </div>

    <div class="item_content">
      <h3>具体描述:</h3>
      <p>{{ cur_post.description }}</p>
    </div>
    <br>

    <!-- 评论部分 -->
    <div class="item_comment">
      <h3>评论</h3>
      <div class="comment-list">
        <div
          v-for="comment in comments"
          :key="comment.comment_id"
          class="comment-box"
        >
          <div v-if="!is_comment_blocked[comment.comment_id]">
            <h3 class="comment-header">
              {{ comment.title }}
              <el-rate
                :model-value="getComputedValue(comment.rate)"
                disabled
                show-score
                text-color="#ff9900"
                :max="5"
                :score-template="getScoreTemplate(comment.rate)"
              />
            </h3>
            <div class="comment-meta">
              于 {{ formatDatetime(comment.created) }} 创建, 作者：{{ comment.username }}
            </div>
            <div class="comment-body">
              <span>{{ comment.body }}</span>
            </div>

            <div class="popconfirm-container">
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
      </div>
      <br>
      <br>

      <!-- 评论输入区域 -->
      <h3>发表我的评论</h3>
      <br>

      <div class="comment-form">
        <el-input
          v-model="title"
          class="input-field"
          placeholder="请输入标题"
          show-word-limit
          type="text"
        />
        <el-input
          v-model="body"
          class="input-field"
          placeholder="请输入内容"
          show-word-limit
          type="text"
        />

        <div class="rating-section">
          <span>我的评分：</span>
          <el-rate v-model="rating" />
          <el-button
            type="primary"
            class="submit-btn"
            @click="submitComment"
          >评论</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, h } from "vue";
import { useRoute } from "vue-router";
import { ElMessage, ElMessageBox, ElInput } from "element-plus";
import axios from "axios";
import { Hide, Tickets } from "@element-plus/icons-vue";

export default {
  components: {
    Hide,
    Tickets,
  },
  methods: {
    formatDatetime(datetime) {
      const date = new Date(datetime); // 创建一个 Date 对象，假设是 UTC 时间
      date.setHours(date.getHours());
      return date; // 格式化为本地日期时间字符串
    },
  },
  setup() {
    const title = ref("");
    const body = ref("");
    const rating = ref(0);
    const reason = ref("");
    const comments = ref([]);
    const cur_post = ref([]);
    const entry_tags = ref([]);
    const route = useRoute();
    const entryId = route.params.entryId;
    const is_comment_blocked = ref({});
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
        console.log("entry page: fetchdata called");
        const response = await axios.get(`/e/${entryId}`, {
          withCredentials: true,
        });
        comments.value = response.data.comments;
        cur_post.value = response.data.post;
        entry_tags.value = response.data.entry_tags;
        console.log("response: ", response.data);

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

    const submitComment = async () => {
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
        if (rating.value === 0) {
          ElMessage.error("评分不能为空");
          return;
        }

        // 提交评论
        const data = {
          title: title.value,
          body: body.value,
          rating: rating.value * 2,
          id: user_id,
        };
        const entryId = route.params.entryId;
          const postResponse = await axios.post(`/e/${entryId}`, data, { withCredentials: true });
        if (postResponse.data.success) {
          ElMessage.success("评论提交成功");
          title.value = "";
          body.value = "";
          rating.value = 0;
          window.location.reload();
        } else {
          ElMessage.error("评论提交失败");
        }
      } catch (error) {
        console.error(error);
        ElMessage.error("评论提交失败，请重试");
      }
    };

    const handleBlockConfirm = async (comment_id) => {
      try {
        const response = await axios.get("http://113.44.59.183:5000/profile/", {
          withCredentials: true,
        });
        const user = response.data.user;

        if (!user) {
          ElMessage.error("屏蔽失败，请先登录！");
          return;
        }

        const user_id = user.id;
          const blockResponse = await axios.post("http://113.44.59.183:5000/block_comment", {
              user_id: user_id,
              comment_id: comment_id,
          }, { withCredentials: true });
        if (blockResponse.data.success) {
          ElMessage.success("评论已屏蔽");
          window.location.reload();
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
        const response = await axios.get("http://113.44.59.183:5000/profile/", {
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
          const response = await axios.post("http://113.44.59.183:5000/report_comment", {
              user_id,
              comment_id,
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
    const handleBlockEntryConfirm = async (entry_id) => {
      try {
        const response = await axios.get("http://113.44.59.183:5000/profile/", {
          withCredentials: true,
        });
        const user = response.data.user;

        if (!user) {
          ElMessage.error("屏蔽失败，请先登录！");
          return;
        }

        const user_id = user.id;
          const blockResponse = await axios.post("http://113.44.59.183:5000/block_entry", {
              user_id: user_id,
              entry_id: entry_id,
          }, { withCredentials: true });
        if (blockResponse.data.success) {
          ElMessage.success("条目已屏蔽");
          window.location.reload();
        } else {
          ElMessage.error("操作失败，请重试");
        }
      } catch (error) {
        console.error(error);
        ElMessage.error("请求失败，请重试");
      }
    };

    const handleReportEntryConfirm = async (entry_id) => {
      try {
        const response = await axios.get("http://113.44.59.183:5000/profile/", {
          withCredentials: true,
        });
        const user = response.data.user;

        if (!user) {
          ElMessage.error("用户信息未找到");
          return;
        }

        const user_id = user.id;
        ElMessageBox.prompt("请输入举报理由：", "举报条目", {
          confirmButtonText: "提交举报",
          cancelButtonText: "取消",
          inputPattern: /.+/,
          inputErrorMessage: "举报理由不能为空",
        })
          .then(({ value }) => {
            reason.value = value;
            submitEntryReport(entry_id, user_id);
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

    const submitEntryReport = async (entry_id, user_id) => {
      try {
          const response = await axios.post("http://113.44.59.183:5000/report_entry", {
              user_id,
              entry_id,
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

    const filteredComments = (entryId) =>
      comments.value.filter((comment) => comment.entry_id === entryId);

    const getComputedValue = (avgRate) => avgRate / 2;
    const getScoreTemplate = (rate) =>
      rate < 2 ? "差" : rate < 4 ? "中" : "好";

    return {
      title,
      body,
      rating,
      reason,
      comments,
      cur_post,
      entry_tags,
      is_comment_blocked,
      submitComment,
      handleBlockConfirm,
      handleReportConfirm,
      submitReport,
      handleBlockEntryConfirm,
      handleReportEntryConfirm,
      submitEntryReport,
      filteredComments,
      getComputedValue,
      getScoreTemplate,
    };
  },
};
</script>

<style scoped>
/* 这里可以添加CSS样式来美化页面 */
/* 基础布局 */
.common-layout {
  width: 90%;
  margin: 20 auto;
  padding: 40px;
  background-color: #f7f7f7;
  border-radius: 8px;
}

.whitebg {
  background: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.comment-list {
  padding: 15px;
  border-top: 1px solid #f0f0f0;
  margin-top: 20px;
  background-color: #fafafa;
}

.comment-box {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #e6e6e6;
  border-radius: 10px;
  background-color: #ffffff;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-meta {
  font-size: 14px;
  color: #999999;
  margin-top: 10px;
}

.comment-body {
  margin-top: 10px;
}

.rating-section {
  margin-top: 20px;
  display: flex;
  /* 启用 Flexbox 布局 */
  justify-content: space-between;
  /* 确保评分和按钮之间有间隔，并且按钮在最右侧 */
  align-items: center;
  /* 垂直居中对齐评分和按钮 */
}

.submit-btn {
  margin-top: 15px;
  width: 10%;
  margin-left: auto;
}

.input-field {
  margin-bottom: 15px;
}

.post-rating {
  margin-top: 10px;
}
</style>