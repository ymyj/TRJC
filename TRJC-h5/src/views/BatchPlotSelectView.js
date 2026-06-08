import { useRouter } from 'vue-router';

export const BatchPlotSelectView = {
  name: 'BatchPlotSelectView',
  props: {
    taskId: {
      type: [String, Number],
      default: null
    }
  },
  setup(props) {
    const router = useRouter();
    const plots = Vue.ref([]);
    const selectedPlotIds = Vue.ref(new Set());
    const loading = Vue.ref(true);

    const goBack = () => {
      router.push('/tasks');
    };

    const fetchPlots = async () => {
      try {
        loading.value = true;
        const taskId = props.taskId;
        if (!taskId) {
          vant.showToast({ message: '任务ID缺失', position: 'top' });
          router.push('/tasks');
          return;
        }
        const res = await TRJC.api.getTaskPlots(taskId);
        if (res.data.code === 200) {
          plots.value = (res.data.data || []).filter(p => p.status === 'transport');
        }
      } catch (error) {
        console.error('获取地块列表失败:', error);
        vant.showToast({ message: '获取地块列表失败', position: 'top' });
      } finally {
        loading.value = false;
      }
    };

    const toggleSelect = (plotId) => {
      if (selectedPlotIds.value.has(plotId)) {
        selectedPlotIds.value.delete(plotId);
      } else {
        selectedPlotIds.value.add(plotId);
      }
      selectedPlotIds.value = new Set(selectedPlotIds.value);
    };

    const isSelected = (plotId) => {
      return selectedPlotIds.value.has(plotId);
    };

    const selectAll = () => {
      if (selectedPlotIds.value.size === plots.value.length) {
        selectedPlotIds.value = new Set();
      } else {
        selectedPlotIds.value = new Set(plots.value.map(p => p.ID));
      }
      selectedPlotIds.value = new Set(selectedPlotIds.value);
    };

    const isAllSelected = Vue.computed(() => {
      return plots.value.length > 0 && selectedPlotIds.value.size === plots.value.length;
    });

    const hasNext = Vue.computed(() => {
      return selectedPlotIds.value.size > 0;
    });

    const goToNext = () => {
      const selectedPlots = plots.value.filter(p => selectedPlotIds.value.has(p.ID));
      import('../store/batchStore.js').then(({ batchStore }) => {
        batchStore.selectedPlots = selectedPlots;
        router.push({
          path: '/batch-sample-form',
          query: { taskId: props.taskId }
        });
      });
    };

    Vue.onMounted(() => {
      fetchPlots();
    });

    return {
      plots,
      selectedPlotIds,
      loading,
      goBack,
      toggleSelect,
      isSelected,
      selectAll,
      isAllSelected,
      hasNext,
      goToNext
    };
  },
  template: `
    <div class="batch-plot-select-view">
      <div class="batch-header">
        <div class="batch-header-back" @click="goBack">
          <van-icon name="arrow-left" size="20" color="#fff" />
        </div>
        <span class="batch-header-title">批量采集 - 选择地块</span>
      </div>
      
      <div class="batch-content">
        <div v-if="loading" class="loading-state">
          <van-loading size="24px">加载中...</van-loading>
        </div>
        
        <template v-else>
          <div class="select-all-bar" v-if="plots.length > 0">
            <van-checkbox :model-value="isAllSelected" @click="selectAll">全选</van-checkbox>
            <span class="select-hint">已选择 {{ selectedPlotIds.size }} / {{ plots.length }} 个地块</span>
          </div>
          
          <div class="plot-list">
            <div 
              v-for="plot in plots" 
              :key="plot.ID"
              class="plot-item"
              :class="{ selected: isSelected(plot.ID) }"
              @click="toggleSelect(plot.ID)"
            >
              <van-checkbox :model-value="isSelected(plot.ID)" />
              <div class="plot-info">
                <div class="plot-name">{{ plot.TBH || '地块' + plot.ID }}</div>
                <div class="plot-detail">图斑编号: {{ plot.TBH }}</div>
                <div class="plot-detail">面积: {{ plot.TBMJ }}㎡</div>
                <div class="plot-detail">区划: {{ plot.SSQH }}</div>
              </div>
              <van-icon name="success" size="20" color="#4A90E2" v-if="isSelected(plot.ID)" />
            </div>
          </div>
          
          <div v-if="plots.length === 0" class="empty-state">
            <van-icon name="warning-o" size="48" color="#DDD" />
            <p>当前任务下没有待运输状态的地块</p>
          </div>
        </template>
      </div>
      
      <div class="batch-bottom">
        <button class="next-btn" @click="goToNext" :disabled="!hasNext">
          下一步 ({{ selectedPlotIds.size }})
        </button>
      </div>
    </div>
  `
};

export const BatchPlotSelectViewStyle = `
.batch-plot-select-view {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 80px;
}

.batch-header {
  background: linear-gradient(135deg, #5B9FE8 0%, #4A90E2 50%, #3D7FD4 100%);
  padding: 16px;
  display: flex;
  align-items: center;
  position: relative;
  border-radius: 0 0 20px 20px;
}

.batch-header-back {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.batch-header-back:active {
  background: rgba(255, 255, 255, 0.2);
}

.batch-header-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin-right: 36px;
}

.batch-content {
  padding: 16px;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.select-all-bar {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.select-hint {
  font-size: 14px;
  color: #666;
}

.plot-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.plot-item {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.plot-item.selected {
  border-color: #4A90E2;
  background: #f0f7ff;
}

.plot-item:active {
  transform: scale(0.98);
}

.plot-info {
  flex: 1;
  min-width: 0;
}

.plot-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.plot-detail {
  font-size: 13px;
  color: #666;
  margin-bottom: 4px;
}

.plot-detail:last-child {
  margin-bottom: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #999;
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}

.batch-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 12px 16px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.next-btn {
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

.next-btn:disabled {
  background: #b3d1f2;
  cursor: not-allowed;
}

.next-btn:active:not(:disabled) {
  opacity: 0.9;
  transform: scale(0.98);
}
`;
