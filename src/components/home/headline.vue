<template>
    <div class="toutiao">
        <div class="banbox">
            <div class="block">
                <el-carousel trigger="click">
                    <el-carousel-item v-for="(image, index) in slides" :key="index">
                        <img :src="image.src" :alt="image.alt" class="carousel-image">
                    </el-carousel-item>
                </el-carousel>
            </div>
        </div>
        <!--banbox end-->

        <!--headline begin-->
        <div class="headline">
            <ul>
                <li><a href="/" title="今日宜考试，睡觉">
                        <img :src=imageh1 alt="">
                        <span style="font-size: 20px;">今日宜考试，睡觉</span></a></li>
                <li><a href="/" title="今日忌上课，运动"><img :src=imageh2 alt=""><span
                            style="font-size: 20px;">今日忌上课，运动</span></a></li>
            </ul>
        </div>
        <!--headline end-->
    </div>
</template>

<script>
import { ref } from 'vue';
import imageh1 from '../../images/h1.jpg';
import imageh2 from '../../images/h2.jpg';
import image1 from '../../images/1.jpg';
import image2 from '../../images/2.jpg';
import image3 from '../../images/3.jpg';
import image4 from '../../images/4.jpg';
export default {
    setup() {
        const slides = ref([
            { src: imageh2, alt: 'Image H2' },
            { src: image1, alt: 'Image 1' },
            { src: image2, alt: 'Image 2' },
            { src: image3, alt: 'Image 3' },
            { src: image4, alt: 'Image 4' }
        ]);

        return {
            slides,
            image1,
            image2,
            image3,
            image4,
            imageh1,
            imageh2
        }
    }
}
</script>


<style scoped>
.toutiao {
    display: flex;
    justify-content: space-between;
    margin: 10px;
}

.banbox {
    flex: 3;
    margin-right: 10px;

}

.headline {
    flex: 1;
    margin: 10px;
}

.headline ul {

    height: 100%;
}

.headline li {
    margin: 10px 0px;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
    background-color: #d3dce6;
}

.carousel-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* 确保图片填充容器并保持比例 */
}
</style>