<!-- src/components/QuizLeaderboardPage.vue -->
<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="quiz-leaderboard"
      @navigate="onNav"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Quiz Leaderboard 🏆
        </h1>
        <p class="text-muted">Top performers for this quiz</p>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <!-- Podium (Top 3) -->
      <div v-else class="row g-4 mb-4">
        <div
          v-for="(entry, i) in leaderboard.slice(0,3)"
          :key="entry.user_id"
          class="col-12 col-md-4"
        >
          <div :class="['card text-center border-2', rankBg(i)]">
            <div class="card-body">
              <i :class="['bi', rankIcon(i), 'fs-1 mb-3']"></i>
              <h5 class="card-title">{{ entry.full_name }}</h5>
              <div :class="['h2 fw-bold', scoreColor(entry.score)]">
                {{ entry.score }}%
              </div>
              <span class="badge bg-light text-dark">#{{ i+1 }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Full Leaderboard -->
      <div class="card">
        <div class="card-header">Complete Rankings</div>
        <ul class="list-group list-group-flush">
          <li
            v-for="(entry, i) in leaderboard"
            :key="entry.user_id"
            :class="['list-group-item d-flex justify-content-between align-items-center', rankBg(i)]"
          >
            <div class="d-flex align-items-center gap-3">
              <i :class="['bi', rankIcon(i), 'fs-4']"></i>
              <div>
                <div class="fw-semibold">{{ entry.full_name }}</div>
                <small class="text-muted">User #{{ entry.user_id }}</small>
              </div>
            </div>
            <div class="text-end">
              <div :class="['h5 mb-0', scoreColor(entry.score)]">{{ entry.score }}%</div>
              <small class="text-muted">Score</small>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../api'
import Navigation from './Navigation.vue'

const route = useRoute()
const router = useRouter()
const quizId = route.params.quiz_id

const leaderboard = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await apiFetch(`/leaderboard/quiz/${quizId}?limit=10`)
    leaderboard.value = res
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load leaderboard'
  } finally {
    loading.value = false
  }
})

function rankIcon(i) {
  return i===0 ? 'bi-trophy-fill text-warning'
       : i===1 ? 'bi-award-fill text-secondary'
       : i===2 ? 'bi-award text-warning'
       : 'bi-circle'
}
function rankBg(i) {
  return i===0 ? 'bg-warning bg-opacity-25'
       : i===1 ? 'bg-secondary bg-opacity-10'
       : i===2 ? 'bg-warning bg-opacity-10'
       : 'bg-white'
}
function scoreColor(score) {
  return score>=90 ? 'text-success'
       : score>=80 ? 'text-warning'
       : 'text-muted'
}

function onNav(page) {
  router.push({ name: page })
}
</script>