<template>
  <div>
    <div class="page-header">
      <button class="btn-back" @click="goBack">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
        返回
      </button>
      <h1 class="page-title">采样地块详情</h1>
    </div>

    <div class="detail-card">
      <!-- 标签页 -->
      <div class="tabs">
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'basic' }"
          @click="activeTab = 'basic'"
        >
          基本信息
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'survey' }"
          @click="activeTab = 'survey'"
        >
          勘察记录
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'sample' }"
          @click="activeTab = 'sample'"
        >
          样品采集记录
        </div>
      </div>

      <!-- 基本信息 -->
      <div v-if="activeTab === 'basic'" class="tab-content">
        <div class="info-grid">
          <div class="info-item">
            <label class="info-label">任务名称</label>
            <span class="info-value">{{ landInfo.taskName }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">图斑编号</label>
            <span class="info-value">{{ landInfo.code }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">所属单元</label>
            <span class="info-value">{{ landInfo.unit }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">图斑面积（㎡）</label>
            <span class="info-value">{{ landInfo.area }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">所属区划</label>
            <span class="info-value">{{ landInfo.district }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">经度</label>
            <span class="info-value">{{ landInfo.longitude }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">纬度</label>
            <span class="info-value">{{ landInfo.latitude }}</span>
          </div>
          <div class="info-item">
            <label class="info-label">状态</label>
            <span class="info-value">
              <span class="status-tag" :class="getStatusClass(landInfo.status)">{{ landInfo.statusText }}</span>
            </span>
          </div>
          <div class="info-item">
            <label class="info-label">采样人员</label>
            <span class="info-value">{{ landInfo.samplers }}</span>
          </div>
        </div>
      </div>

      <!-- 勘察记录 -->
      <div v-if="activeTab === 'survey'" class="tab-content">
        <table class="survey-table">
          <tbody>
            <tr>
              <td class="label-cell">项目名称</td>
              <td class="value-cell" colspan="3">{{ surveyRecord.projectName }}</td>
            </tr>
            <tr>
              <td class="label-cell">图斑编号</td>
              <td class="value-cell">{{ surveyRecord.code }}</td>
              <td class="label-cell">面积（㎡）</td>
              <td class="value-cell">{{ surveyRecord.area }}</td>
            </tr>
            <tr>
              <td class="label-cell">地理位置</td>
              <td class="value-cell" colspan="3">{{ surveyRecord.locationCity }} {{ surveyRecord.locationCounty }} {{ surveyRecord.locationVillage }}</td>
            </tr>
            <tr>
              <td class="label-cell">地理坐标</td>
              <td class="value-cell" colspan="3">经度：{{ surveyRecord.longitude }}　　纬度：{{ surveyRecord.latitude }}</td>
            </tr>
            <tr>
              <td class="label-cell">变更前土地利用类型</td>
              <td class="value-cell">{{ surveyRecord.beforeType }}</td>
              <td class="label-cell">变更时间</td>
              <td class="value-cell">{{ surveyRecord.changeTime }}</td>
            </tr>
            <tr>
              <td class="label-cell">利用类型</td>
              <td class="value-cell">{{ surveyRecord.useType }}</td>
              <td class="label-cell">有效土层厚度（cm）</td>
              <td class="value-cell">{{ surveyRecord.soilThickness }}</td>
            </tr>
            <tr>
              <td class="label-cell">侵入体类型及含量（%）</td>
              <td class="value-cell">{{ surveyRecord.intrusionType }}</td>
              <td class="label-cell">砾石含量（%）</td>
              <td class="value-cell">{{ surveyRecord.gravelContent }}</td>
            </tr>
            <tr>
              <td class="label-cell">地形坡度（°）</td>
              <td class="value-cell">{{ surveyRecord.slope }}</td>
              <td class="label-cell">田面平整程度</td>
              <td class="value-cell">{{ surveyRecord.flatness }}</td>
            </tr>
            <tr>
              <td class="label-cell">水资源保障条件</td>
              <td class="value-cell">{{ surveyRecord.waterCondition }}</td>
              <td class="label-cell">道路通行条件</td>
              <td class="value-cell">{{ surveyRecord.roadCondition }}</td>
            </tr>
            <tr>
              <td class="label-cell">地形部位</td>
              <td class="value-cell">{{ surveyRecord.terrain }}</td>
              <td class="label-cell">质地构型</td>
              <td class="value-cell">{{ surveyRecord.texture }}</td>
            </tr>
            <tr>
              <td class="label-cell">排水能力</td>
              <td class="value-cell">{{ surveyRecord.drainage }}</td>
              <td class="label-cell">海拔高度（m）</td>
              <td class="value-cell">{{ surveyRecord.altitude }}</td>
            </tr>
            <tr>
              <td class="label-cell">农田防护与生态环境保护水平</td>
              <td class="value-cell">{{ surveyRecord.protection }}</td>
              <td class="label-cell">耕层厚度（cm）</td>
              <td class="value-cell">{{ surveyRecord.plowThickness }}</td>
            </tr>
            <tr>
              <td class="label-cell">勘察日期</td>
              <td class="value-cell">{{ surveyRecord.surveyDate }}</td>
              <td class="label-cell">调查人员（签字）</td>
              <td class="value-cell">{{ surveyRecord.surveyor }}</td>
            </tr>
            <tr>
              <td class="label-cell">项目承担单位代表（签字）</td>
              <td class="value-cell">{{ surveyRecord.unitRep }}</td>
              <td class="label-cell">踏勘专家（签字）</td>
              <td class="value-cell">{{ surveyRecord.expert }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 样品采集记录 -->
      <div v-if="activeTab === 'sample'" class="tab-content">
        <table class="sample-table">
          <tbody>
            <tr>
              <td class="label-cell">土壤混合样品编号</td>
              <td class="value-cell" colspan="5">{{ sampleRecord.sampleCode }}</td>
            </tr>
            <tr>
              <td class="label-cell">地理位置</td>
              <td class="value-cell" colspan="5">{{ sampleRecord.locationCity }} {{ sampleRecord.locationCounty }} {{ sampleRecord.locationVillage }}</td>
            </tr>
            <tr>
              <td class="label-cell" rowspan="3">地理坐标</td>
              <td class="value-cell">{{ sampleRecord.point1Code }}</td>
              <td class="value-cell" colspan="4">经度：{{ sampleRecord.point1Lon }}　　纬度：{{ sampleRecord.point1Lat }}</td>
            </tr>
            <tr>
              <td class="value-cell">{{ sampleRecord.point2Code }}</td>
              <td class="value-cell" colspan="4">经度：{{ sampleRecord.point2Lon }}　　纬度：{{ sampleRecord.point2Lat }}</td>
            </tr>
            <tr>
              <td class="value-cell">{{ sampleRecord.point3Code }}</td>
              <td class="value-cell" colspan="4">经度：{{ sampleRecord.point3Lon }}　　纬度：{{ sampleRecord.point3Lat }}</td>
            </tr>
            <tr>
              <td class="label-cell" rowspan="3">采样深度（cm）</td>
              <td class="value-cell">{{ sampleRecord.depth1Code }}</td>
              <td class="value-cell" colspan="4"></td>
            </tr>
            <tr>
              <td class="value-cell">{{ sampleRecord.depth2Code }}</td>
              <td class="value-cell" colspan="4"></td>
            </tr>
            <tr>
              <td class="value-cell">{{ sampleRecord.depth3Code }}</td>
              <td class="value-cell" colspan="4"></td>
            </tr>
            <tr>
              <td class="label-cell">采样点位数量（个）</td>
              <td class="value-cell" colspan="2">{{ sampleRecord.pointCount }}</td>
              <td class="label-cell">混合样品重量（g）</td>
              <td class="value-cell" colspan="2">{{ sampleRecord.sampleWeight }}</td>
            </tr>
            <tr>
              <td class="label-cell">采样日期</td>
              <td class="value-cell" colspan="2">{{ sampleRecord.sampleDate }}</td>
              <td class="label-cell">采样人员（签字）</td>
              <td class="value-cell" colspan="2">{{ sampleRecord.sampler }}</td>
            </tr>
            <tr>
              <td class="label-cell">项目承担单位代表（签字）</td>
              <td class="value-cell" colspan="2">{{ sampleRecord.unitRep }}</td>
              <td class="label-cell">踏勘专家（签字）</td>
              <td class="value-cell" colspan="2">{{ sampleRecord.expert }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getSurveyRecords, getSampleRecords, getPlotDetail } from '../api'

const router = useRouter()
const route = useRoute()
const activeTab = ref('basic')

const landInfo = reactive({})
const surveyRecord = reactive({})
const sampleRecord = reactive({})

const statusMap = {
  pending: { text: '待领取', class: 'status-pending' },
  sampling: { text: '待采样', class: 'status-sampling' },
  transport: { text: '待运输', class: 'status-transport' },
  analysis: { text: '待分析', class: 'status-analysis' },
  completed: { text: '已完成', class: 'status-completed' }
}

const getStatusClass = (status) => {
  return statusMap[status]?.class || 'status-pending'
}

const fetchLandDetail = async () => {
  try {
    const landId = route.params.id
    const res = await getPlotDetail(landId)
    if (res.data.code === 200) {
      const data = res.data.data
      Object.assign(landInfo, {
        code: data.TBH,
        unit: data.SSDY,
        area: data.TBMJ,
        district: data.SSQH,
        longitude: data.JD,
        latitude: data.WD,
        status: data.ZT,
        statusText: statusMap[data.ZT]?.text || data.ZT,
        samplers: data.SYRY
      })
    }
  } catch (error) {
    console.error('获取地块详情失败:', error)
  }
}

const fetchSurveyRecords = async () => {
  try {
    const taskId = route.query.taskId || route.params.id
    const res = await getSurveyRecords(taskId)
    if (res.data.code === 200) {
      const list = res.data.data || []
      if (list.length > 0) {
        const data = list[0]
        const locationParts = (data.DLWZ || '').split(' ')
        Object.assign(surveyRecord, {
          projectName: data.XMMC,
          code: data.TBH,
          area: data.MJ,
          locationCity: locationParts[0] || '',
          locationCounty: locationParts[1] || '',
          locationVillage: locationParts.slice(2).join(' ') || '',
          longitude: data.DLZB_JD,
          latitude: data.DLZB_WD,
          beforeType: data.BGQ,
          changeTime: data.BGSJ,
          useType: data.LYLX,
          soilThickness: data.YXTCHD,
          intrusionType: data.QRLXJHL,
          gravelContent: data.LSHL,
          slope: data.DXPD,
          flatness: data.TMPZCD,
          waterCondition: data.SZBZTJ,
          roadCondition: data.DLTXTJ,
          terrain: data.DXBW,
          texture: data.ZDGX,
          drainage: data.PSNL,
          altitude: data.HBGD,
          protection: data.NTFH,
          plowThickness: data.GCHD,
          surveyDate: data.KCRQ,
          surveyor: data.DCRY,
          unitRep: data.XMDWDB,
          expert: data.TKZJ
        })
      }
    }
  } catch (error) {
    console.error('获取勘察记录失败:', error)
  }
}

const fetchSampleRecords = async () => {
  try {
    const taskId = route.query.taskId || route.params.id
    const res = await getSampleRecords(taskId)
    if (res.data.code === 200) {
      const list = res.data.data || []
      if (list.length > 0) {
        const data = list[0]
        const locationParts = (data.DLWZ || '').split(' ')
        Object.assign(sampleRecord, {
          sampleCode: data.TRHHYPBH,
          locationCity: locationParts[0] || '',
          locationCounty: locationParts[1] || '',
          locationVillage: locationParts.slice(2).join(' ') || '',
          point1Code: data.CYD1_BH,
          point1Lon: data.CYD1_JD,
          point1Lat: data.CYD1_WD,
          point2Code: data.CYD2_BH,
          point2Lon: data.CYD2_JD,
          point2Lat: data.CYD2_WD,
          point3Code: data.CYD3_BH,
          point3Lon: data.CYD3_JD,
          point3Lat: data.CYD3_WD,
          depth1Code: data.CYSD_D1,
          depth2Code: data.CYSD_D2,
          depth3Code: data.CYSD_D3,
          pointCount: data.CYDWSL,
          sampleWeight: data.HHYPSL,
          sampleDate: data.CYRQ,
          sampler: data.SYRY,
          unitRep: data.XMDWDB,
          expert: data.TKZJ
        })
      }
    }
  } catch (error) {
    console.error('获取样品采集记录失败:', error)
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchLandDetail()
  fetchSurveyRecords()
  fetchSampleRecords()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background-color: #fff;
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
}

.detail-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 标签页 */
.tabs {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fafafa;
}

.tab-item {
  padding: 14px 24px;
  font-size: 14px;
  color: #595959;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}

.tab-item:hover {
  color: #1677ff;
}

.tab-item.active {
  color: #1677ff;
  background-color: #fff;
  border-bottom-color: #1677ff;
  font-weight: 500;
}

/* 标签内容 */
.tab-content {
  padding: 24px;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 13px;
  color: #8c8c8c;
}

.info-value {
  font-size: 14px;
  color: #262626;
  font-weight: 500;
}

/* 状态标签 */
.status-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
}

.status-pending {
  background-color: #fff7e6;
  color: #fa8c16;
}

.status-sampling {
  background-color: #e6f7ff;
  color: #1890ff;
}

.status-transport {
  background-color: #f6ffed;
  color: #52c41a;
}

.status-analysis {
  background-color: #f9f0ff;
  color: #722ed1;
}

.status-completed {
  background-color: #f6ffed;
  color: #52c41a;
}

/* 勘察记录表格 */
.survey-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #d9d9d9;
}

.survey-table td {
  padding: 12px 16px;
  font-size: 14px;
  border: 1px solid #d9d9d9;
}

.survey-table .label-cell {
  background-color: #fafafa;
  color: #595959;
  font-weight: 500;
  text-align: center;
  width: 20%;
}

.survey-table .value-cell {
  color: #262626;
  text-align: center;
}

/* 样品采集记录表格 */
.sample-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #d9d9d9;
}

.sample-table td {
  padding: 12px 16px;
  font-size: 14px;
  border: 1px solid #d9d9d9;
}

.sample-table .label-cell {
  background-color: #fafafa;
  color: #595959;
  font-weight: 500;
  text-align: center;
  width: 16%;
}

.sample-table .value-cell {
  color: #262626;
  text-align: center;
}
</style>
