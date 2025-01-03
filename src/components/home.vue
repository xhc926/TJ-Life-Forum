<template>
    <div id="home">
      <Header></Header>
      <Article></Article>
    </div>
</template>

<script >
import Header from './head.vue'
import Article from './home/article.vue';     
export default {
  name: 'home',
  components: {
    Header,
    Article,
  }
}

</script>

<!--主页-->
