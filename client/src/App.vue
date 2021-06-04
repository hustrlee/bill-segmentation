<template>
  <div id="app">
    <el-row>
      <canvas
        id="orig-img"
        :width="canvasWidth"
        :height="canvasHeight"
        style="border: 5px solid #d9d9d9; z-index: 1; position: absolute;"
      >
      </canvas>
      <canvas
        id="mask"
        :width="canvasWidth"
        :height="canvasHeight"
        style="border: 5px solid #d9d9d9; z-index: 2; position: absolute;"
        @click="selectRoi"
      >
      </canvas>
    </el-row>
    <el-row>
      <el-upload
        action="/api/upload"
        :show-file-list="false"
        accept=".jpg, .jpeg, .png, .bmp"
        :on-success="handleUploaded"
      >
        <el-button slot="trigger">选择图片</el-button>
        <el-button style="margin-left: 10px;" @click="wrapPerspective">
          矫正图片</el-button
        >
        <el-button style="margin-left: 10px;" @click="wrapSegmentation">
          分割图片</el-button
        >
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
      canvasWidth: 800, // 画布宽度
      canvasHeight: 600, // 画布高度
      origImgWidth: 0, // 原始图像宽度
      origImgHeight: 0, // 原始图像高度
      roiPts: [] // 发票的 4 个顶点数组
    };
  },
  mounted: () => {
    document.title = "票据分割示例";
  },
  methods: {
    selectRoi(evt) {
      var canvas = document.getElementById("orig-img");
      // 将鼠标的绝对坐标，转换为 canvas 内部的坐标。
      // 需减去 canvas 边框的大小
      var dx = evt.layerX - 5,
        dy = evt.layerY - 5;

      var ctx = canvas.getContext("2d");
      // ctx.save();
      // ctx.beginPath();
      ctx.arc(dx, dy, 5, 0, 2 * Math.PI, false);
      // ctx.fillStyle = "red";
      // ctx.fill();
      // ctx.closePath();
      // ctx.restore();
    },
    wrapPerspective() {},
    wrapSegmentation() {},
    handleUploaded(res) {
      // 上载图像成功后，按照图像比例缩放显示在画布中
      var canvas = document.getElementById("orig-img");
      var ctx = canvas.getContext("2d");

      var img = new Image();
      var _this = this;

      img.onload = function() {
        // 保存原始图像宽度、高度
        _this.origImgWidth = this.width;
        _this.origImgHeight = this.height;

        // 按照图像比例缩放，居中显示
        var dx, dy, dWidth, dHeight;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (this.width > this.height) {
          // 图像是横向的
          dx = 0;
          dWidth = canvas.width;
          dHeight = (this.height * dWidth) / this.width;
          dy = (canvas.height - dHeight) / 2;
        } else {
          // 图像是纵向的
          dy = 0;
          dHeight = canvas.height;
          dWidth = (this.width * dHeight) / this.height;
          dx = (canvas.width - dWidth) / 2;
        }
        ctx.drawImage(this, dx, dy, dWidth, dHeight);
      };
      img.src = res.uploadImgUrl;
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
