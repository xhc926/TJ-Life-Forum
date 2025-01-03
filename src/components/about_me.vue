<script>
import ab_box from './about_me/ab_box.vue'
import myblog from './about_me/myblog.vue'
import Header from './head.vue'
import rbox from './home/rbox.vue'
export default {
  name: 'about_me',
  components: {
    Header,
    ab_box,
    rbox,
  }
}

</script>

<template>
  <div id="about_me">
    <Header></Header>
    <article id="article" class="article-container">
      <ab_box />      
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
