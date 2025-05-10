const express = require("express");
const { createProxyMiddleware } = require("http-proxy-middleware");
const path = require("path");
// const sqlite3 = require("sqlite3").verbose();
const app = express();
const port = 3000;
const backendUrl = "http://localhost:5000"; // 后端API地址

// 数据库连接
// const db = new sqlite3.Database(path.join(__dirname, "trajectory.db"));

app.use(express.json()); // 解析JSON请求体
// 1. 静态文件服务（指向打包后的dist目录）
app.use(express.static(path.join(__dirname, "dist")));

// 2. API代理（将/api前缀的请求转发到后端）
app.use(
  "/api",
  createProxyMiddleware({
    target: backendUrl,
    changeOrigin: true,
    pathRewrite: { "^/api": "" }, // 去除请求路径中的/api前缀
    logLevel: "debug",
  })
);

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

app.use((req, res, next) => {
  console.log(`收到请求: ${req.method} ${req.url}`);
  next(); // 传递给下一个中间件
});
