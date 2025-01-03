<template>
    <div id="message">
        <Header></Header>
        <article id="article" class="article-container">
            <my_message v-if="user" />
            <please_login v-else />
            <rbox />            
        </article>
    </div>
</template>

<script>
import { ref, onMounted ,computed} from 'vue';
import axios from 'axios';
import Header from './head.vue'
import rbox from './home/rbox.vue';
import my_message from './about_me/my_message.vue';
import please_login from './about_me/please_login.vue';
export default {
    name: 'message',
    components: {
        Header,
        rbox,
        my_message,
        please_login
    },
    setup(){
      const user = ref(null);
      const fetchUserProfile = async() =>{
        try{
          const response = await axios.get('/profile',{withCredentials: true});
          console.log('User Profile:', response.data);
          user.value = response.data.user;
        }catch(error){
          console.error('Error fetching user profile:', error);
        }
      };
      onMounted(()=>{
        fetchUserProfile();
      });
      return {
        user
      }
    }
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


</style>