import { createRouter, createWebHistory } from 'vue-router';
import routes from './router';

const router = createRouter({
  history: createWebHistory(''),
  routes: [
    {
      path : '/',
      redirect : '/home'
    },
    {
      path:'/home',
      meta:{
        title:'论坛主页'
      },
      component: async () => {
        try {
            return await import('../components/home.vue');
        } catch (error) {
            console.error('Error loading component:', error);
            return import('../components/home.vue'); // 加载一个备用组件
        }
      }
    },
    {
      path:'/about_me',
      meta:{
        title:'个人主页'
      },
      component:()=>import('../components/about_me.vue')
    },
    {
      path:'/login',
      name:'login',
      meta:{
        title:'登录注册'
      },
      component:()=>import('../components/login.vue')
    },
    {
      path:'/forum',
      name:'all_forum',
      meta:{
        title:'论坛'
      },
      component:()=>import('../components/forum_sum.vue')
    },
    {
      path:'/forum/:forumId',
      name:'forum',
      component:()=>import('../components/forum.vue')
    },
    {
      path:'/topic/:topicId',
      name:'topic',
      component:()=>import('../components/topic.vue')
    },
    {
      path:'/entry/:entryId',
      name:'entry',
      meta:{
        title:'帖子详情'
      },
      component:()=>import('../components/item_detail.vue')
    },
    {
      path:'/hottest_posts',
      name:'hottest_posts',
      component:()=>import('../components/hottest.vue')
    },
    {
      path:'/message',
      name:'message',
      meta:{
        title:'消息中心'
      },
      component:()=>import('../components/message.vue')
    }
  ]
});


export default router;