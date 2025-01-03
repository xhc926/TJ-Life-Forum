<template>
    <div class="zhuanti whitebg">
        <h2 class="htitle">
            <span class="hnav">
                <a href="/">最新</a>
                <a href="/">最热门</a>
                <a href="/">周边</a>
                <a href="/">校内</a>
            </span>精彩话题
        </h2>
        <ul>
            <li v-for="topic in topics" :key="topic.topic_id">
                <i class="ztpic"><a href="/" target="_blank"><img :src=image1></a></i>
                <b>{{ topic.topic_name }}</b>
                <span>浏览人数：{{ topic.total_views }}人</span>
                <span>{{ topic.description }}</span>
                <a :href="`/topic/${topic.topic_id}`" target="_blank" class="readmore">进入话题</a>
            </li>

        </ul>
    </div>
</template>

<script>
import image1 from '../../images/1.jpg';
import axios from 'axios';
import { onMounted, ref } from 'vue'

export default {
    name: 'Zhuanti',
    setup() {
        const topics = ref();
        const fetchData = async () => {
            try {
                const response = await axios.get('/api/get_recommended_topics', { withCredentials: true });
                console.log('get_recommended_topics data', response.data);
                topics.value = response.data.topics;
            } catch (error) {
                console.error('get_recommended_topics error: ', error);
            }
        };
        onMounted(() => {
            fetchData();
        })
        return {
            image1,
            topics
        }
    }

}
</script>
