<template>
    <Header></Header>
    <div id="topic">
      <t_lbox/>
      <rbox/>
    </div>
</template>

<script >
import Header from './head.vue'
import rbox from './home/rbox.vue';
import t_lbox from './topic/topic_lbox.vue'

export default {
  name: 'topic',
  components: {
    Header,
    t_lbox,
    rbox,
  }
}

</script>

<style scoped>
#topic {
  display: flex;
  justify-content: space-between; /* 确保两个组件之间有间距 */
  width: 1200px; 
  margin: auto; 
  overflow: hidden 
}

#topic > * {
  margin: 10px; /* 可选：为组件之间添加一些间距 */
}



</style>
