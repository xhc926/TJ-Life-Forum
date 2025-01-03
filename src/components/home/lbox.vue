<script >
import Tab_box from './tab_box.vue';
import zhuanti from './zhuanti.vue';
import bloglist from './bloglist.vue';
import headline from './headline.vue';
import image2 from '../../images/2.jpg';



export default {
    name: 'rbox',
    components: {
        headline,
        Tab_box,
        zhuanti,
        bloglist,
    },
    data() {
        return {
            image2: image2,
        }
    }

}

</script>

<template>
    <div class="lbox">

        <headline/>
    
        <Tab_box/>
    
        <zhuanti/>
    
        <div class="ad whitebg"> <img :src=image2></div>
    
        <bloglist/>
        <!--bloglist end--> 
    </div>
    
</template>