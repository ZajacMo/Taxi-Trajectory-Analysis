const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    https: false,
    open: false,
    proxy: {
      "/api": {
        target: "http://0.0.0.0:5000/api",
        changeOrigin: true,
      },
    },
  },
});
