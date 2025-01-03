<template>
    <div class="common-layout whitebg">
        若要访问此内容，请先<a href="/login">登录</a>
    </div>
</template>


<script>
export default {
    name: 'please login',
    components: {
    }
}

</script>

<style>
.common-layout {
    margin: 0 auto;
    width: 80%;
    padding: 0 10px;
    overflow: hidden;
}

.common-layout ul {
    padding: 10px 0 0
}

.common-layout li {
    overflow: hidden;
    margin-bottom: 20px;
    border-bottom: #eee 1px dashed;
    padding-bottom: 20px;
    position: relative;
}
</style>