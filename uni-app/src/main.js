import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import VCharts from 'v-charts';
import AFTableColumn from 'af-table-column'  // el-table-column自适应宽度
import VueClipboard from 'vue-clipboard2'  // 复制内容到粘贴板

Vue.config.productionTip = false

App.mpType = 'app'

const app = new Vue({
  ...App
})
app.$mount()
