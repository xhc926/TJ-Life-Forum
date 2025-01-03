<template>
    <div class="common-layout whitebg">
        <el-tabs type="border-card">
            <el-tab-pane :label="'全部消息(' + s_messages_cnt + ')'">
                <div class="message-box" v-for="s_message in s_messages" :key="s_message.message_id">
                    <h2>{{ s_message.title }} </h2>
                    <div class="timestamp">
                        时间： {{ s_message.created }}
                        &nbsp;&nbsp;&nbsp;
                        状态： {{ s_message.is_read === 1 ? '已读' : '未读' }}
                    </div>
                    <div class="timestamp"> 作者: Admin</div>
                    <p>{{ s_message.content }}</p>
                    <div class="button-container">
                        <button :disabled="s_message.is_read === 1" @click="setRead(s_message.message_id)">
                            设为已读
                        </button>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane :label="'已读消息(' + s_messages_read_cnt + ')'">
                <div class="message-box" v-for="s_message in s_messages_read" :key="s_message.message_id">
                    <h2>{{ s_message.title }} </h2>
                    <div class="timestamp">
                        时间： {{ s_message.created }}
                        &nbsp;&nbsp;&nbsp;
                        状态： {{ s_message.is_read === 1 ? '已读' : '未读' }}
                    </div>
                    <div class="timestamp"> 作者: Admin</div>
                    <p>{{ s_message.content }}</p>
                    <div class="button-container">
                        <button :disabled="s_message.is_read === 1" @click="setRead(s_message.message_id)">
                            设为已读
                        </button>
                    </div>
                </div>
            </el-tab-pane>
            <el-tab-pane :label="'未读消息(' + s_messages_nread_cnt + ')'">
                <div class="message-box" v-for="s_message in s_messages_nread" :key="s_message.message_id">
                    <h2>{{ s_message.title }} </h2>
                    <div class="timestamp">
                        时间： {{ s_message.created }}
                        &nbsp;&nbsp;&nbsp;
                        状态： {{ s_message.is_read === 1 ? '已读' : '未读' }}
                    </div>
                    <div class="timestamp"> 作者: Admin</div>
                    <p>{{ s_message.content }}</p>
                    <div class="button-container">
                        <button :disabled="s_message.is_read === 1" @click="setRead(s_message.message_id)">
                            设为已读
                        </button>
                    </div>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
    name: 'my_message',
    setup() {
        const user = ref([]);
        const s_messages = ref([]);
        const s_messages_read = ref([]);
        const s_messages_nread = ref([]);
        const s_messages_read_cnt = ref(null);
        const s_messages_cnt = ref(null);
        const s_messages_nread_cnt = ref(null);

        const get_s_message = async () => {
            try {
                const user_res = await axios.get('/profile', { withCredentials: true });
                user.value = user_res.data.user;
                const response = await axios.get(`/profile/get_s_messages${user.value.id}`);
                s_messages.value = response.data.s_messages;
                s_messages_cnt.value = response.data.read_count;
            } catch (error) {
                console.error('Error fetching s_message: ', error);
            }
        };

        const get_s_message_read = async () => {
            try {
                const user_res = await axios.get('/profile', { withCredentials: true });
                user.value = user_res.data.user;
                const response = await axios.get(`/profile/get_s_messages${user.value.id}_read`);
                s_messages_read.value = response.data.s_messages;
                s_messages_read_cnt.value = response.data.read_count;
            } catch (error) {
                console.error('Error fetching s_message: ', error);
            }
        };

        const get_s_message_nread = async () => {
            try {
                const user_res = await axios.get('/profile', { withCredentials: true });
                user.value = user_res.data.user;
                const response = await axios.get(`/profile/get_s_messages${user.value.id}_not_read`);
                s_messages_nread.value = response.data.s_messages;
                s_messages_nread_cnt.value = response.data.read_count;
            } catch (error) {
                console.error('Error fetching s_message: ', error);
            }
        };

        onMounted(() => {
            get_s_message();
            get_s_message_read();
            get_s_message_nread();
        });

        const setRead = async (messageId) => {
            try {
                const response = await axios.post(`/profile/set_read_${messageId}`, {}, { withCredentials: true });
                window.location.reload();
            } catch (error) {
                console.error('设置已读状态失败:', error);
            }
        };

        return {
            s_messages,
            s_messages_cnt,
            s_messages_read,
            s_messages_read_cnt,
            s_messages_nread,
            s_messages_nread_cnt,
            setRead
        };
    }
};
</script>

<style scoped>
.common-layout {
    margin: 0 auto;
    width: 80%;
    padding: 20px;
    background-color: #f4f7fc;
}

.whitebg {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
}

.el-tabs {
    margin-top: 20px;
}

.message-box {
    background-color: #fff;
    border-radius: 10px;
    border: 1px solid #ddd;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}

.message-box h2 {
    color: #333;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

.timestamp {
    font-size: 14px;
    color: #777;
    margin-bottom: 5px;
}

.timestamp strong {
    font-weight: bold;
}

p {
    font-size: 16px;
    line-height: 1.6;
    color: #555;
    margin-bottom: 20px;
}

.button-container {
    align-self: flex-end;
}

button {
    padding: 8px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 30px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}

button:hover:not(:disabled) {
    background-color: #0056b3;
    transform: translateY(-2px);
}

button:active:not(:disabled) {
    transform: translateY(2px);
}

.el-tab-pane {
    padding: 20px;
}

.el-tabs__header {
    margin-bottom: 20px;
}

.el-tabs__item {
    font-weight: bold;
}

.el-tabs__nav-wrap {
    border-bottom: 2px solid #f4f7fc;
}
</style>
