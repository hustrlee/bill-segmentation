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
    <el-row style="margin-bottom: 20px;">
      <el-upload
        action="/api/upload"
        :show-file-list="false"
        accept=".jpg, .jpeg, .png, .bmp"
        :on-success="loadImage"
        :on-error="
          err => {
            this.$alert(JSON.parse(err.message).message, '错误', {
              type: 'error'
            });
          }
        "
      >
        <el-button slot="trigger">选择图片</el-button>
        <el-button
          style="margin-left: 10px;"
          @click="wrapPerspective"
          :disabled="roiPts.length < 4"
        >
          矫正图片</el-button
        >
        <el-button style="margin-left: 10px;" @click="wrapSegmentation">
          分割图片</el-button
        >
      </el-upload>
    </el-row>
    <el-row v-for="item in segmentationImgs" :key="item.name">
      <div>{{ item.name }}</div>
      <div>
        <img :src="item.img_url" />
      </div>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";

const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const CANVAS_BORDER_SIZE = 5;

export default {
  name: "app",
  components: {},
  data() {
    return {
      canvasWidth: CANVAS_WIDTH, // 画布宽度
      canvasHeight: CANVAS_HEIGHT, // 画布高度
      origImg: new Image(), // 原始图像对象
      origImgId: "", // 原始图像 ID，由服务器设置，并保持唯一，用于指定服务器图像
      imgRect: {
        // 图像相对于画布的显示位置
        left: 0, // 左边界
        top: 0, // 上边界
        width: 0, // 宽度
        height: 0 // 高度
      },
      roiPts: [], // 相对于画布的 4 个顶点数组
      segmentationImgs: [] // 分割结果
    };
  },
  mounted: () => {
    document.title = "票据分割示例";
  },
  methods: {
    addRoiVertex(evt) {
      // 将鼠标坐标转换为 canvas 内部的坐标：需减去 canvas 边框的大小
      var x = evt.layerX - CANVAS_BORDER_SIZE;
      var y = evt.layerY - CANVAS_BORDER_SIZE;

      // 如果顶点数不足 4 个，则添加该顶点。
      if (this.roiPts.length < 4) {
        this.roiPts.push({ x, y });
      }
    },
    removeRoiVertex() {
      // 若果顶点数组不为空，去掉最后一个顶点
      if (this.roiPts.length > 0) {
        this.roiPts.pop();
      }
    },
    loadImage(res) {
      // 从服务器载入图像，并按照图像比例缩放显示在画布中
      var canvas = document.getElementById("orig-img");
      var ctx = canvas.getContext("2d");

      var _this = this;

      _this.origImg.onload = function() {
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
        _this.imgRect.left = dx;
        _this.imgRect.top = dy;
        _this.imgRect.width = dWidth;
        _this.imgRect.height = dHeight;

        // 清空 ROI 的顶点，可能触发画布重画
        _this.roiPts.length = 0;
      };
      _this.origImg.src = res.imgUrl;
      _this.origImgId = res.imgId;
    },
    async wrapPerspective() {
      // 将相对于画布的 roiPts 坐标转换成相对于原始图像的 imgRoiPts
      var ratio =
        this.origImg.width > this.origImg.height
          ? this.origImg.width / this.imgRect.width
          : this.origImg.height / this.imgRect.height;
      var imgRoiPts = [];
      var _this = this;
      this.roiPts.forEach(element =>
        imgRoiPts.push({
          x: Math.round((element.x - _this.imgRect.left) * ratio),
          y: Math.round((element.y - _this.imgRect.top) * ratio)
        })
      );
      // 调用服务完成透视变换
      try {
        var res = await axios.post(
          "/api/warp-perspective/sh-invoice/" + this.origImgId,
          { pts: imgRoiPts }
        );
        this.loadImage(res.data);
      } catch (error) {
        this.$alert(error.response.data.message, "错误", { type: "error" });
      }
    },
    async wrapSegmentation() {
      // 调用服务完成图像分割
      try {
        this.segmentationImgs = (
          await axios.get("/api/warp-segmentation/sh-invoice/" + this.origImgId)
        ).data;
      } catch (error) {
        this.$alert(error.response.data.message, "错误", { type: "error" });
      }
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
        this.imgRect.left,
        this.imgRect.top,
        this.imgRect.width,
        this.imgRect.height
      );

      // 绘制 ROI 区域顶点，及边界
      if (newRoiPts.length > 0) {
        ctx.lineWidth = 4;
        ctx.lineCap = "square";
        ctx.strokeStyle = "rgba(255, 0, 0)";
        ctx.beginPath();
        ctx.moveTo(newRoiPts[0].x, newRoiPts[0].y);
        for (let pt of newRoiPts) {
          ctx.lineTo(pt.x, pt.y);
        }
        if (newRoiPts.length == 4) {
          // 如果已加入 4 个顶点，则需要闭合 ROI 区域
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
