const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// 图数据结构类
class Graph {
  constructor() {
    this.nodes = new Map();
    this.adjacencyList = new Map();
  }

  addNode(node) {
    this.nodes.set(node.id, node);
    this.adjacencyList.set(node.id, []);
  }

  addEdge(source, target, weight, transport) {
    this.adjacencyList.get(source).push({ target, weight, transport });
    this.adjacencyList.get(target).push({ source, weight, transport });
  }

  dijkstra(startId, endId, transportType) {
    const transportWeights = {
      walk: 1,
      bike: 0.6,
      shuttle: 0.3,
    };

    const distances = new Map();
    const previous = new Map();
    const priorityQueue = [];

    this.nodes.forEach((_, id) => {
      distances.set(id, Infinity);
      previous.set(id, null);
    });

    distances.set(startId, 0);
    priorityQueue.push({ id: startId, distance: 0 });

    while (priorityQueue.length > 0) {
      priorityQueue.sort((a, b) => a.distance - b.distance);
      const { id: currentId } = priorityQueue.shift();

      if (currentId === endId) break;

      for (const edge of this.adjacencyList.get(currentId)) {
        const weightModifier =
          transportWeights[transportType] / transportWeights[edge.transport];
        const alt = distances.get(currentId) + edge.weight * weightModifier;

        if (alt < distances.get(edge.target)) {
          distances.set(edge.target, alt);
          previous.set(edge.target, currentId);
          priorityQueue.push({ id: edge.target, distance: alt });
        }
      }
    }

    const path = [];
    let current = endId;
    while (previous.has(current)) {
      path.unshift({
        from: previous.get(current),
        to: current,
        transport: this.adjacencyList
          .get(previous.get(current))
          .find((e) => e.target === current).transport,
      });
      current = previous.get(current);
    }

    return path.length ? { path, distance: distances.get(endId) } : null;
  }
}

const campusGraph = new Graph();

// 添加测试数据
campusGraph.addNode({ id: 1, name: "图书馆", x: 200, y: 200 });
campusGraph.addNode({ id: 2, name: "教学楼", x: 400, y: 400 });
campusGraph.addEdge(1, 2, 150, "walk");

// 获取地图数据端点
app.get("/api/map-data", (req, res) => {
  res.json({
    nodes: Array.from(campusGraph.nodes.values()),
    edges: Array.from(campusGraph.adjacencyList.entries()).flatMap(
      ([source, edges]) => edges.map((edge) => ({ source, ...edge }))
    ),
  });
});

// 管理员鉴权中间件
const adminAuth = (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ error: "未授权" });
  // 实际应验证JWT并检查用户角色
  next();
};

// 管理员节点管理端点
app.get("/admin/nodes", adminAuth, (req, res) => {
  res.json(Array.from(campusGraph.nodes.values()));
});

app.post("/admin/nodes", adminAuth, (req, res) => {
  const { name, x, y } = req.body;
  const id = Date.now();
  campusGraph.nodes.set(id, { id, name, x, y });
  res.status(201).json({ id });
});

app.put("/admin/nodes/:id", adminAuth, (req, res) => {
  const node = campusGraph.nodes.get(Number(req.params.id));
  if (!node) return res.status(404).json({ error: "节点不存在" });
  Object.assign(node, req.body);
  res.json(node);
});

app.delete("/admin/nodes/:id", adminAuth, (req, res) => {
  if (!campusGraph.nodes.delete(Number(req.params.id))) {
    return res.status(404).json({ error: "节点不存在" });
  }
  res.sendStatus(204);
});

// // 图数据结构类
// class Graph {
//   constructor() {
//     this.nodes = new Map();
//     this.adjacencyList = new Map();
//   }

//   addNode(node) {
//     this.nodes.set(node.id, node);
//     this.adjacencyList.set(node.id, []);
//   }

//   addEdge(source, target, weight, transport) {
//     this.adjacencyList.get(source).push({ target, weight, transport });
//     this.adjacencyList.get(target).push({ source, weight, transport });
//   }

//   dijkstra(startId, endId, transportType) {
//     const transportWeights = {
//       walk: 1,
//       bike: 0.6,
//       shuttle: 0.3
//     };

//     const distances = new Map();
//     const previous = new Map();
//     const priorityQueue = [];

//     this.nodes.forEach((_, id) => {
//       distances.set(id, Infinity);
//       previous.set(id, null);
//     });

//     distances.set(startId, 0);
//     priorityQueue.push({ id: startId, distance: 0 });

//     while (priorityQueue.length > 0) {
//       priorityQueue.sort((a, b) => a.distance - b.distance);
//       const { id: currentId } = priorityQueue.shift();

//       if (currentId === endId) break;

//       for (const edge of this.adjacencyList.get(currentId)) {
//         const weightModifier = transportWeights[transportType] / transportWeights[edge.transport];
//         const alt = distances.get(currentId) + edge.weight * weightModifier;

//         if (alt < distances.get(edge.target)) {
//           distances.set(edge.target, alt);
//           previous.set(edge.target, currentId);
//           priorityQueue.push({ id: edge.target, distance: alt });
//         }
//       }
//     }

//     const path = [];
//     let current = endId;
//     while (previous.has(current)) {
//       path.unshift({
//         from: previous.get(current),
//         to: current,
//         transport: this.adjacencyList.get(previous.get(current))
//           .find(e => e.target === current).transport
//       });
//       current = previous.get(current);
//     }

//     return path.length ? { path, distance: distances.get(endId) } : null;
//   }
// }

// 最短路径计算端点
app.post("/api/shortest-path", (req, res) => {
  const { startId, endId, transport = "walk" } = req.body;

  if (!campusGraph.nodes.has(startId) || !campusGraph.nodes.has(endId)) {
    return res.status(400).json({ error: "无效的节点ID" });
  }

  const result = campusGraph.dijkstra(startId, endId, transport);
  if (!result) {
    return res.status(400).json({ error: "路径不存在" });
  }

  res.json({
    path: result.path.map((step) => campusGraph.nodes.get(step.to).name),
    distance: result.distance.toFixed(1),
  });
});

// 管理员节点管理接口
app.post("/api/admin/nodes", (req, res) => {
  const { id, name, x, y } = req.body;
  if (campusGraph.nodes.has(id)) {
    return res.status(400).json({ error: "节点ID已存在" });
  }
  campusGraph.nodes.set(id, { id, name, x, y });
  res.status(201).json({ message: "节点添加成功", node: { id, name, x, y } });
});

app.delete("/api/admin/nodes/:id", (req, res) => {
  const id = parseInt(req.params.id);
  if (!campusGraph.nodes.has(id)) {
    return res.status(404).json({ error: "节点不存在" });
  }
  campusGraph.nodes.delete(id);
  // 删除关联的边
  campusGraph.adjacencyList.forEach((edges, sourceId) => {
    campusGraph.adjacencyList.set(
      sourceId,
      edges.filter((edge) => edge.target !== id)
    );
  });
  campusGraph.adjacencyList.delete(id);
  res.json({ message: "节点删除成功" });
});

app.put("/api/admin/nodes/:id", (req, res) => {
  const id = parseInt(req.params.id);
  if (!campusGraph.nodes.has(id)) {
    return res.status(404).json({ error: "节点不存在" });
  }
  const { name, x, y } = req.body;
  const node = campusGraph.nodes.get(id);
  if (name) node.name = name;
  if (x !== undefined) node.x = x;
  if (y !== undefined) node.y = y;
  res.json({ message: "节点更新成功", node });
});

app.get("/api/admin/nodes", (req, res) => {
  res.json(Array.from(campusGraph.nodes.values()));
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
