<template>
    <Header/>    
    <div id="forum">
      <af_lbox/>
      <rbox/>
    </div>
</template>

<script >
import Header from './head.vue'
import rbox from './home/rbox.vue'
import af_lbox from './forum/forum_lbox_sum.vue'

export default {
  name: 'forum',
  components: {
    Header,
    af_lbox,
    rbox,
  }
}

</script>

<style scoped>
#forum {
  display: flex;
  justify-content: space-between; /* 确保两个组件之间有间距 */
  width: 1200px; 
  margin: auto; 
  overflow: hidden 
}

#forum > * {
  margin: 10px; /* 可选：为组件之间添加一些间距 */
}



</style>
