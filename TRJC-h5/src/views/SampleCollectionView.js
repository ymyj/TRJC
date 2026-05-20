export const SampleCollectionView = {
  name: 'SampleCollectionView',
  emits: ['navigate'],
  props: {
    taskId: {
      type: [String, Number],
      default: null
    }
  },
  setup(props, { emit }) {
    const formData = Vue.reactive({
      sampleCode: '',
      location: '',
      coordinates: '',
      depth: '',
      pointCount: '',
      weight: '',
      sampleDate: ''
    });

    const submitting = Vue.ref(false);

    const goBack = () => {
      emit('navigate', 'plot-detail');
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
      if (!formData.depth) {
        vant.showToast({ message: '请输入采样深度', position: 'top' });
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

      submitting.value = true;
      try {
        const taskId = props.taskId || '1';
        const payload = {
          RWID: parseInt(taskId),
          DKID: parseInt(taskId),
          TRHHYPBH: formData.sampleCode,
          DLWZ: formData.location,
          CYSD_D1: formData.depth,
          CYDWSL: parseInt(formData.pointCount),
          HHYPSL: parseFloat(formData.weight),
          CYRQ: formData.sampleDate
        };
        const res = await TRJC.api.createSampleRecord(taskId, payload);
        if (res.data.code === 200) {
          vant.showToast({ message: '提交成功', position: 'top' });
          resetForm();
          emit('navigate', 'plot-detail');
        }
      } catch (error) {
        console.error('提交失败:', error);
        vant.showToast({ message: '提交失败', position: 'top' });
      } finally {
        submitting.value = false;
      }
    };

    const resetForm = () => {
      formData.sampleCode = '';
      formData.location = '';
      formData.coordinates = '';
      formData.depth = '';
      formData.pointCount = '';
      formData.weight = '';
      formData.sampleDate = '';
    };

    return {
      formData,
      submitting,
      goBack,
      handleSubmit,
      resetForm
    };
  },
  template: `
    <div class="sample-collection-view">
      <div class="sample-collection-header">
        <div class="sample-collection-header-back" @click="goBack">
          <van-icon name="arrow-left" size="20" color="#fff" />
        </div>
        <span class="sample-collection-header-title">样品采集记录登记</span>
      </div>
      
      <div class="sample-collection-content">
        <div class="sample-collection-form-card">
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
          
          <div class="form-item">
            <label class="form-label">地理坐标</label>
            <input 
              type="text" 
              v-model="formData.coordinates"
              placeholder="按度分秒填写"
              class="form-input"
            />
          </div>
          
          <div class="form-row">
            <div class="form-item half">
              <label class="form-label">采样深度</label>
              <div class="input-with-unit">
                <input 
                  type="number" 
                  v-model="formData.depth"
                  placeholder="请输入"
                  class="form-input"
                />
                <span class="input-unit">cm</span>
              </div>
            </div>
            
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
          </div>
          
          <div class="form-item">
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
          
          <div class="form-item">
            <label class="form-label">采样日期</label>
            <input 
              type="date" 
              v-model="formData.sampleDate"
              class="form-input date-input"
            />
          </div>
        </div>
        
        <div class="form-instructions">
          <div class="instructions-title">填表说明</div>
          <ul class="instructions-list">
            <li>1. 土壤混合样品编号：县级行政区域代码(6位)+补充耕地类型(F复耕、K垦造)+采样日期(6位)+顺序号(3位)。如110101F250723001。</li>
            <li>2. 地理位置：所在市(州)、县(市、区)、乡(镇、街道)、村的名称。</li>
            <li>3. 地理坐标：按度分秒填写。</li>
            <li>4. 采样深度：单位为cm，保留整数位。</li>
            <li>5. 采样点位数量：单位为个。</li>
            <li>6. 混合样品重量：土壤混合样品重量，单位为g，保留整数位。</li>
            <li>7. 采样日期：填写年月日。</li>
            <li>8. 各地可根据实际细化修改补充耕地质量鉴定土壤混合样品采集记录表。</li>
          </ul>
        </div>
      </div>
      
      <div class="sample-collection-bottom">
        <button class="submit-btn" @click="handleSubmit" :disabled="submitting">{{ submitting ? '提交中...' : '提交' }}</button>
      </div>
    </div>
  `
};

export const SampleCollectionViewStyle = `
.sample-collection-view {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 80px;
}

.sample-collection-header {
  background: linear-gradient(135deg, #5B9FE8 0%, #4A90E2 50%, #3D7FD4 100%);
  padding: 16px;
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 0 0 20px 20px;
}

.sample-collection-header-back {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.sample-collection-header-back:active {
  background: rgba(255, 255, 255, 0.2);
}

.sample-collection-header-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin-right: 36px;
}

.sample-collection-content {
  padding: 16px;
}

.sample-collection-form-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 16px;
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

.sample-collection-bottom {
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
