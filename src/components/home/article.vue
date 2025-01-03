<template>
<article id="article" class="article-container"> 

  <!--正文部分，偏左-->
    <lbox/>
  <!--边框栏，偏右-->
    <rbox/>

</article>

</template>


<script >
import rbox from './rbox.vue';
import lbox from './lbox.vue';


export default {
    name: 'Article',
    components: {
        lbox,
        rbox
    },
}

</script>

<style scoped>
.article-container {
  display: flex;
  justify-content: space-between; /* 确保两个组件之间有间距 */
  
}

.article-container > * {
  margin: 10px; /* 可选：为组件之间添加一些间距 */
}
/*此处的rbox lbox的style请删除*/
</style>