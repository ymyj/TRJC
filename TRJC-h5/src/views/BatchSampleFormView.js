import { useRouter, useRoute } from 'vue-router';
import { batchStore } from '../store/batchStore.js';

export const BatchSampleFormView = {
  name: 'BatchSampleFormView',
  props: {
    taskId: {
      type: [String, Number],
      default: null
    }
  },
  setup(props) {
    const router = useRouter();
    const route = useRoute();
    const formData = Vue.reactive({
      sampleCode: '',
      location: '',
      pointCount: '',
      weight: '',
      sampleDate: '',
      sampler: '',
      unitRep: '',
      expert: ''
    });

    const plotData = Vue.ref([]);
    const submitting = Vue.ref(false);
    const taskObj = Vue.ref({});

    const goBack = () => {
      router.push('/batch-plot-select/' + (props.taskId || route.query.taskId));
    };

    const initPlotData = () => {
      const selectedPlots = batchStore.selectedPlots;
      if (!selectedPlots || selectedPlots.length === 0) {
        vant.showToast({ message: '未选择地块，请返回重新选择', position: 'top' });
        setTimeout(() => {
          router.push('/tasks');
        }, 1500);
        return;
      }
      plotData.value = selectedPlots.map(plot => ({
        DKID: plot.ID,
        name: plot.TBH || '地块' + plot.ID,
        coord_d1bh: '',
        coord_d1jd: '',
        coord_d1wd: '',
        depth: ''
      }));

    };

    const updatePlotField = (index, field, value) => {
      if (plotData.value[index]) {
        plotData.value[index][field] = value;
      }
    };

    const handleSubmit = async () => {
      if (!formData.sampleCode) {
        vant.showToast({ message: '请输入土壤混合样品编号', position: 'top' });
        return;
      }
      if (!formData.location) {
        vant.showToast({ message: '请输入地理位置', position: 'top' });
        return;
      }
      if (!formData.pointCount) {
        vant.showToast({ message: '请输入采样点位数量', position: 'top' });
        return;
      }
      if (!formData.weight) {
        vant.showToast({ message: '请输入混合样品重量', position: 'top' });
        return;
      }
      if (!formData.sampleDate) {
        vant.showToast({ message: '请选择采样日期', position: 'top' });
        return;
      }

      for (let i = 0; i < plotData.value.length; i++) {
        if (!plotData.value[i].coord_d1jd || !plotData.value[i].coord_d1wd) {
          vant.showToast({ message: `请填写第${i + 1}个地块的地理坐标`, position: 'top' });
          return;
        }
        if (!plotData.value[i].depth) {
          vant.showToast({ message: `请填写第${i + 1}个地块的采样深度`, position: 'top' });
          return;
        }
      }

      submitting.value = true;
      try {
        const taskId = props.taskId || route.query.taskId;
        const payload = {
          common: {
            TRHHYPBH: formData.sampleCode,
            DLWZ: formData.location,
            CYDWSL: parseInt(formData.pointCount),
            HHYPSL: parseFloat(formData.weight),
            CYRQ: formData.sampleDate,
            CYRY: formData.sampler || '',
            XMDWDB: formData.unitRep || '',
            TKZJ: formData.expert || ''
          },
          plots: plotData.value.map(pd => ({
            DKID: pd.DKID,
            DLZB_D1BH: pd.coord_d1bh,
            DLZB_D1JD: pd.coord_d1jd,
            DLZB_D1WD: pd.coord_d1wd,
            CYSD_D1: pd.depth
          }))
        };



        const res = await TRJC.api.createSampleRecordsBatch(taskId, payload);
        if (res.data.code === 200) {
          vant.showToast({ message: '批量提交成功', position: 'top' });
          batchStore.selectedPlots = [];
          setTimeout(() => {
            router.push('/tasks');
          }, 1500);
        }
      } catch (error) {
        console.error('批量提交失败:', error);
        vant.showToast({ message: '批量提交失败', position: 'top' });
      } finally {
        submitting.value = false;
      }
    };

    const resetForm = () => {
      formData.sampleCode = '';
      formData.location = '';
      formData.pointCount = '';
      formData.weight = '';
      formData.sampleDate = '';
      formData.sampler = '';
      formData.unitRep = '';
      formData.expert = '';
      initPlotData();
    };

    Vue.onMounted(() => {
      initPlotData();
    });

    return {
      formData,
      plotData,
      submitting,
      goBack,
      updatePlotField,
      handleSubmit,
      resetForm
    };
  },
  template: `
    <div class="batch-sample-form-view">
      <div class="batch-sample-header">
        <div class="batch-sample-header-back" @click="goBack">
          <van-icon name="arrow-left" size="20" color="#fff" />
        </div>
        <span class="batch-sample-header-title">批量采集 - 填写信息</span>
      </div>
      
      <div class="batch-sample-content">
        <div class="selected-plots-info">
          <div class="info-title">已选地块 ({{ plotData.length }}个)</div>
          <div class="plot-tags">
            <span v-for="(plot, index) in plotData" :key="plot.DKID" class="plot-tag">
              {{ index + 1 }}. {{ plot.name }}
            </span>
          </div>
        </div>
        
        <div class="sample-collection-form-card">
          <div class="form-section-title">通用信息</div>
          
          <div class="form-item">
            <label class="form-label">土壤混合样品编号</label>
            <input 
              type="text" 
              v-model="formData.sampleCode"
              placeholder="如：110101F250723001"
              class="form-input"
            />
            <span class="form-tip">县级行政区域代码(6位)+补充耕地类型(F复耕/K垦造)+采样日期(6位)+顺序号(3位)</span>
          </div>
          
          <div class="form-item">
            <label class="form-label">地理位置</label>
            <input 
              type="text" 
              v-model="formData.location"
              placeholder="所在市(州)、县(市、区)、乡(镇、街道)、村的名称"
              class="form-input"
            />
          </div>
          
          <div class="form-row">
            <div class="form-item half">
              <label class="form-label">采样点位数量</label>
              <div class="input-with-unit">
                <input 
                  type="number" 
                  v-model="formData.pointCount"
                  placeholder="请输入"
                  class="form-input"
                />
                <span class="input-unit">个</span>
              </div>
            </div>
            
            <div class="form-item half">
              <label class="form-label">混合样品重量</label>
              <div class="input-with-unit">
                <input 
                  type="number" 
                  v-model="formData.weight"
                  placeholder="请输入"
                  class="form-input"
                />
                <span class="input-unit">g</span>
              </div>
            </div>
          </div>
          
          <div class="form-item">
            <label class="form-label">采样日期</label>
            <input 
              type="date" 
              v-model="formData.sampleDate"
              class="form-input date-input"
            />
          </div>
          
          <div class="form-item">
            <label class="form-label">采样人员（签字）</label>
            <input 
              type="text" 
              v-model="formData.sampler"
              placeholder="请输入"
              class="form-input"
            />
          </div>
          
          <div class="form-item">
            <label class="form-label">项目承担单位代表（签字）</label>
            <input 
              type="text" 
              v-model="formData.unitRep"
              placeholder="请输入"
              class="form-input"
            />
          </div>
          
          <div class="form-item">
            <label class="form-label">踏勘专家（签字）</label>
            <input 
              type="text" 
              v-model="formData.expert"
              placeholder="请输入"
              class="form-input"
            />
          </div>
        </div>
        
        <div class="sample-collection-form-card">
          <div class="form-section-title">地块坐标与深度信息</div>
          <span class="form-tip">请为每个选中的地块填写地理坐标和采样深度</span>
          
          <div v-for="(plot, index) in plotData" :key="plot.DKID" class="plot-data-card">
            <div class="plot-data-header">
              <span class="plot-data-index">地块 {{ index + 1 }}</span>
              <span class="plot-data-name">{{ plot.name }}</span>
            </div>
            
            <div class="form-item">
              <label class="form-label">地理坐标</label>
              <div class="coord-row">
                <input 
                  type="text" 
                  v-model="plot.coord_d1bh"
                  placeholder="编号"
                  class="form-input coord-input-small"
                />
                <input 
                  type="text" 
                  v-model="plot.coord_d1jd"
                  placeholder="经度"
                  class="form-input coord-input"
                />
                <input 
                  type="text" 
                  v-model="plot.coord_d1wd"
                  placeholder="纬度"
                  class="form-input coord-input"
                />
              </div>
              <span class="form-tip">按度分秒填写，如：116°24′ 39°55′</span>
            </div>
            
            <div class="form-item">
              <label class="form-label">采样深度</label>
              <div class="input-with-unit">
                <input 
                  type="number" 
                  :value="plot.depth"
                  @input="updatePlotField(index, 'depth', $event.target.value)"
                  placeholder="请输入"
                  class="form-input"
                />
                <span class="input-unit">cm</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="form-instructions">
          <div class="instructions-title">填表说明</div>
          <ul class="instructions-list">
            <li>1. 土壤混合样品编号：县级行政区域代码(6位)+补充耕地类型(F复耕、K垦造)+采样日期(6位)+顺序号(3位)。</li>
            <li>2. 地理位置：所在市(州)、县(市、区)、乡(镇、街道)、村的名称。</li>
            <li>3. 地理坐标：按度分秒填写。</li>
            <li>4. 采样深度：单位为cm，保留整数位。</li>
            <li>5. 混合样品重量：土壤混合样品重量，单位为g，保留整数位。</li>
          </ul>
        </div>
      </div>
      
      <div class="batch-sample-bottom">
        <button class="submit-btn" @click="handleSubmit" :disabled="submitting">{{ submitting ? '提交中...' : '批量提交' }}</button>
      </div>
    </div>
  `
};

export const BatchSampleFormViewStyle = `
.batch-sample-form-view {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 80px;
}

.batch-sample-header {
  background: linear-gradient(135deg, #5B9FE8 0%, #4A90E2 50%, #3D7FD4 100%);
  padding: 16px;
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 0 0 20px 20px;
}

.batch-sample-header-back {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.batch-sample-header-back:active {
  background: rgba(255, 255, 255, 0.2);
}

.batch-sample-header-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin-right: 36px;
}

.batch-sample-content {
  padding: 16px;
}

.selected-plots-info {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.info-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.plot-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.plot-tag {
  display: inline-block;
  background: #e3f2fd;
  color: #1565c0;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 13px;
}

.sample-collection-form-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px;
}

.form-section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.form-item {
  margin-bottom: 16px;
}

.form-item.half {
  flex: 1;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  background: #fafafa;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #4A90E2;
  background: #fff;
}

.form-input::placeholder {
  color: #999;
}

.date-input {
  color: #333;
}

.input-with-unit {
  display: flex;
  align-items: center;
  position: relative;
}

.input-with-unit .form-input {
  padding-right: 50px;
}

.input-unit {
  position: absolute;
  right: 12px;
  font-size: 14px;
  color: #666;
}

.form-tip {
  display: block;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.coord-row {
  display: flex;
  gap: 8px;
}

.coord-input-small {
  width: 80px;
  flex-shrink: 0;
}

.coord-input {
  flex: 1;
}

.plot-data-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid #e8e8e8;
}

.plot-data-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e0e0e0;
}

.plot-data-index {
  font-size: 14px;
  font-weight: 600;
  color: #4A90E2;
  background: #e3f2fd;
  padding: 4px 12px;
  border-radius: 12px;
}

.plot-data-name {
  font-size: 14px;
  color: #666;
}

.plot-data-card .form-item:last-child {
  margin-bottom: 0;
}

.form-instructions {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.instructions-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.instructions-list {
  margin: 0;
  padding-left: 20px;
}

.instructions-list li {
  font-size: 13px;
  color: #666;
  line-height: 1.8;
  margin-bottom: 8px;
}

.instructions-list li:last-child {
  margin-bottom: 0;
}

.batch-sample-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 12px 16px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.submit-btn {
  width: 100%;
  height: 44px;
  border: none;
  border-radius: 22px;
  font-size: 16px;
  font-weight: 500;
  color: #fff;
  background: #4A90E2;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:disabled {
  background: #b3d1f2;
  cursor: not-allowed;
}

.submit-btn:active:not(:disabled) {
  opacity: 0.9;
  transform: scale(0.98);
}
`;
