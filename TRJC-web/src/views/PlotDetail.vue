<template>
  <div class="plot-detail-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <button class="btn-back" @click="goBack">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        返回
      </button>
      <h2 class="page-title">图斑详情</h2>
    </div>

    <!-- 表单区域 -->
    <div class="form-section">
      <div class="form-row">
        <div class="form-item">
          <label class="form-label">图斑编号</label>
          <div class="form-value">{{ form.plotNumber }}</div>
        </div>
        <div class="form-item">
          <label class="form-label">所属单元</label>
          <div class="form-value">{{ form.unit }}</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item">
          <label class="form-label">所属区划</label>
          <div class="form-value">{{ form.district }}</div>
        </div>
        <div class="form-item">
          <label class="form-label">图斑面积</label>
          <div class="form-value">{{ form.area }} ㎡</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item">
          <label class="form-label">经度</label>
          <div class="form-value">{{ form.longitude }}</div>
        </div>
        <div class="form-item">
          <label class="form-label">纬度</label>
          <div class="form-value">{{ form.latitude }}</div>
        </div>
      </div>

      <div class="form-row">
        <div class="form-item">
          <label class="form-label">创建时间</label>
          <div class="form-value">{{ form.createTime }}</div>
        </div>
        <div class="form-item">
          <label class="form-label">创建人</label>
          <div class="form-value">{{ form.creator }}</div>
        </div>
      </div>
    </div>

    <!-- 围栏地图区域 -->
    <div class="map-section">
      <div class="map-header">
        <div class="map-title-wrapper">
          <span class="map-title">围栏地图</span>
          <span class="map-tip">图斑围栏范围展示</span>
        </div>
      </div>
      <div class="map-container" ref="mapContainer">
        <div id="tianditu-map-detail" class="tianditu-map"></div>
        <div v-if="!mapLoaded" class="map-loading">
          <div class="loading-spinner"></div>
          <p>地图加载中...</p>
        </div>
      </div>
    </div>

    <!-- 底部按钮 -->
    <div class="form-footer">
      <button class="btn btn-default" @click="goBack">返回</button>
      <button class="btn btn-primary" @click="handleEdit">编辑</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPlotDetail } from '../api'

const router = useRouter()
const route = useRoute()
const mapContainer = ref(null)
const mapLoaded = ref(false)

const form = reactive({
  plotNumber: '',
  unit: '',
  district: '',
  area: '',
  longitude: '',
  latitude: '',
  createTime: '',
  creator: ''
})

let map = null
let polygon = null

const fetchPlotDetail = async () => {
  try {
    const plotId = route.params.id
    const res = await getPlotDetail(plotId)
    if (res.data.code === 200) {
      const data = res.data.data
      Object.assign(form, {
        plotNumber: data.TBBH,
        unit: data.SSDY,
        district: data.SSQH,
        area: data.TBmj,
        longitude: data.JD,
        latitude: data.WD,
        createTime: data.CJSJ,
        creator: data.CJR
      })
      if (data.fence_points && data.fence_points.length > 0) {
        fencePoints.length = 0
        data.fence_points.forEach(point => {
          fencePoints.push({ lng: point.lng, lat: point.lat })
        })
      }
      initMap()
    }
  } catch (error) {
    console.error('获取图斑详情失败:', error)
  }
}

const fencePoints = []

const initMap = () => {
  if (typeof T === 'undefined') {
    const script = document.createElement('script')
    script.src = 'https://api.tianditu.gov.cn/api?v=4.0&tk=174705aebfe31b79b3587279e211cb9a'
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
    map = new T.Map('tianditu-map-detail')
    const centerLng = parseFloat(form.longitude)
    const centerLat = parseFloat(form.latitude)
    map.centerAndZoom(new T.LngLat(centerLng, centerLat), 15)
    const vecLayer = new T.TileLayer(
      'https://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=174705aebfe31b79b3587279e211cb9a',
      { minZoom: 1, maxZoom: 18 }
    )
    map.addLayer(vecLayer)
    const cvaLayer = new T.TileLayer(
      'https://t0.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=174705aebfe31b79b3587279e211cb9a',
      { minZoom: 1, maxZoom: 18 }
    )
    map.addLayer(cvaLayer)
    map.addControl(new T.Control.Zoom())
    map.addControl(new T.Control.Scale())
    drawFence()
    mapLoaded.value = true
  } catch (error) {
    console.error('地图初始化失败:', error)
    showFallbackMap()
  }
}

const drawFence = () => {
  if (!map || fencePoints.length === 0) return
  const points = fencePoints.map(point => new T.LngLat(point.lng, point.lat))
  polygon = new T.Polygon(points, {
    color: '#1677ff',
    weight: 3,
    opacity: 0.8,
    fillColor: '#1677ff',
    fillOpacity: 0.3
  })
  map.addOverLay(polygon)
  const centerLng = parseFloat(form.longitude)
  const centerLat = parseFloat(form.latitude)
  const marker = new T.Marker(new T.LngLat(centerLng, centerLat))
  map.addOverLay(marker)
  const infoWindow = new T.InfoWindow({
    content: `<div style="padding: 8px;">
      <div style="font-weight: 600; margin-bottom: 4px;">${form.plotNumber}</div>
      <div style="font-size: 12px; color: #666;">面积: ${form.area} ㎡</div>
    </div>`,
    offset: new T.Point(0, -20)
  })
  marker.addEventListener('click', () => {
    marker.openInfoWindow(infoWindow)
  })
}

const showFallbackMap = () => {
  const container = document.getElementById('tianditu-map-detail')
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

const goBack = () => {
  router.push('/map')
}

const handleEdit = () => {
  const plotId = route.params.id
  router.push(`/map/plot/edit/${plotId}`)
}

onMounted(() => {
  fetchPlotDetail()
})

onUnmounted(() => {
  if (map) {
    map.clearOverLays()
    map = null
  }
})
</script>

<style scoped>
.plot-detail-page {
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
  color: #8c8c8c;
  font-weight: 500;
}

.form-value {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
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
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  padding: 4px 12px;
  border-radius: 4px;
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
