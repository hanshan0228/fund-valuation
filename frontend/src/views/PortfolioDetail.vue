<template>
  <div class="portfolio-detail">
    <el-card v-if="stats">
      <template #header>
        <div class="card-header">
          <span>{{ stats.portfolio_name }}</span>
          <div>
            <el-tag v-if="store.isTradingTime()" type="success">交易时间</el-tag>
            <el-tag v-else type="info">非交易时间</el-tag>
            <el-button type="primary" @click="refresh" :loading="store.loading">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <!-- 总览 -->
      <el-row :gutter="20" class="stats-summary">
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">总成本</div>
            <div class="value">¥{{ formatNumber(stats.total_cost) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">总市值</div>
            <div class="value">¥{{ formatNumber(stats.total_value) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">总收益</div>
            <div class="value" :class="getProfitClass(stats.total_profit)">
              {{ formatProfit(stats.total_profit) }}
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="label">收益率</div>
            <div class="value" :class="getProfitClass(stats.total_profit_rate)">
              {{ formatProfitRate(stats.total_profit_rate) }}
            </div>
          </div>
        </el-col>
      </el-row>

      <div class="update-time">
        更新时间: {{ stats.updated_at }}
      </div>

      <!-- 持仓列表 -->
      <el-table :data="stats.holdings" class="holdings-table">
        <el-table-column prop="fund_code" label="基金代码" width="100" />
        <el-table-column prop="fund_name" label="基金名称" min-width="200" />
        <el-table-column prop="shares" label="持仓份额" width="120">
          <template #default="{ row }">
            {{ formatNumber(row.shares) }}
          </template>
        </el-table-column>
        <el-table-column prop="cost_nav" label="成本净值" width="100">
          <template #default="{ row }">
            {{ formatNumber(row.cost_nav) }}
          </template>
        </el-table-column>
        <el-table-column prop="current_nav" label="当前净值" width="100">
          <template #default="{ row }">
            {{ formatNumber(row.current_nav) }}
          </template>
        </el-table-column>
        <el-table-column prop="value" label="持仓市值" width="120">
          <template #default="{ row }">
            ¥{{ formatNumber(row.value) }}
          </template>
        </el-table-column>
        <el-table-column prop="profit" label="收益" width="120">
          <template #default="{ row }">
            <span :class="getProfitClass(row.profit)">
              {{ formatProfit(row.profit) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="profit_rate" label="收益率" width="100">
          <template #default="{ row }">
            <span :class="getProfitClass(row.profit_rate)">
              {{ formatProfitRate(row.profit_rate) }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-empty v-else-if="!store.loading" description="暂无数据" />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePortfolioStore } from '../stores/portfolio'
import { ElMessage } from 'element-plus'
import { computed } from 'vue'

const route = useRoute()
const store = usePortfolioStore()

const portfolioId = computed(() => parseInt(route.params.id))
const stats = computed(() => store.currentStats)

const formatNumber = (num) => {
  if (!num) return '0.00'
  return parseFloat(num).toFixed(2)
}

const formatProfit = (num) => {
  if (!num) return '¥0.00'
  const value = parseFloat(num)
  return (value >= 0 ? '+' : '') + '¥' + value.toFixed(2)
}

const formatProfitRate = (num) => {
  if (!num) return '0.00%'
  const value = parseFloat(num)
  return (value >= 0 ? '+' : '') + value.toFixed(2) + '%'
}

const getProfitClass = (num) => {
  if (!num) return ''
  const value = parseFloat(num)
  return value > 0 ? 'profit-positive' : value < 0 ? 'profit-negative' : ''
}

const refresh = async () => {
  try {
    await store.refresh(portfolioId.value)
    ElMessage.success('刷新成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}

onMounted(() => {
  store.startPolling(portfolioId.value)
})

onUnmounted(() => {
  store.stopPolling()
})
</script>

<style scoped>
.portfolio-detail {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.stats-summary {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.stat-item .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-item .value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.update-time {
  text-align: right;
  color: #909399;
  font-size: 12px;
  margin-bottom: 15px;
}

.holdings-table {
  margin-top: 20px;
}

.profit-positive {
  color: #f56c6c;
}

.profit-negative {
  color: #67c23a;
}
</style>
