<template>
  <Teleport to="body">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <h3 class="modal-title">数据集详情</h3>
          <button class="modal-close" @click="close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-table">
            <div class="detail-row">
              <div class="detail-label">任务名称</div>
              <div class="detail-value">{{ data.taskName }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">图斑编号</div>
              <div class="detail-value">{{ data.plotNumber }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">经度</div>
              <div class="detail-value">{{ data.longitude }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">纬度</div>
              <div class="detail-value">{{ data.latitude }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">采样日期</div>
              <div class="detail-value">{{ data.sampleDate }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">地形部位</div>
              <div class="detail-value">{{ data.terrain }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">有效土层厚度(cm)</div>
              <div class="detail-value">{{ data.soilThickness }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">耕层质地</div>
              <div class="detail-value">{{ data.soilTexture }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">容重(g/cm³)</div>
              <div class="detail-value">{{ data.bulkDensity }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">质地构型</div>
              <div class="detail-value">{{ data.textureStructure }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">生物多样性</div>
              <div class="detail-value">{{ data.biodiversity }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">农田林网化程度</div>
              <div class="detail-value">{{ data.forestNetwork }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">障碍因素</div>
              <div class="detail-value">{{ data.obstacleFactor }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">灌溉能力</div>
              <div class="detail-value">{{ data.irrigationCapacity }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">排水能力</div>
              <div class="detail-value">{{ data.drainageCapacity }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">pH值</div>
              <div class="detail-value">{{ data.phValue }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">有机质(g/kg)</div>
              <div class="detail-value">{{ data.organicMatter || '30.5' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">有效磷(mg/kg)</div>
              <div class="detail-value">{{ data.availablePhosphorus || '29.6' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">速效钾(mg/kg)</div>
              <div class="detail-value">{{ data.availablePotassium || '236' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">水溶性盐总量(g/kg)</div>
              <div class="detail-value">{{ data.solubleSalt || '0.7' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">地类名称</div>
              <div class="detail-value">{{ data.landType || '旱地' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">清洁程度</div>
              <div class="detail-value">{{ data.cleanliness || '清洁' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">备注</div>
              <div class="detail-value">{{ data.remark || '-' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">镉(mg/kg)</div>
              <div class="detail-value">{{ data.cadmium || '0.08' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">总汞(mg/kg)</div>
              <div class="detail-value">{{ data.totalMercury || '0.094' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">总砷(mg/kg)</div>
              <div class="detail-value">{{ data.totalArsenic || '5.41' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">铅(mg/kg)</div>
              <div class="detail-value">{{ data.lead || '25.1' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">铬(mg/kg)</div>
              <div class="detail-value">{{ data.chromium || '64' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">耕地质量等级</div>
              <div class="detail-value">{{ data.qualityGrade || '0.883351664' }}</div>
            </div>
            <div class="detail-row">
              <div class="detail-label">质量分级</div>
              <div class="detail-value">{{ data.qualityLevel || '三等' }}</div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-default" @click="close">关闭</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  data: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:visible'])

const close = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background-color: #fff;
  border-radius: 8px;
  width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8c8c8c;
  border-radius: 4px;
  transition: all 0.3s;
}

.modal-close:hover {
  background-color: #f5f5f5;
  color: #595959;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}

.detail-table {
  width: 100%;
}

.detail-row {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  width: 180px;
  padding: 12px 16px;
  background-color: #fafafa;
  font-size: 14px;
  color: #595959;
  font-weight: 500;
  border-right: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.detail-value {
  flex: 1;
  padding: 12px 16px;
  font-size: 14px;
  color: #262626;
  word-break: break-all;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
}

.btn {
  height: 36px;
  padding: 0 20px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
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
</style>
