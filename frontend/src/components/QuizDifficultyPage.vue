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
          Hardest Quizzes Globally 🌍
        </h1>
        <p class="text-muted">Top 5 quizzes with the lowest average scores across all users</p>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <!-- Hardest Quizzes List -->
      <div v-else class="card">
        <div class="card-header">Top 5 Hardest Quizzes</div>
        <ul class="list-group list-group-flush">
          <li
            v-for="quiz in data"
            :key="quiz.quiz_id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span class="fw-semibold">{{ quiz.title }}</span>
            <div class="text-end">
              <div :class="['h5 mb-0', scoreColor(quiz.average_score)]">
                {{ quiz.average_score.toFixed(1) }}%
              </div>
              <small class="text-muted">Average Score</small>
            </div>
          </li>
        </ul>
      </div>

      <div class="text-center text-secondary small mt-4">
        💡 Use this data to identify challenging topics and improve learning materials.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api'
import Navigation from './Navigation.vue'

// const route = useRoute()
const router = useRouter()
// const quizId = route.params.quiz_id

const data = ref([])
const loading = ref(true)
const error = ref('')

// Fetch difficulty
onMounted(async () => {
  try {
    const res = await apiFetch(`/analytics/quizzes/hardest`)
    data.value = res
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load hardest quizzes'
  } finally {
    loading.value = false
  }
})

function scoreColor(score) {
  return score >= 80 ? 'text-success'
       : score >= 60 ? 'text-warning'
       : 'text-danger'
}

function onNav(page) {
  router.push({ name: page })
}
</script>