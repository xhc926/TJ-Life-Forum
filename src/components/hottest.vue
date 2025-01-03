<script>
import ab_box from './about_me/ab_box.vue'
import Header from './head.vue'
import rbox from './home/rbox.vue'
import hottest_posts from './home/hottest_posts.vue'
export default {
  name: 'hottest',
  components: {
    Header,
    rbox,
    hottest_posts,
  }
}

</script>
<template>
  <div id="hottest">
    <Header></Header>
    <article id="article" class="article-container">
      <hottest_posts />      
      <rbox />
    </article>
  </div>
</template>


<style scoped>
.article-container {
  display: flex;
  justify-content: space-between;
  /* 确保两个组件之间有间距 */

}

.article-container>* {
  margin: 10px;
  /* 可选：为组件之间添加一些间距 */
}
</style>