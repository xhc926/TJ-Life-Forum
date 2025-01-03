<template>
  <div
    style="padding: 30px; max-width: 800px; margin: 0 auto; background-color: #f9f9f9; border-radius: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
    <!-- 标题和说明 -->
    <h2 style="text-align: center; color: #333;">个人资料更新</h2>
    <p style="text-align: center; color: #777;">在这里，您可以更新头像、用户名、邮箱、密码及更多个人信息。</p>

    <!-- 用户头像上传 -->
    <el-divider content-position="left" style="margin-top: 30px;">上传头像</el-divider>
    <form @submit.prevent="uploadAvatar">
      <el-upload
        class="avatar-uploader"
        action="/profile/upload_avatar"
        :show-file-list="false"
        :on-success="handleUploadSuccess"
        :before-upload="beforeAvatarUpload"
        :http-request="customRequest"
        :headers="{ 'Content-Type': 'multipart/form-data' }"
        with-credentials
      >
        <el-button size="small" type="primary">上传头像</el-button>
      </el-upload>
    </form>

    <!-- 用户名更新 -->
    <el-divider content-position="left">更新用户名</el-divider>
    <form @submit.prevent="updateUsername">
      <el-input v-model="newUsername" placeholder="请输入新用户名" clearable class="input-field" />
      <el-button type="primary" size="small" @click="updateUsername" class="custom-btn">更新用户名</el-button>
    </form>

    <!-- 邮箱更新 -->
    <el-divider content-position="left">更新邮箱</el-divider>
    <form @submit.prevent="updateEmail">
      <el-input v-model="newEmail" placeholder="请输入新邮箱" clearable class="input-field" />
      <el-button type="primary" size="small" @click="updateEmail" class="custom-btn">更新邮箱</el-button>
    </form>

    <!-- 邮箱验证 -->
    <el-divider content-position="left">邮箱验证</el-divider>
    <div>
      <h4>请输入验证信息</h4>
      <el-input v-model="oldVerificationCode" placeholder="请输入旧邮箱验证码" clearable class="input-field" />
      <el-input v-model="newVerificationCode" placeholder="请输入新邮箱验证码" clearable class="input-field" />
      <el-button type="primary" size="small" @click="verifyEmailCodes" class="custom-btn">验证邮箱</el-button>
    </div>

    <!-- 标签选择 -->
    <el-divider content-position="left">更新标签</el-divider>
    <form @submit.prevent="updateTags">
      <label for="tags">选择标签：</label>
      <el-row gutter="20" class="tag-row">
        <el-col :span="6" v-for="tag in tags" :key="tag.id">
          <el-checkbox :label="tag.id" v-model="selectedTags" :id="`tag-${tag.id}`">{{ tag.name }}</el-checkbox>
        </el-col>
      </el-row>
      <el-button type="primary" size="small" @click="updateTags" class="custom-btn">更新标签</el-button>
    </form>

    <!-- 修改密码 -->
    <el-divider content-position="left">修改密码</el-divider>
    <form @submit.prevent="requestVerificationCode">
      <el-input v-model="newPassword" type="password" placeholder="请输入新密码" clearable class="input-field" />
      <el-input v-model="confirmPassword" type="password" placeholder="确认新密码" clearable class="input-field" />
      <el-button type="primary" size="small" @click="requestVerificationCode" class="custom-btn">发送验证码</el-button>
    </form>

    <!-- 验证码输入 -->
    <div v-if="showVerificationFields">
      <el-divider content-position="left">验证码验证</el-divider>
      <h4>请输入验证码以完成密码更新</h4>
      <el-input v-model="verificationCode_for_psw" placeholder="请输入验证码" clearable class="input-field" />
      <el-button type="primary" @click="verifyAndUpdatePassword" class="custom-btn">验证并更新密码</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newUsername: '',
      newEmail: '',
      oldVerificationCode: '', // 旧邮箱验证码
      newVerificationCode: '', // 新邮箱验证码
      verificationCode_for_psw: '',  // 用于存储验证码
      selectedTags: [],
      newPassword: '',
      confirmPassword: '',
      tags: [],  // 你可以通过 API 获取标签列表
      showVerificationFields: false, // 是否显示验证输入框
    };
  },
  methods: {
    // 请求验证码
    async requestVerificationCode() {
      if (this.newPassword !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }

      try {
        const response = await axios.post('/profile/request_verification_code', {}, { withCredentials: true });

        if (response.data.message) {
          alert(response.data.message);
          this.showVerificationFields = true; // 显示验证码输入框
        }
      } catch (error) {
        alert(error.response.data.error || '发送验证码失败');
      }
    },

    // 验证验证码并更新密码
    async verifyAndUpdatePassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }

      try {
        const response = await axios.post('/profile/update_password', {
          new_password: this.newPassword,
          verification_code_for_psw: this.verificationCode_for_psw, // 使用新的验证码字段
        }, { withCredentials: true });

        alert(response.data.message);
        this.showVerificationFields = false; // 隐藏验证码输入框
      } catch (error) {
        alert(error.response.data.error || '密码更新失败');
      }
    },
    // 上传头像
    beforeAvatarUpload(file) {
      console.log('before upload:', file);
      if (!file) {
        alert('请先选择文件');
      }
      return true;  // 继续上传
    },
    handleUploadSuccess(response) {
      console.log('文件上传成功:', response);
      alert('头像更新成功');
    },
    customRequest({ file, onSuccess, onError }) {
      const formData = new FormData();
      formData.append('avatar', file);
      
      axios.post('/profile/upload_avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        withCredentials: true
      })
        .then(response => {
          onSuccess(response.data);  // 上传成功
        })
        .catch(error => {
          onError(error);  // 上传失败
        });
    },
    async uploadAvatar() {
      const formData = new FormData();
      const avatarFile = this.$refs.avatar.files[0];
      console.log(avatarFile);  // 打印文件信息
      formData.append('avatar', avatarFile);

      try {
        const response = await axios.post('/profile/upload_avatar', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          withCredentials: true
        });
        alert(response.data.message);
      } catch (error) {
        alert(error.response.data.error || 'Failed to upload avatar');
      }
    },

    // 更新用户名
    async updateUsername() {
      try {
        const response = await axios.post('/profile/update_username', { new_username: this.newUsername },
          { withCredentials: true });
        alert(response.data.message);
      } catch (error) {
        alert(error.response.data.error || 'Failed to update username');
      }
    },

    // 修改邮箱方法
    async updateEmail() {
      try {
        const response = await axios.post('/profile/update_email', { new_email: this.newEmail },
          { withCredentials: true });

        // 如果后台成功返回了信息，表示邮箱验证步骤已经触发
        alert(response.data.message);
        this.showVerificationFields = true; // 显示验证码输入框
      } catch (error) {
        alert(error.response.data.error || 'Failed to update email');
      }
    },

    // 验证邮箱验证码
    async verifyEmailCodes() {
      try {
        const response = await axios.post('/profile/verify_email_codes', {
          old_verification_code: this.oldVerificationCode,
          new_verification_code: this.newVerificationCode
        }, { withCredentials: true });

        alert(response.data.message);
        this.showVerificationFields = false; // 隐藏验证码输入框
      } catch (error) {
        alert(error.response.data.error || 'Failed to verify email');
      }
    },

    // 更新标签
    async updateTags() {
      console.log('Updating tags:', this.selectedTags);  // 调试输出
      try {
        const response = await axios.post('/profile/update_tags', { selected_tags: this.selectedTags },
          { withCredentials: true });
        alert(response.data.message);
      } catch (error) {
        alert(error.response.data.error || 'Failed to update tags');
      }
    },

    // 获取标签列表
    async fetchTags() {
      try {
        const response = await axios.get('/profile/get_tags', { withCredentials: true });
        this.tags = response.data.tags;  // 假设后端返回的标签数据是 { tags: [...] }
      } catch (error) {
        console.error('Failed to fetch tags:', error);
      }
    }
  },
  created() {
    // 获取标签列表
    this.fetchTags();
  }
}
</script>
<style scoped>
/* 通用样式 */
.custom-btn {
  width: 20%;
  margin-top: 10px;
  background: linear-gradient(135deg, #6e7bff, #4c6ef5);
  border-radius: 30px;
  font-weight: bold;
  font-size: 14px;
  transition: all 0.3s ease;
}

.custom-btn:hover {
  background: linear-gradient(135deg, #4c6ef5, #6e7bff);
  transform: translateY(-3px);
}

.custom-btn:active {
  transform: translateY(2px);
}

.input-field {
  width: 100%;
  margin-bottom: 20px;
}

.tag-row {
  margin-bottom: 20px;
}

.el-divider {
  font-weight: bold;
  margin-top: 30px;
  margin-bottom: 20px;
}

.el-checkbox {
  margin-bottom: 10px;
}

h2 {
  color: #333;
  font-size: 24px;
}

h4 {
  color: #444;
  font-size: 18px;
}

form {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
}

.avatar-uploader {
  margin-bottom: 20px;
}

.el-input {
  margin-bottom: 20px;
}

.el-col {
  margin-bottom: 10px;
}

.el-row {
  margin-bottom: 20px;
}

/* 全局样式 */
body {
  background-color: #f4f7fc;
}
</style>