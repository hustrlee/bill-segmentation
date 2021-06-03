<template>
  <div id="app">
    <el-row>
      <el-image
        style="width: 800px; height: 600px; border: 5px solid #d9d9d9;"
        :src="imgUrl"
        fit="scale-down"
        @click="hello($event)"
      >
      </el-image>
    </el-row>
    <el-row>
      <el-upload action="/api/upload" :on-success="handleUploaded">
        <el-button>选择图片</el-button>
      </el-upload>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {},
  data() {
    return {
      imgUrl:
        "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
    };
  },
  mounted: () => {
    document.title = "票据分割示例";
  },
  methods: {
    hello(evt) {
      alert(
        "clientX value: " +
          evt.clientX +
          "\n" +
          "clientY value: " +
          evt.clientY +
          "\n"
      );
    },
    handleUploaded(res) {
      console.log(res);
      this.imgUrl = res;
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
