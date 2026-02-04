<template>
  <div class="upload-ocr" v-loading="recognizing" element-loading-text="正在识别中，请稍候..." element-loading-background="rgba(255, 255, 255, 0.8)">
    <el-card>
      <template #header>
        <span>OCR识别 - 上传支付宝基金截图</span>
      </template>

      <!-- 上传区域 -->
      <el-upload
        class="upload-area"
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        :show-file-list="false"
        accept="image/*"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 jpg/png 格式的支付宝基金持仓截图
          </div>
        </template>
      </el-upload>

      <!-- 识别结果 -->
      <div v-if="ocrResults.length > 0" class="results-section">
        <el-divider>识别结果</el-divider>

        <el-alert type="info" :closable="false" style="margin-bottom: 15px;">
          共识别到 <strong>{{ ocrResults.length }}</strong> 只基金，请仔细核对后选择组合导入
        </el-alert>

        <el-table :data="ocrResults" border>
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="fund_code" label="基金代码" width="100">
            <template #default="{ row }">
              <el-input v-model="row.fund_code" size="small" :class="{ 'is-empty': !row.fund_code }" />
            </template>
          </el-table-column>
          <el-table-column prop="fund_name" label="基金名称" width="200">
            <template #default="{ row }">
              <el-input v-model="row.fund_name" size="small" placeholder="可留空" />
            </template>
          </el-table-column>
          <el-table-column prop="amount" label="持仓金额" width="150">
            <template #default="{ row }">
              <el-input-number
                v-model="row.amount"
                :precision="2"
                :min="0"
                size="small"
                style="width: 100%"
              />
            </template>
          </el-table-column>
          <el-table-column prop="shares" label="持仓份额" width="150">
            <template #default="{ row }">
              <el-input-number
                v-model="row.shares"
                :precision="2"
                :min="0"
                size="small"
                style="width: 100%"
              />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ $index }">
              <el-button type="danger" size="small" @click="removeResult($index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="import-section">
          <el-select v-model="selectedPortfolio" placeholder="选择组合" style="width: 300px;">
            <el-option
              v-for="portfolio in portfolios"
              :key="portfolio.id"
              :label="portfolio.name"
              :value="portfolio.id"
            />
          </el-select>
          <el-button type="primary" @click="importToPortfolio" :loading="importing">
            导入到组合
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ocrAPI, portfolioAPI, holdingAPI } from '../api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const ocrResults = ref([])
const portfolios = ref([])
const selectedPortfolio = ref(null)
const importing = ref(false)
const recognizing = ref(false)

const handleFileChange = async (file) => {
  try {
    recognizing.value = true
    const result = await ocrAPI.uploadFile(file.raw)

    if (result.success && result.data.length > 0) {
      ocrResults.value = result.data
      ElMessage.success(`识别成功，共识别到 ${result.count} 只基金`)
    } else {
      ElMessage.warning('未识别到基金信息，请检查图片')
    }
  } catch (error) {
    ElMessage.error('OCR识别失败: ' + error.message)
  } finally {
    recognizing.value = false
  }
}

const removeResult = (index) => {
  ocrResults.value.splice(index, 1)
}

const importToPortfolio = async () => {
  if (!selectedPortfolio.value) {
    ElMessage.warning('请选择组合')
    return
  }

  if (ocrResults.value.length === 0) {
    ElMessage.warning('没有可导入的数据')
    return
  }

  // 验证数据
  for (const item of ocrResults.value) {
    if (!/^\d{6}$/.test(item.fund_code)) {
      ElMessage.error(`基金代码 ${item.fund_code} 格式不正确`)
      return
    }
    if (item.amount <= 0 || item.shares <= 0) {
      ElMessage.error(`基金 ${item.fund_code} 的金额或份额必须大于0`)
      return
    }
  }

  try {
    importing.value = true
    const result = await holdingAPI.batchCreate(
      selectedPortfolio.value,
      ocrResults.value
    )
    ElMessage.success(`导入成功：新增 ${result.created} 只，跳过 ${result.skipped} 只`)

    // 清空结果并跳转
    ocrResults.value = []
    router.push(`/portfolios/${selectedPortfolio.value}`)
  } catch (error) {
    ElMessage.error('导入失败: ' + error.message)
  } finally {
    importing.value = false
  }
}

onMounted(async () => {
  try {
    portfolios.value = await portfolioAPI.getAll()
  } catch (error) {
    ElMessage.error('获取组合列表失败')
  }
})
</script>

<style scoped>
.upload-ocr {
  max-width: 1000px;
  margin: 0 auto;
}

.upload-area {
  margin-bottom: 30px;
}

.results-section {
  margin-top: 30px;
}

.import-section {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  align-items: center;
}

:deep(.is-empty .el-input__wrapper) {
  background-color: #fef0f0;
  border-color: #f56c6c;
}
</style>
