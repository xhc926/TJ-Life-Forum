<template>
    <Header></Header>
    <div id="item">
      <i_lbox/>
      <rbox/>
    </div>
</template>

<script >
import Header from './head.vue'
import rbox from './home/rbox.vue';
import i_lbox from './item/item_lbox.vue'

export default {
  name: 'item',
  components: {
    Header,
    i_lbox,
    rbox,
  }
}

</script>

<style scoped>
#item {
  display: flex;
  justify-content: space-between; /* 确保两个组件之间有间距 */
  width: 1200px; 
  margin: auto; 
  overflow: hidden 
}

#item > * {
  margin: 10px; /* 可选：为组件之间添加一些间距 */
}



</style>
