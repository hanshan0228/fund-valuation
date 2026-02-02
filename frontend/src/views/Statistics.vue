<template>
  <div class="statistics">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>历史收益统计</span>
          <div>
            <el-select v-model="selectedPortfolio" placeholder="选择组合" style="width: 200px; margin-right: 10px;">
              <el-option
                v-for="portfolio in portfolios"
                :key="portfolio.id"
                :label="portfolio.name"
                :value="portfolio.id"
              />
            </el-select>
            <el-select v-model="days" placeholder="天数" style="width: 120px; margin-right: 10px;">
              <el-option label="最近7天" :value="7" />
              <el-option label="最近30天" :value="30" />
              <el-option label="最近90天" :value="90" />
            </el-select>
            <el-button type="primary" @click="loadHistory" :loading="loading">
              查询
            </el-button>
          </div>
        </div>
      </template>

      <div v-if="historyData" class="chart-container">
        <div ref="chartRef" style="width: 100%; height: 500px;"></div>
      </div>

      <el-empty v-else-if="!loading" description="请选择组合并查询" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { portfolioAPI } from '../api'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const portfolios = ref([])
const selectedPortfolio = ref(null)
const days = ref(30)
const loading = ref(false)
const historyData = ref(null)
const chartRef = ref(null)
let chartInstance = null

const loadHistory = async () => {
  if (!selectedPortfolio.value) {
    ElMessage.warning('请选择组合')
    return
  }

  try {
    loading.value = true
    const result = await portfolioAPI.getHistoryStats(selectedPortfolio.value, days.value)
    historyData.value = result

    await nextTick()
    renderChart()
  } catch (error) {
    ElMessage.error('获取历史数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const renderChart = () => {
  if (!chartRef.value || !historyData.value) return

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  const dates = historyData.value.history.map(item => item.date)
  const totalValues = historyData.value.history.map(item => parseFloat(item.total_value))
  const cumulativeProfits = historyData.value.history.map(item => parseFloat(item.cumulative_profit))
  const cumulativeProfitRates = historyData.value.history.map(item => parseFloat(item.cumulative_profit_rate))

  const option = {
    title: {
      text: historyData.value.portfolio_name + ' 收益曲线',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['总市值', '累计收益', '收益率'],
      top: 30
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: [
      {
        type: 'value',
        name: '金额(元)',
        position: 'left'
      },
      {
        type: 'value',
        name: '收益率(%)',
        position: 'right'
      }
    ],
    series: [
      {
        name: '总市值',
        type: 'line',
        data: totalValues,
        smooth: true,
        itemStyle: { color: '#409eff' }
      },
      {
        name: '累计收益',
        type: 'line',
        data: cumulativeProfits,
        smooth: true,
        itemStyle: { color: '#67c23a' }
      },
      {
        name: '收益率',
        type: 'line',
        yAxisIndex: 1,
        data: cumulativeProfitRates,
        smooth: true,
        itemStyle: { color: '#f56c6c' }
      }
    ]
  }

  chartInstance.setOption(option)
}

onMounted(async () => {
  try {
    portfolios.value = await portfolioAPI.getAll()
    if (portfolios.value.length > 0) {
      selectedPortfolio.value = portfolios.value[0].id
    }
  } catch (error) {
    ElMessage.error('获取组合列表失败')
  }

  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})
</script>

<style scoped>
.statistics {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  margin-top: 20px;
}
</style>
