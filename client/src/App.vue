<template>
  <div id="app">
    <el-row>
      <canvas
        id="orig-img"
        :width="canvasWidth"
        :height="canvasHeight"
        @click.left="addRoiVertex"
        @click.right="removeRoiVertex"
        @contextmenu.prevent
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
import axios from "axios";

export default {
  name: "app",
  components: {},
  data() {
    return {
      canvasWidth: 800, // 画布宽度
      canvasHeight: 600, // 画布高度
      origImg: new Image(),
      origImgId: "",
      origImgWidth: 0, // 原始图像宽度
      origImgHeight: 0, // 原始图像高度
      imgPosition: {
        // 图像在画布中，相对于画布的显示位置
        left: 0, // 左边界
        right: 0, // 右边界
        top: 0, // 上边界
        bottom: 0 // 下边界
      },
      roiPts: [] // 发票的 4 个顶点数组
    };
  },
  mounted: () => {
    document.title = "票据分割示例";
  },
  methods: {
    addRoiVertex(evt) {
      // 将鼠标坐标，转换为 canvas 内部的坐标。
      // 需减去 canvas 边框的大小
      var x = evt.layerX - 5;
      var y = evt.layerY - 5;

      // 如果坐标在显示区域内，且顶点数不足 4 个，则添加该顶点
      if (
        x >= this.imgPosition.left &&
        x <= this.imgPosition.right &&
        y >= this.imgPosition.top &&
        y <= this.imgPosition.bottom &&
        this.roiPts.length < 4
      ) {
        this.roiPts.push({ x, y });
      }
    },
    removeRoiVertex() {
      // 去掉最后一个顶点
      if (this.roiPts.length > 0) {
        this.roiPts.pop();
      }
    },
    async wrapPerspective() {
      // 调用服务完成透视变换
      var res = await axios.post("/api/wrap_perspective", {
        imgId: this.origImgId,
        roiPts: this.roiPts
      });
      this.handleUploaded(res);
    },
    wrapSegmentation() {},
    handleUploaded(res) {
      // 上载图像成功后，按照图像比例缩放显示在画布中
      var canvas = document.getElementById("orig-img");
      var ctx = canvas.getContext("2d");

      var _this = this;

      _this.origImg.onload = function() {
        // 保存原始图像宽度、高度
        _this.origImgWidth = this.width;
        _this.origImgHeight = this.height;

        // 清除画布
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 按照图像比例缩放，居中显示
        var dx, dy, dWidth, dHeight;

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

        // 保存图像相对于画布的显示位置
        _this.imgPosition.left = dx;
        _this.imgPosition.top = dy;
        _this.imgPosition.right = dx + dWidth;
        _this.imgPosition.bottom = dy + dHeight;
      };
      _this.origImg.src = res.uploadImgUrl;
      _this.origImgId = res.uploadImgId;
    }
  },
  watch: {
    roiPts: function(newRoiPts) {
      // 顶点坐标数组发生变化，执行重画

      var canvas = document.getElementById("orig-img");
      var ctx = canvas.getContext("2d");
      // 清除画布
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // 绘制图像
      ctx.drawImage(
        this.origImg,
        this.imgPosition.left,
        this.imgPosition.top,
        this.imgPosition.right - this.imgPosition.left,
        this.imgPosition.bottom - this.imgPosition.top
      );
      // 绘制 ROI 区域顶点，及边界
      if (newRoiPts.length > 0) {
        ctx.lineWidth = 4;
        ctx.lineCap = "square";
        ctx.strokeStyle = "rgba(200, 0, 0)";
        ctx.beginPath();
        ctx.moveTo(newRoiPts[0].x, newRoiPts[0].y);
        for (let pt of newRoiPts) {
          ctx.lineTo(pt.x, pt.y);
        }
        if (newRoiPts.length == 4) {
          ctx.closePath();
          ctx.stroke();
        } else {
          ctx.stroke();
          ctx.closePath();
        }
      }
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

#orig-img {
  border: 5px solid #d9d9d9;
}
</style>
