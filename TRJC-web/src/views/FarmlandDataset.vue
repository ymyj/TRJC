<template>
  <div>
    <!-- 详情弹窗 -->
    <DatasetDetailModal v-model:visible="modalVisible" :data="selectedData" />
    
    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-item">
          <label class="filter-label">任务名称</label>
          <input type="text" class="form-input" placeholder="请输入任务名称" v-model="filterForm.taskName">
        </div>
        <div class="filter-item">
          <label class="filter-label">图斑编号</label>
          <input type="text" class="form-input" placeholder="请输入图斑编号" v-model="filterForm.plotNumber">
        </div>
        <div class="filter-item">
          <label class="filter-label">采样日期</label>
          <input type="text" class="form-input" placeholder="请选择采样日期" v-model="filterForm.sampleDate">
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-actions">
          <button class="btn btn-default" @click="resetFilter">重置</button>
          <button class="btn btn-primary" @click="handleQuery">查询</button>
        </div>
      </div>
    </div>

    <!-- 列表区域 -->
    <div class="list-section">
      <div class="list-header">
        <h3 class="list-title">耕地质量数据集</h3>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th class="col-fixed col-fixed-left-1">任务名称</th>
              <th class="col-fixed col-fixed-left-2">图斑编号</th>
              <th>经度</th>
              <th>纬度</th>
              <th>采样日期</th>
              <th>地形部位</th>
              <th>有效土层厚度(cm)</th>
              <th>耕层质地</th>
              <th>容重(g/cm³)</th>
              <th>质地构型</th>
              <th>生物多样性</th>
              <th>农田林网化程度</th>
              <th>障碍因素</th>
              <th>灌溉能力</th>
              <th>排水能力</th>
              <th>pH值</th>
              <th class="col-fixed col-fixed-right">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in datasetList" :key="item.id">
              <td class="col-fixed col-fixed-left-1">{{ item.taskName }}</td>
              <td class="col-fixed col-fixed-left-2">{{ item.plotNumber }}</td>
              <td>{{ item.longitude }}</td>
              <td>{{ item.latitude }}</td>
              <td>{{ item.sampleDate }}</td>
              <td>{{ item.terrain }}</td>
              <td>{{ item.soilThickness }}</td>
              <td>{{ item.soilTexture }}</td>
              <td>{{ item.bulkDensity }}</td>
              <td>{{ item.textureStructure }}</td>
              <td>{{ item.biodiversity }}</td>
              <td>{{ item.forestNetwork }}</td>
              <td>{{ item.obstacleFactor }}</td>
              <td>{{ item.irrigationCapacity }}</td>
              <td>{{ item.drainageCapacity }}</td>
              <td>{{ item.phValue }}</td>
              <td class="col-fixed col-fixed-right">
                <div class="action-links">
                  <span class="action-link" @click="viewDetail(item)">详情</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-wrapper">
        <span class="pagination-info">显示 {{ pagination.start }} 到 {{ pagination.end }} 条，共 {{ pagination.total }} 条记录</span>
        <div class="pagination">
          <button class="page-btn" :disabled="pagination.current === 1" @click="changePage(pagination.current - 1)">&lt;</button>
          <button 
            v-for="page in pagination.pages" 
            :key="page" 
            class="page-btn" 
            :class="{ active: page === pagination.current }"
            @click="changePage(page)"
          >{{ page }}</button>
          <button class="page-btn" :disabled="pagination.current === pagination.totalPages" @click="changePage(pagination.current + 1)">&gt;</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import DatasetDetailModal from '../components/DatasetDetailModal.vue'
import { getDatasetList } from '../api'

const modalVisible = ref(false)
const selectedData = ref({})

const filterForm = reactive({
  taskName: '',
  plotNumber: '',
  sampleDate: ''
})

const datasetList = ref([])

const pagination = reactive({
  current: 1,
  total: 0,
  pageSize: 9,
  pages: [],
  get start() { return (this.current - 1) * this.pageSize + 1 },
  get end() { return Math.min(this.current * this.pageSize, this.total) },
  get totalPages() { return Math.ceil(this.total / this.pageSize) }
})

const updatePaginationPages = () => {
  const totalPages = pagination.totalPages
  const pages = []
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || Math.abs(i - pagination.current) <= 2) {
      pages.push(i)
    }
  }
  pagination.pages = pages
}

const fetchList = async () => {
  const params = {
    page: pagination.current,
    pageSize: pagination.pageSize
  }
  if (filterForm.taskName) params.taskName = filterForm.taskName
  if (filterForm.plotNumber) params.plotNumber = filterForm.plotNumber
  if (filterForm.sampleDate) params.sampleDate = filterForm.sampleDate

  const res = await getDatasetList(params)
  if (res.data.code === 200) {
    datasetList.value = res.data.data.list || []
    pagination.total = res.data.data.total || 0
    updatePaginationPages()
  }
}

const resetFilter = () => {
  filterForm.taskName = ''
  filterForm.plotNumber = ''
  filterForm.sampleDate = ''
  fetchList()
}

const handleQuery = () => {
  pagination.current = 1
  fetchList()
}

const viewDetail = (item) => {
  selectedData.value = item
  modalVisible.value = true
}

const changePage = (page) => {
  if (page >= 1 && page <= pagination.totalPages) {
    pagination.current = page
    fetchList()
  }
}

onMounted(() => {
  fetchList()
})
</script>

<style scoped>
.filter-section {
  background-color: #fff;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.filter-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.filter-row:last-child {
  margin-bottom: 0;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  color: #595959;
  font-weight: 500;
}

.form-input {
  width: 200px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
  transition: all 0.3s;
}

.form-input:hover {
  border-color: #4096ff;
}

.form-input:focus {
  outline: none;
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}

.form-input::placeholder {
  color: #bfbfbf;
}

.filter-actions {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.btn {
  height: 36px;
  padding: 0 20px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-default {
  background-color: #fff;
  border: 1px solid #d9d9d9;
  color: #595959;
}

.btn-default:hover {
  border-color: #4096ff;
  color: #4096ff;
}

.btn-primary {
  background-color: #1677ff;
  color: #fff;
}

.btn-primary:hover {
  background-color: #4096ff;
}

.list-section {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.list-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.table-container {
  overflow-x: auto;
  position: relative;
}

.data-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.data-table th {
  background-color: #fafafa;
  padding: 16px 16px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

.data-table td {
  padding: 20px 16px;
  font-size: 14px;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
}

.data-table tr:hover {
  background-color: #fafafa;
}

/* 固定列样式 */
.col-fixed {
  position: sticky;
  background-color: #fff;
  z-index: 1;
}

.data-table tr:hover .col-fixed {
  background-color: #fafafa;
}

.col-fixed-left-1 {
  left: 0;
  min-width: 280px;
}

.col-fixed-left-2 {
  left: 280px;
  min-width: 80px;
}

.col-fixed-right {
  right: 0;
  min-width: 80px;
}

.data-table th.col-fixed {
  background-color: #fafafa;
  z-index: 2;
}

.action-links {
  display: flex;
  gap: 12px;
}

.action-link {
  color: #1677ff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.action-link:hover {
  color: #4096ff;
}

.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
}

.pagination-info {
  font-size: 14px;
  color: #595959;
}

.pagination {
  display: flex;
  gap: 8px;
}

.page-btn {
  min-width: 32px;
  height: 32px;
  padding: 0 8px;
  border: 1px solid #d9d9d9;
  background-color: #fff;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #595959;
  transition: all 0.3s;
}

.page-btn:hover {
  border-color: #1677ff;
  color: #1677ff;
}

.page-btn.active {
  background-color: #1677ff;
  border-color: #1677ff;
  color: #fff;
}

.page-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
