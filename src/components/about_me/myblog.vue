<template>
  <div >
    <h2 class="gd_title">心路历程</h2>
    <ul class="xinlu">
      <li><a href="/" target="_blank"><i><img :src="image1"></i>
        <p>我是怎么评价自己的？</p>
        <span>我性格属于好静的，喜欢写写画画，自从读了计算机专业，那就更好静了，我可以两星期都不出门，但是半刻钟也不能离开电脑。</span></a></li>
      <li><a href="/" target="_blank"><i><img :src="image2"></i>
        <p>个人博客，属于我的小世界！</p>
        <span>个人博客，用来做什么？我刚开始就把它当做一个我吐槽心情的地方，也就相当于一个网络记事本，写上一些关于自己生活工作中的小情小事，也会放上一些照片，音乐。每天工作回家后就能访问自己的网站，一边听着音乐，一边写写文章。</span></a></li>
      <li><a href="/" target="_blank"><i><img :src="image3"></i>
        <p>【爱设计】安静地做一个爱设计的女子</p>
        <span>自从入了这行，很多人跟我说可以做网络教程，我也有考虑，但最终没有实现，因为我觉得在这个教程泛滥的时代，直接做一套免费的原创个人博客模板更为实在。</span></a></li>
      <li><a href="/" target="_blank"><i><img :src="image4"></i>
        <p>【匆匆那些年】总结个人博客经历的这四年</p>
        <span>博客从最初的域名购买，到上线已经有四年的时间了，这四年的时间，有笑过，有怨过，有悔过，有执着过，也有放弃过…但最后还是坚持了下来，时间如此匆匆，等再回过头已来不及去弥补</span></a></li>
      <li><a href="/" target="_blank"><i><img :src="imagead"></i>
        <p>我是怎么评价自己的？</p>
        <span>我性格属于好静的，喜欢写写画画，自从读了计算机专业，那就更好静了，我可以两星期都不出门，但是半刻钟也不能离开电脑。</span></a></li>
      <li><a href="/" target="_blank"><i><img :="imagead02"></i>
        <p>个人博客，属于我的小世界！</p>
        <span>个人博客，用来做什么？我刚开始就把它当做一个我吐槽心情的地方，也就相当于一个网络记事本，写上一些关于自己生活工作中的小情小事，也会放上一些照片，音乐。每天工作回家后就能访问自己的网站，一边听着音乐，一边写写文章。</span></a></li>
      <li><a href="/" target="_blank"><i><img :src="imageb01"></i>
        <p>【爱设计】安静地做一个爱设计的女子</p>
        <span>自从入了这行，很多人跟我说可以做网络教程，我也有考虑，但最终没有实现，因为我觉得在这个教程泛滥的时代，直接做一套免费的原创个人博客模板更为实在。</span></a></li>
      <li><a href="/" target="_blank"><i><img :src="imageb05"></i>
        <p>【匆匆那些年】总结个人博客经历的这四年</p>
        <span>博客从最初的域名购买，到上线已经有四年的时间了，这四年的时间，有笑过，有怨过，有悔过，有执着过，也有放弃过…但最后还是坚持了下来，时间如此匆匆，等再回过头已来不及去弥补</span></a></li>
    </ul>
  </div>
</template>

<script>
import image1 from '../../images/1.jpg';
import image2 from '../../images/2.jpg';
import image3 from '../../images/3.jpg';
import image4 from '../../images/4.jpg';
import imagead from '../../images/ad.jpg';
import imagead02 from '../../images/ad02.jpg';
import imageb01 from '../../images/b01.jpg';
import imageb05 from '../../images/b05.jpg';
export default {
    name: 'Myblog',
    data() {
        return {
            image1,
            image2,
            image3,
            image4,
            imagead,
            imagead02,
            imageb01,
            imageb05
        }
    }
}

</script>