<template>
  <Header></Header>
  <article id="article" class="article-container">
    <no_content v-if="is_blocked" />
    <id_lbox v-else />
    <rbox />
  </article>
</template>

<script>
import Header from './head.vue'
import rbox from './home/rbox.vue';
import { useRoute } from 'vue-router';
import { ref, onMounted, h } from 'vue';
import axios from 'axios';
import id_lbox from './item_detail/item_detail_lbox.vue'
import no_content from './item_detail/no_content.vue'

export default {
  name: 'item',
  components: {
    Header,
    rbox,
    id_lbox,
    no_content
  },
  setup() {
    const route = useRoute();
    const entryId = route.params.entryId;
    const is_blocked = ref();

    const isBlocked = async () => {
      const [response1, response2] = await Promise.all([
          axios.get('/profile', { withCredentials: true }),
          axios.get(`/api/get_block_list/${entryId}`)
        ]);
        const user = response1.data.user;
        const block_list = response2.data.block_list;
        console.log("user: ", user.id);
        console.log("block list: ", block_list); 
        console.log("isBlocked: ", block_list.some(block => block.user_id === user.id))
      return block_list.some(block => block.user_id === user.id);
    }
    onMounted(async () => {
      is_blocked.value = await isBlocked();
    });
    return {
      is_blocked
    }
  }
}

</script>

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
