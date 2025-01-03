<template>
    <div class="common-layout whitebg">
        该内容不存在，可能被屏蔽或者被举报
    </div>
</template>


<script>
export default {
    name: 'no_content',
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