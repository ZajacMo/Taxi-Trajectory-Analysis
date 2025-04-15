<template>
  <div class="admin-panel">
    <h2>节点管理</h2>
    <el-table :data="nodes" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button @click="editNode(scope.row)">编辑</el-button>
          <el-button type="danger" @click="deleteNode(scope.row.id)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="nodeDialogVisible" title="节点编辑">
      <el-form :model="currentNode">
        <el-form-item label="名称">
          <el-input v-model="currentNode.name"></el-input>
        </el-form-item>
        <el-form-item label="X坐标">
          <el-input-number v-model="currentNode.x"></el-input-number>
        </el-form-item>
        <el-form-item label="Y坐标">
          <el-input-number v-model="currentNode.y"></el-input-number>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="nodeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitNode">确认</el-button>
      </span>
    </el-dialog>

    <h2>道路管理</h2>
    <el-table :data="edges" style="width: 100%">
      <el-table-column prop="source" label="起点"></el-table-column>
      <el-table-column prop="target" label="终点"></el-table-column>
      <el-table-column prop="weight" label="距离"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button @click="editEdge(scope.row)">编辑</el-button>
          <el-button type="danger" @click="deleteEdge(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="edgeDialogVisible" title="道路编辑">
      <el-form :model="currentEdge">
        <el-form-item label="起点ID">
          <el-input-number v-model="currentEdge.source"></el-input-number>
        </el-form-item>
        <el-form-item label="终点ID">
          <el-input-number v-model="currentEdge.target"></el-input-number>
        </el-form-item>
        <el-form-item label="距离">
          <el-input-number v-model="currentEdge.weight"></el-input-number>
        </el-form-item>
        <el-form-item label="交通工具">
          <el-select v-model="currentEdge.transport">
            <el-option label="步行" value="walk"></el-option>
            <el-option label="自行车" value="bike"></el-option>
            <el-option label="校车" value="shuttle"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="edgeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdge">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      nodes: [],
      edges: [],
      nodeDialogVisible: false,
      edgeDialogVisible: false,
      currentNode: { id: null, name: "", x: 0, y: 0 },
      currentEdge: { source: null, target: null, weight: 0, transport: "walk" },
    };
  },
  mounted() {
    this.fetchNodes();
    this.fetchEdges();
  },
  methods: {
    async fetchNodes() {
      try {
        const res = await this.$axios.get("/admin/nodes");
        this.nodes = res.data;
      } catch (error) {
        this.$message.error("获取节点数据失败");
      }
    },
    async fetchEdges() {
      // 需要后端添加获取所有边的接口
    },
    editNode(node) {
      this.currentNode = { ...node };
      this.nodeDialogVisible = true;
    },
    async submitNode() {
      try {
        if (this.currentNode.id) {
          await this.$axios.put(
            `/admin/nodes/${this.currentNode.id}`,
            this.currentNode
          );
        } else {
          await this.$axios.post("/admin/nodes", this.currentNode);
        }
        this.fetchNodes();
        this.nodeDialogVisible = false;
      } catch (error) {
        this.$message.error("操作失败");
      }
    },
    async deleteNode(id) {
      try {
        await this.$axios.delete(`/admin/nodes/${id}`);
        this.fetchNodes();
      } catch (error) {
        this.$message.error("删除失败");
      }
    },
    editEdge(edge) {
      this.currentEdge = { ...edge };
      this.edgeDialogVisible = true;
    },
    submitEdge() {
      // 对接后端道路管理接口
    },
  },
};
</script>

<style>
.admin-panel {
  padding: 20px;
}
.el-table {
  margin-bottom: 20px;
}
</style>
