<template>
  <div class="plot-add-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <button class="btn-back" @click="goBack">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        返回
      </button>
      <h2 class="page-title">新增图斑</h2>
    </div>

    <!-- 表单区域 -->
    <div class="form-section">
      <div class="form-row">
        <div class="form-item">
          <label class="form-label">图斑编号<span class="required">*</span></label>
          <input type="text" class="form-input" placeholder="请输入图斑编号" v-model="form.plotNumber">
        </div>
        <div class="form-item">
          <label class="form-label">所属单元<span class="required">*</span></label>
          <input type="text" class="form-input" placeholder="请输入所属单元" v-model="form.unit">
        </div>
      </div>

      <div class="form-row">
        <div class="form-item">
          <label class="form-label">所属区划<span class="required">*</span></label>
          <select class="form-select" v-model="form.district">
            <option value="">请选择所属区划</option>
            <option value="东城区">东城区</option>
            <option value="西城区">西城区</option>
            <option value="朝阳区">朝阳区</option>
            <option value="海淀区">海淀区</option>
            <option value="丰台区">丰台区</option>
          </select>
        </div>
        <div class="form-item">
          <label class="form-label">图斑面积<span class="required">*</span></label>
          <input type="text" class="form-input" placeholder="请输入图斑面积" v-model="form.area" readonly>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item">
          <label class="form-label">经度<span class="required">*</span></label>
          <input type="text" class="form-input" placeholder="请输入经度" v-model="form.longitude" readonly>
        </div>
        <div class="form-item">
          <label class="form-label">纬度<span class="required">*</span></label>
          <input type="text" class="form-input" placeholder="请输入纬度" v-model="form.latitude" readonly>
        </div>
      </div>
    </div>

    <!-- 围栏地图区域 -->
    <div class="map-section">
      <div class="map-header">
        <div class="map-title-wrapper">
          <span class="map-title">围栏地图</span>
          <span class="map-tip">点击【绘制围栏】在地图中绘制多边形区域，双击完成绘制。</span>
        </div>
        <div class="map-actions">
          <div class="map-search-wrapper">
            <input type="text" class="map-search-input" placeholder="请输入城市名进行定位" v-model="searchKeyword" @keyup.enter="handleSearch">
            <button class="btn btn-search" @click="handleSearch">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              搜索
            </button>
          </div>
          <button class="btn btn-default" @click="clearDraw">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            清除绘制
          </button>
          <button class="btn btn-primary" @click="startDraw">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
              <polyline points="2 17 12 22 22 17"></polyline>
              <polyline points="2 12 12 17 22 12"></polyline>
            </svg>
            绘制围栏
          </button>
        </div>
      </div>
      <div class="map-container" ref="mapContainer">
        <div id="tianditu-map" class="tianditu-map"></div>
        <div v-if="!mapLoaded" class="map-loading">
          <div class="loading-spinner"></div>
          <p>地图加载中...</p>
        </div>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div class="form-footer">
      <button class="btn btn-default" @click="goBack">取消</button>
      <button class="btn btn-primary" @click="handleSubmit">确定</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { createPlot } from '../api'

const router = useRouter()
const mapContainer = ref(null)
const mapLoaded = ref(false)
const searchKeyword = ref('')

const form = reactive({
  plotNumber: '',
  unit: '',
  district: '',
  area: '',
  longitude: '',
  latitude: ''
})

let map = null
let polygonTool = null
let currentPolygon = null
let currentPoints = []

const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    alert('请输入要搜索的城市名称')
    return
  }
  if (!map) {
    alert('地图正在加载中，请稍后再试')
    return
  }
  
  const result = await searchPlace(searchKeyword.value.trim())
  if (result) {
    map.centerAndZoom(new T.LngLat(result.lng, result.lat), 10)
  }
}

const searchPlace = async (keyword) => {
  try {
    const url = 'https://api.tianditu.gov.cn/geocoder?ds={"keyWord":"' + keyword + '"}&tk=d5cbd0c27896bb8f535dc57ecef2718c'
    
    const response = await fetch(url)
    const data = await response.json()
    
    if (data.status === '0' && data.location) {
      return {
        lng: parseFloat(data.location.lon),
        lat: parseFloat(data.location.lat),
        name: keyword
      }
    } else {
      alert(`未找到 "${keyword}" 相关地点，请尝试输入其他城市名称`)
      return null
    }
  } catch (error) {
    console.error('搜索请求失败:', error)
    alert('搜索失败，请检查网络连接')
    return null
  }
}

const initMap = () => {
  if (typeof T === 'undefined') {
    const script = document.createElement('script')
    script.src = 'https://api.tianditu.gov.cn/api?v=4.0&tk=d5cbd0c27896bb8f535dc57ecef2718c'
    script.onload = () => {
      createMap()
    }
    script.onerror = () => {
      console.error('天地图加载失败')
      showFallbackMap()
    }
    document.head.appendChild(script)
  } else {
    createMap()
  }
}

const createMap = () => {
  try {
    map = new T.Map('tianditu-map')
    map.centerAndZoom(new T.LngLat(116.4074, 39.9042), 12)
    const vecLayer = new T.TileLayer(
      'https://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=d5cbd0c27896bb8f535dc57ecef2718c',
      { minZoom: 1, maxZoom: 18 }
    )
    map.addLayer(vecLayer)
    const cvaLayer = new T.TileLayer(
      'https://t0.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=d5cbd0c27896bb8f535dc57ecef2718c',
      { minZoom: 1, maxZoom: 18 }
    )
    map.addLayer(cvaLayer)
    map.addControl(new T.Control.Zoom())
    map.addControl(new T.Control.Scale())
    initPolygonTool()
    mapLoaded.value = true
  } catch (error) {
    console.error('地图初始化失败:', error)
    showFallbackMap()
  }
}

const initPolygonTool = () => {
  if (!map) return
  const config = {
    showLabel: true,
    color: '#1677ff',
    weight: 3,
    opacity: 0.8,
    fillColor: '#1677ff',
    fillOpacity: 0.3
  }
  polygonTool = new T.PolygonTool(map, config)
  polygonTool.addEventListener('draw', (e) => {
    currentPolygon = e.currentPolygon
    currentPoints = e.currentLnglats
    if (currentPoints && currentPoints.length > 0) {
      let sumLng = 0, sumLat = 0
      currentPoints.forEach(point => {
        sumLng += point.lng
        sumLat += point.lat
      })
      form.longitude = (sumLng / currentPoints.length).toFixed(6)
      form.latitude = (sumLat / currentPoints.length).toFixed(6)
      const area = calculateArea(currentPoints)
      form.area = area.toFixed(2)
    }
    polygonTool.close()
  })
}

const calculateArea = (points) => {
  if (points.length < 3) return 0
  let area = 0
  const n = points.length
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n
    area += points[i].lng * points[j].lat
    area -= points[j].lng * points[i].lat
  }
  area = Math.abs(area) * 111000 * 111000 / 2
  return area
}

const showFallbackMap = () => {
  const container = document.getElementById('tianditu-map')
  if (container) {
    container.innerHTML = `
      <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #f5f5f5; color: #999;">
        <div style="text-align: center;">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1" style="margin-bottom: 16px;">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
          <p>地图服务暂时不可用</p>
          <p style="font-size: 12px; margin-top: 8px;">请检查网络连接或稍后重试</p>
        </div>
      </div>
    `
  }
  mapLoaded.value = true
}

const startDraw = () => {
  if (!polygonTool) {
    alert('地图正在加载中，请稍后再试')
    return
  }
  if (currentPolygon) {
    map.removeOverLay(currentPolygon)
    currentPolygon = null
    currentPoints = []
  }
  polygonTool.open()
}

const clearDraw = () => {
  if (currentPolygon && map) {
    map.removeOverLay(currentPolygon)
    currentPolygon = null
    currentPoints = []
  }
  form.area = ''
  form.longitude = ''
  form.latitude = ''
}

const goBack = () => {
  router.push('/map')
}

const handleSubmit = async () => {
  if (!form.plotNumber) {
    alert('请输入图斑编号')
    return
  }
  if (!form.unit) {
    alert('请输入所属单元')
    return
  }
  if (!form.district) {
    alert('请选择所属区划')
    return
  }
  if (!form.area) {
    alert('请在地图上绘制围栏')
    return
  }

  const data = {
    TBH: form.plotNumber,
    SSDY: form.unit,
    SSQH: form.district,
    TBMJ: parseFloat(form.area),
    JD: parseFloat(form.longitude),
    WD: parseFloat(form.latitude),
    WLZB: currentPoints.map(p => ({ lng: p.lng, lat: p.lat }))
  }

  try {
    const res = await createPlot(data)
    if (res.data.code === 200) {
      alert('保存成功')
      goBack()
    } else {
      alert('保存失败: ' + (res.data.message || '未知错误'))
    }
  } catch (error) {
    console.error('提交失败:', error)
    alert('保存失败: ' + (error.message || '网络错误'))
  }
}

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.clearOverLays()
    map = null
  }
})
</script>

<style scoped>
.plot-add-page {
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background: #fff;
  color: #595959;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-back:hover {
  border-color: #4096ff;
  color: #4096ff;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.form-section {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}

.required {
  color: #ff4d4f;
  margin-left: 4px;
}

.form-input,
.form-select {
  height: 40px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
  transition: all 0.3s;
}

.form-input[readonly] {
  background-color: #f5f5f5;
  color: #8c8c8c;
}

.form-input:hover,
.form-select:hover {
  border-color: #4096ff;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}

.form-input::placeholder {
  color: #bfbfbf;
}

.form-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238c8c8c' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 32px;
}

.map-section {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.map-title-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.map-title {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
}

.map-tip {
  font-size: 13px;
  color: #8c8c8c;
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  padding: 4px 12px;
  border-radius: 4px;
}

.map-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.map-search-wrapper {
  display: flex;
  gap: 8px;
}

.map-search-input {
  width: 220px;
  height: 36px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 14px;
  color: #262626;
  background-color: #fff;
  transition: all 0.3s;
}

.map-search-input:hover {
  border-color: #4096ff;
}

.map-search-input:focus {
  outline: none;
  border-color: #1677ff;
  box-shadow: 0 0 0 2px rgba(22, 119, 255, 0.1);
}

.map-search-input::placeholder {
  color: #bfbfbf;
}

.btn-search {
  height: 36px;
  padding: 0 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #1677ff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background-color: #fff;
  color: #1677ff;
}

.btn-search:hover {
  background-color: #1677ff;
  color: #fff;
}

.map-container {
  width: 100%;
  height: 500px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.tianditu-map {
  width: 100%;
  height: 100%;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #8c8c8c;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e8e8e8;
  border-top-color: #1677ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.form-footer {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn {
  height: 40px;
  padding: 0 24px;
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
</style>
