<!-- src/components/UserRankingPage.vue -->
<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="user-ranking"
      @navigate="onNav"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Your Global Ranking 🌟
        </h1>
        <p class="text-muted">See how you stack up against other learners</p>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <div v-else>
        <!-- Main Card -->
        <div class="card mb-4 border-primary bg-light">
          <div class="card-body text-center">
            <i class="bi bi-trophy-fill fs-1 text-primary mb-3"></i>
            <div class="h1 fw-bold text-primary">#{{ ranking.ranking }}</div>
            <div class="h6 text-muted mb-2">of {{ ranking.total_users.toLocaleString() }} users</div>
            <div :class="['h3 fw-semibold', percentileColor]">
              {{ percentile.toFixed(1) }}th percentile
            </div>
            <small class="text-muted d-block mt-2">{{ ranking.improvement_trend }}</small>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="row g-4 mb-4">
          <div class="col-12 col-md-4" v-for="stat in stats" :key="stat.label">
            <div class="card text-center">
              <div class="card-body">
                <i :class="['bi', stat.icon, 'fs-2', stat.color, 'mb-2']"></i>
                <div class="h4 fw-bold" :class="stat.color">{{ stat.value }}</div>
                <small class="text-muted">{{ stat.label }}</small>
              </div>
            </div>
          </div>
        </div>

        <!-- Percentile Progress -->
        <div class="card">
          <div class="card-body">
            <h5>Your Position</h5>
            <div class="d-flex justify-content-between small text-muted">
              <span>0th</span>
              <span :class="percentileColor">{{ percentile.toFixed(1) }}th</span>
              <span>100th</span>
            </div>
            <div class="progress" style="height: 6px;">
              <div
                class="progress-bar"
                :class="percentileBarColor"
                :style="{ width: percentile + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../api'
import Navigation from './Navigation.vue'

const route = useRoute()
const router = useRouter()
const userId = route.params.user_id

const ranking = ref({})
const attempts = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const [rankingData, attemptsData] = await Promise.all([
      apiFetch(`/leaderboard/user/${userId}`),
      apiFetch(`/users/${userId}/attempts`)
    ])
    ranking.value = rankingData
    attempts.value = attemptsData
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load ranking'
  } finally {
    loading.value = false
  }
})

const percentile = computed(() => {
  if (!ranking.value.total_users) return 0
  return ((ranking.value.total_users - ranking.value.ranking) / ranking.value.total_users) * 100
})

const percentileColor = computed(() =>
  percentile.value >= 90 ? 'text-success'
    : percentile.value >= 75 ? 'text-warning'
    : 'text-muted'
)
const percentileBarColor = computed(() =>
  percentile.value >= 90 ? 'bg-success'
    : percentile.value >= 75 ? 'bg-warning'
    : 'bg-danger'
)

const averageScore = computed(() => {
  if (!attempts.value.length) return 0
  const validAttempts = attempts.value.filter(a => a.total_questions > 0)
  if (!validAttempts.length) return 0
  const sum = validAttempts.reduce((acc, a) => acc + a.score/a.total_questions, 0)
  return (sum/validAttempts.length)*100
})

const stats = computed(() => [
  { label: 'Average Score',    value: `${averageScore.value.toFixed(1)}%`, icon: 'bi-target',       color: 'text-success' },
  { label: 'Quizzes Taken',     value: attempts.value.length,     icon: 'bi-people',       color: 'text-primary' },
  { label: 'Percentile Rank',   value: `${percentile.value.toFixed(1)}th`,  icon: 'bi-bar-chart-fill', color: percentileColor.value }
])

function onNav(page) {
  router.push({ name: page })
}
</script>