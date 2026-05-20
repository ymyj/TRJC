import { UserHeader, UserHeaderStyle } from './components/UserHeader.js';
import { TaskStats, TaskStatsStyle } from './components/TaskStats.js';
import { TaskItem, TaskItemStyle } from './components/TaskItem.js';
import { HomeView, HomeViewStyle } from './views/HomeView.js';
import { SampleCollectionView, SampleCollectionViewStyle } from './views/SampleCollectionView.js';
import * as api from './api/index.js';

const { createApp, ref } = Vue;

window.TRJC = { api };

const app = createApp({
  components: {
    UserHeader,
    TaskStats,
    TaskItem,
    HomeView,
    SampleCollectionView
  },
  setup() {
    const currentView = ref('home');

    const navigate = (viewName) => {
      currentView.value = viewName;
    };

    return {
      currentView,
      navigate
    };
  },
  template: `
    <div id="app">
      <home-view v-if="currentView === 'home'" @navigate="navigate" />
      <sample-collection-view v-else-if="currentView === 'sample-collection'" :task-id="1" @navigate="navigate" />
    </div>
  `
});

app.use(vant);

app.mount('#app');

const styles = [
  UserHeaderStyle,
  TaskStatsStyle,
  TaskItemStyle,
  HomeViewStyle,
  SampleCollectionViewStyle
];

const styleElement = document.createElement('style');
styleElement.textContent = styles.join('\n');
document.head.appendChild(styleElement);
