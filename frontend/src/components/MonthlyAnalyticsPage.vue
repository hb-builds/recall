<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="reports"
      @navigate="onNav"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Monthly Performance 📈
        </h1>
        <p class="text-muted">Track your learning progress over time</p>
      </div>

      <!-- Overall Trend Card -->
      <div v-if="!loading && !error" class="card mb-4 border-primary bg-light">
        <div class="card-body text-center">
          <div class="d-flex justify-content-center align-items-center gap-2 mb-3">
            <i :class="overallTrend.icon" :style="{ fontSize: '2rem', color: overallTrend.color }"></i>
            <span class="h5 mb-0 text-capitalize">Current trend: {{ overallTrend.text }}</span>
          </div>
          <div :class="['h1 fw-bold', scoreColor(latestScore * 100)]">{{ (latestScore * 100)?.toFixed(1) || 'N/A' }}%</div>
          <small class="text-muted" v-if="data.length">
            Average for {{ formatMonth(data[data.length-1]?.period) }}
          </small>
        </div>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <!-- Monthly Breakdown -->
      <div v-else class="card">
        <div class="card-header">Monthly Breakdown</div>
        <ul class="list-group list-group-flush">
          <li
            v-for="(m,i) in data"
            :key="m.period"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <div class="d-flex align-items-center gap-3">
              <div class="fw-semibold">{{ formatMonth(m.period) }}</div>
              <template v-if="i>0">
                <i
                  :class="trendIcon(data[i].avg_score, data[i-1].avg_score)"
                  :style="{ color: trendColor(data[i].avg_score, data[i-1].avg_score) }"
                ></i>
                <small :style="{ color: trendColor(data[i].avg_score, data[i-1].avg_score) }">
                  <span v-if="m.avg_score && data[i-1].avg_score">
                    {{ ((m.avg_score - data[i-1].avg_score) * 100).toFixed(1) }}%
                  </span>
                </small>
              </template>
            </div>
            <div class="text-end">
              <div :class="['h5 mb-0', scoreColor(m.avg_score * 100)]">{{ (m.avg_score * 100)?.toFixed(1) || 'N/A' }}%</div>
              <small class="text-muted">Average</small>
            </div>
          </li>
        </ul>
      </div>

      <div class="text-center text-secondary small mt-4">
        📊 Keep up the great work! Consistent practice leads to steady improvement.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../api'
import Navigation from './Navigation.vue'

const route = useRoute()
const router = useRouter()
const userId = route.params.user_id

const data = ref([])
const loading = ref(true)
const error = ref('')

// Fetch monthly analytics
onMounted(async () => {
  try {
    const res = await apiFetch(`/analytics/user/${userId}/monthly`)
    data.value = res
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load analytics'
  } finally {
    loading.value = false
  }
})

const latestScore = computed(() =>
  data.value.length ? data.value[data.value.length-1].avg_score : 0
)
const previousScore = computed(() =>
  data.value.length>1 ? data.value[data.value.length-2].avg_score : 0
)

const overallTrend = computed(() => {
  if (latestScore.value > previousScore.value)
    return { text:'up',    icon:'bi bi-trending-up-fill',   color:'#198754' }
  if (latestScore.value < previousScore.value)
    return { text:'down',  icon:'bi bi-trending-down-fill', color:'#dc3545' }
  return { text:'stable', icon:'bi bi-dash-lg',           color:'#6c757d' }
})

function formatMonth(period) {
  if (!period) return ''
  const [y,m] = period.split('-').map(Number)
  return new Date(y,m-1).toLocaleString(undefined,{ month:'short',year:'numeric' })
}

function trendIcon(curr,prev) {
  return curr>prev?'bi bi-trending-up-fill': curr<prev?'bi bi-trending-down-fill':'bi bi-dash-lg'
}
function trendColor(curr,prev) {
  return curr>prev?'#198754': curr<prev?'#dc3545':'#6c757d'
}
function scoreColor(score) {
  return score>=85?'text-success': score>=75?'text-warning':'text-muted'
}

function onNav(page) {
  router.push({ name: page })
}
</script>

<style scoped>
.bi { font-size: 1.5rem; }
</style>