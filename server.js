const express = require("express");
const { exec } = require("child_process");

const app = express();

app.use(express.json());

// 定义POST路由用于执行Python脚本
app.post("/api/run-python", (req, res) => {
  // 从请求体中解构获取脚本名称和参数
  const { script, args } = req.body;
  // 构建Python命令字符串
  const command = `python src/utils/${script} ${args}`;
  // 执行Python脚本
  exec(command, (error, stdout, stderr) => {
    // 如果执行出错，返回500错误状态码和错误信息
    if (error) {
      return res.status(500).json({ error: stderr });
    }
    // 执行成功，返回脚本的标准输出
    res.json({ output: stdout });
  });
});

// 设置服务器监听端口，优先使用环境变量中的PORT，默认为3000
const PORT = process.env.PORT || 3000;
// 启动服务器并监听指定端口
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
