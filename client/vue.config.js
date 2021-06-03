module.exports = {
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000", // api接口基础路径
        changeOrigin: true, // 是否支持跨域
        ws: true,
        pathRewrite: {
          "^/api": "/bill-segmentation" // 重写路径：去掉路径中开头的 '/api'
        }
      }
    }
  }
};
