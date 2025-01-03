<template>
    <div class="rbox">
        <div class="card">
            <!-- 登录状态显示 -->
            <div class="login-status" :class="{ 'logged-in': user, 'not-logged-in': !user }">
                {{ user ? '已登录' : '未登录' }}
            </div>
            <h2>我的信息</h2>
            <p v-if="user">用户名：{{ user.username }}</p>
            <p v-else>用户名：未知</p>
            <p v-if="userTags.length">兴趣：
                <span v-for="(tag, index) in userTags" :key="index">
                    {{ tag.name }}<span v-if="index < userTags.length - 1">、</span>
                </span>
            </p>
            <p v-else>兴趣：暂无</p>
            <p v-if="user && user.email">Email: {{ user.email }}</p>
            <p v-else>Email: 未知</p>
            <p v-if="user && user.introduction">简介: {{ user.introduction }}</p>
            <p v-else>简介: 未知</p>
            <ul class="linkmore">
                <li><a href="/home" target="_blank" class="iconfont icon-zhuye" title="网站地址"></a></li>
                <li><a href="http://mail.tongji.edu.cn" target="_blank" class="iconfont icon-youxiang" title="我的邮箱"></a>
                </li>
                <li><a href="http://wpa.qq.com/msgrd?v=3&uin=476847113&site=qq&menu=yes" target="_blank"
                        class="iconfont icon---" title="QQ"></a></li>
                <li id="weixin"><a href="https://web.wechat.com/m/?lang=zh_CN" target="_blank"
                        class="iconfont icon-weixin" title="微信"></a><i><img :src=image1></i></li>
            </ul>
        </div>
        <div class="whitebg notice">
            <h2 class="htitle">论坛公告</h2>
            <ul>
                <li><a href="/">请尊重他人，禁止任何形式的辱骂和人身攻击。</a></li>
                <li><a href="/">禁止发布任何形式的广告和垃圾信息。</a></li>
                <li><a href="/">请勿发布任何违反法律法规的内容。</a></li>
                <li><a href="/">遇到技术问题？请访问我们的技术支持版块。</a></li>
            </ul>
        </div>
        <div class="whitebg paihang">
        <h2 class="htitle">热帖排行</h2>
        <section class="topnews imgscale"><a href="/"><img :src=image1><span>憧憬成为图书馆卷王</span></a></section>
        <ul>
            <li v-for="post in posts3.slice(0, 5)" :key="post.forum_id"><i></i>
                <router-link :to="`/entry/${post.entry_id}`" @click.prevent="navigatetoentry(post.entry_id)" >
                   <h4 >{{post.title}}</h4> 
                </router-link>                
                
            </li>

        </ul>
        </div>
        <div class="whitebg tuijian">
        <h2 class="htitle">论坛推荐</h2>
        <ul>
            <li v-for="forum in forums" :key="forum.forum_id" >
                <router-link :to="`/forum/${forum.forum_id}`" @click.prevent="navigateToForum(forum.forum_id)" >
                    <i><img :src=image1></i>
                    <p>{{ forum.forum_name }}</p>
                </router-link>
            </li>
        </ul>
        </div>
        <div class="ad whitebg imgscale">
            <ul>
                <a href="/"><img :src=image1></a>
            </ul>
        </div>
        <div class="whitebg wenzi">
            <h2 class="htitle">猜你喜欢</h2>
            <ul>
                <li v-for="post in posts2.slice(0, 5)" :key="post.forum_id"><i></i>
                    <a href="/entry/${post.entry_id}" @click.prevent="navigateToEntry(post.entry_id)">
                        <h4>{{ post.title }}</h4>
                    </a>
                </li>
            </ul>
        </div>
        <div class="ad whitebg imgscale">
            <ul>
                <li>
                    <a href="/"><img :src=image1></a>
                </li>
            </ul>
        </div>
        <div class="whitebg tongji">
            <h2 class="htitle">论坛信息</h2>
            <ul>
                <li><b>建站时间</b>：2024-12-13</li>
                <li><b>论坛小程序</b>：敬请期待...</li>
                <li><b>用户统计：</b>{{ user_counts }}</li>
                <li><b>帖子统计：</b>{{ entry_counts }}</li>
                <li><b>评论统计：</b>{{ comment_counts }}</li>
                <li><b>访问次数：</b>{{ view_counts }}</li>
                <li><b>微信公众号</b>：敬请期待...</li>
                <img :src=image1 class="tongji_gzh">
            </ul>
        </div>
        <div class="links whitebg">
            <h2 class="htitle"><span class="sqlink"></span>技术相关链接</h2>
            <ul>
                <li><a href="https://gitlab.com/tj-cs-swe/cs10102302-2024-fall/G7/forum-0.0" target="_blank">技术</a></li>
            </ul>
        </div>
    </div>

</template>

<script>
import image1 from '../../images/1.jpg';
import { ref, onMounted ,computed, watch} from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
export default {
    name: 'Rbox',
    methods: {
        navigateToEntry(entryId) {
            this.$router.push({ name: 'entry', params: { entryId: entryId } });
            window.location.href = `/entry/${entryId}`;
            console.log("navigate to entry: ", entryId);
        }
    },
    setup() {
        const user = ref(null);
        const userTags = ref([]);
        const email = ref(null);
        //1=most_viewed, 2=most_recommended, 3=hottest
        const posts1 = ref([]);
        const posts2 = ref([]);
        const posts3 = ref([]);
        const comments1 = ref([]);
        const comments2 = ref([]);
        const comments3 = ref([]);
        const entryTags1 = ref([]);
        const entryTags2 = ref([]);
        const entryTags3 = ref([]);
        const user_counts = ref(null);
        const entry_counts = ref(null);
        const comment_counts = ref(null);
        const view_counts = ref(null);
        //const history = ref([]);
        //const uMessage = ref([]);
        //const sMessage = ref([]);    // 发送请求获取用户资料
        const fetchUserProfile = async () => {
            try {
                const response = await axios.get('/profile/', { withCredentials: true });
                console.log('User Profile:', response.data); // 打印后端返回的所有数据
                user.value = response.data.user;
                userTags.value = response.data.user_tags;
                email.value = response.data.user.email;
                //history.value = data.history;
                //uMessage.value = data.u_message;
                //sMessage.value = data.s_message;
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        };
        const fetchData = async () => {
            try {
                const [response1, response2, response3] = await Promise.all([
                    axios.get('/api/get_most_viewed_posts', { withCredentials: true }), // 替换为你的第一个后端 API 路径
                    axios.get('/api/get_recommend_posts', { withCredentials: true }), // 推荐算法接口
                    axios.get('/api/get_hottest_posts', { withCredentials: true })
                ])
                posts1.value = response1.data.posts;
                comments1.value = response1.data.comments;
                entryTags1.value = response1.data.entry_tags;
                posts2.value = response2.data.posts;
                comments2.value = response2.data.comments;
                entryTags2.value = response2.data.entry_tags;
                posts3.value = response3.data.posts;
                comments3.value = response3.data.comments;
                entryTags3.value = response3.data.entry_tags;
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        const fetchStatistics = async () => {
            try {
                const response = await axios.get('/statistics', { withCredentials: true });
                user_counts.value = response.data.user_counts;
                entry_counts.value = response.data.entry_counts;
                comment_counts.value = response.data.comment_counts;
                view_counts.value = response.data.total_views;
            } catch (error) {
                console.error('Error fetching statistics:', error);
            }
        }
        const filteredComments = (entryId) => {
            return comments.value.filter(comment => comment.entry_id === entryId);
        };
        onMounted(() => {
            fetchUserProfile();
            fetchData();
            fetchStatistics();
        });
        return {
            user,
            userTags,
            posts1,
            comments1,
            entryTags1,
            posts2,
            comments2,
            entryTags2,
            posts3,
            comments3,
            entryTags3,
            user_counts,
            entry_counts,
            comment_counts,
            view_counts,
            //history,
            //uMessage,
            //sMessage,
            image1
        }
    }
}
</script>
