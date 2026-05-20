<template>
  <div>
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-item">
          <label class="filter-label">图斑编号</label>
          <input type="text" class="form-input" placeholder="请输入图斑编号" v-model="filterForm.keyword">
        </div>
        <div class="filter-item">
          <label class="filter-label">所属区划</label>
          <select class="form-select" v-model="filterForm.ssqh">
            <option value="">全部区划</option>
            <option value="东城区">东城区</option>
            <option value="西城区">西城区</option>
            <option value="朝阳区">朝阳区</option>
            <option value="海淀区">海淀区</option>
            <option value="丰台区">丰台区</option>
          </select>
        </div>
      </div>
      <div class="filter-row">
        <div class="filter-actions">
          <button class="btn btn-default" @click="resetFilter">重置</button>
          <button class="btn btn-primary" @click="handleQuery">查询</button>
        </div>
      </div>
    </div>

    <div class="list-section">
      <div class="list-header">
        <h3 class="list-title">地块管理列表</h3>
        <div class="list-actions">
          <button class="btn btn-primary" @click="goToAddPlot">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            新增图斑
          </button>
        </div>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>图斑编号</th>
            <th>所属单元</th>
            <th>图斑面积（㎡）</th>
            <th>所属区划</th>
            <th>经度</th>
            <th>纬度</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in plotList" :key="item.ID">
            <td>{{ item.TBH }}</td>
            <td>{{ item.SSDY }}</td>
            <td>{{ item.TBMJ }}</td>
            <td>{{ item.SSQH }}</td>
            <td>{{ item.JD }}</td>
            <td>{{ item.WD }}</td>
            <td>{{ item.CJSJ ? item.CJSJ.split(' ')[0] : '' }}</td>
            <td>
              <div class="action-links">
                <span class="action-link" @click="viewDetail(item)">详情</span>
                <span class="action-link" @click="handleEdit(item)">编辑</span>
                <span class="action-link-delete" @click="handleDelete(item)">删除</span>
              </div>
            </td>
          </tr>
          <tr v-if="plotList.length === 0">
            <td colspan="8" class="empty-cell">暂无数据</td>
          </tr>
        </tbody>
      </table>

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
import { useRouter } from 'vue-router'
import { getPlotList, deletePlot } from '../api'

const router = useRouter()

const filterForm = reactive({
  keyword: '',
  ssqh: ''
})

const plotList = ref([])

const pagination = reactive({
  current: 1,
  total: 0,
  pageSize: 10,
  pages: [],
  get start() { return (this.current - 1) * this.pageSize + 1 },
  get end() { return Math.min(this.current * this.pageSize, this.total) },
  get totalPages() { return Math.ceil(this.total / this.pageSize) }
})

const fetchList = async () => {
  try {
    const params = {
      page: pagination.current,
      size: pagination.pageSize,
      keyword: filterForm.keyword || undefined,
      ssqh: filterForm.ssqh || undefined
    }
    const res = await getPlotList(params)
    if (res.data.code === 200) {
      plotList.value = res.data.data.list || []
      pagination.total = res.data.data.total || 0
      const totalPages = Math.ceil(pagination.total / pagination.pageSize)
      pagination.pages = Array.from({ length: Math.min(totalPages, 5) }, (_, i) => i + 1)
    }
  } catch (error) {
    console.error('获取地块列表失败:', error)
  }
}

const resetFilter = () => {
  filterForm.keyword = ''
  filterForm.ssqh = ''
  pagination.current = 1
  fetchList()
}

const handleQuery = () => {
  pagination.current = 1
  fetchList()
}

const viewDetail = (item) => {
  router.push(`/map/plot/detail/${item.ID}`)
}

const handleEdit = (item) => {
  console.log('编辑', item)
}

const handleDelete = async (item) => {
  if (!confirm(`确定删除图斑 ${item.TBH} 吗？`)) return
  try {
    await deletePlot(item.ID)
    alert('删除成功')
    fetchList()
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

const goToAddPlot = () => {
  router.push('/map/plot/add')
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
.form-select {
  width: 200px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238c8c8c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
  transition: all 0.3s;
}
.form-select:hover {
  border-color: #4096ff;
}
.form-select:focus {
  outline: none;
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
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
.list-actions {
  display: flex;
  gap: 12px;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th {
  background-color: #fafafa;
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
}
.data-table td {
  padding: 16px;
  font-size: 14px;
  color: #595959;
  border-bottom: 1px solid #f0f0f0;
}
.data-table tr:hover {
  background-color: #fafafa;
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
.action-link-delete {
  color: #ff4d4f;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}
.action-link-delete:hover {
  color: #ff7875;
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
.empty-cell {
  text-align: center;
  color: #8c8c8c;
  padding: 40px;
}
</style>
