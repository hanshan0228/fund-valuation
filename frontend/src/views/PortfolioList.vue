<template>
  <div class="portfolio-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>组合列表</span>
          <el-button type="primary" @click="showCreateDialog = true">
            <el-icon><Plus /></el-icon>
            创建组合
          </el-button>
        </div>
      </template>

      <el-table :data="store.portfolios" v-loading="store.loading">
        <el-table-column prop="name" label="组合名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewPortfolio(row.id)">
              查看详情
            </el-button>
            <el-button type="danger" size="small" @click="deletePortfolio(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建组合对话框 -->
    <el-dialog v-model="showCreateDialog" title="创建组合" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="组合名称" required>
          <el-input v-model="form.name" placeholder="请输入组合名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            placeholder="请输入描述"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createPortfolio">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePortfolioStore } from '../stores/portfolio'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const router = useRouter()
const store = usePortfolioStore()

const showCreateDialog = ref(false)
const form = ref({
  name: '',
  description: ''
})

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const viewPortfolio = (id) => {
  router.push(`/portfolios/${id}`)
}

const createPortfolio = async () => {
  if (!form.value.name) {
    ElMessage.warning('请输入组合名称')
    return
  }

  try {
    await store.createPortfolio(form.value)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    form.value = { name: '', description: '' }
  } catch (error) {
    ElMessage.error(error.message)
  }
}

const deletePortfolio = async (portfolio) => {
  try {
    await ElMessageBox.confirm(`确定要删除组合 "${portfolio.name}" 吗？`, '确认删除', {
      type: 'warning'
    })
    await store.deletePortfolio(portfolio.id)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message)
    }
  }
}

onMounted(() => {
  store.fetchPortfolios()
})
</script>

<style scoped>
.portfolio-list {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
