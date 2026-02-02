import { defineStore } from 'pinia'
import { portfolioAPI, holdingAPI } from '../api'

export const usePortfolioStore = defineStore('portfolio', {
  state: () => ({
    portfolios: [],
    currentPortfolio: null,
    currentStats: null,
    loading: false,
    pollingInterval: null
  }),

  actions: {
    // 判断是否交易时间
    isTradingTime() {
      const now = new Date()
      const day = now.getDay()
      if (day === 0 || day === 6) return false

      const hour = now.getHours()
      const minute = now.getMinutes()
      const timeMinutes = hour * 60 + minute

      return timeMinutes >= 570 && timeMinutes <= 900 // 9:30-15:00
    },

    // 获取所有组合
    async fetchPortfolios() {
      try {
        this.loading = true
        this.portfolios = await portfolioAPI.getAll()
      } catch (error) {
        console.error('获取组合列表失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 创建组合
    async createPortfolio(data) {
      try {
        const portfolio = await portfolioAPI.create(data)
        this.portfolios.push(portfolio)
        return portfolio
      } catch (error) {
        console.error('创建组合失败:', error)
        throw error
      }
    },

    // 删除组合
    async deletePortfolio(id) {
      try {
        await portfolioAPI.delete(id)
        this.portfolios = this.portfolios.filter(p => p.id !== id)
      } catch (error) {
        console.error('删除组合失败:', error)
        throw error
      }
    },

    // 获取实时统计
    async fetchRealtimeStats(portfolioId) {
      try {
        this.loading = true
        this.currentStats = await portfolioAPI.getRealtimeStats(portfolioId)
      } catch (error) {
        console.error('获取实时统计失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 启动轮询
    startPolling(portfolioId) {
      // 清除已有轮询
      this.stopPolling()

      // 立即执行一次
      this.fetchRealtimeStats(portfolioId)

      // 设置定时轮询 (5分钟)
      this.pollingInterval = setInterval(() => {
        if (this.isTradingTime()) {
          this.fetchRealtimeStats(portfolioId)
        }
      }, 5 * 60 * 1000)
    },

    // 停止轮询
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval)
        this.pollingInterval = null
      }
    },

    // 手动刷新
    async refresh(portfolioId) {
      await this.fetchRealtimeStats(portfolioId)
    }
  }
})
