<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="history"
      @navigate="onNav"
    />

    <div class="container py-4">
      <!-- Back -->
      <button class="btn btn-link mb-3" @click="goBack">
        <i class="bi bi-arrow-left me-1"></i>
        Back to History
      </button>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <!-- Summary -->
      <div v-else>
        <div class="card mb-4 text-center">
          <div class="card-body">
            <h3 class="card-title">{{ review.title }}</h3>
            <h1 :class="scoreClass">{{ attempt.score }} / {{ attempt.details.length }}</h1>
            <p class="text-muted">{{ scorePct }}%</p>
            <p>{{ scoreMessage }}</p>
            <small class="text-muted">Submitted {{ formattedDate }}</small>
          </div>
        </div>

        <!-- Question Review -->
        <h5>Question Review</h5>
        <div class="mb-4" v-for="(q, idx) in review.questions" :key="q.question_id">
          <div class="card mb-2">
            <div class="card-header d-flex justify-content-between align-items-center">
              <span>Q{{ idx+1 }}: {{ q.statement }}</span>
              <span
                class="badge"
                :class="q.selected === q.correct ? 'bg-success' : 'bg-danger'"
              >
                <i :class="q.selected === q.correct ? 'bi bi-check-circle' : 'bi bi-x-circle'"></i>
                {{ q.selected === q.correct ? 'Correct' : 'Incorrect' }}
              </span>
            </div>
            <ul class="list-group list-group-flush">
              <li
                v-for="(opt, i) in q.options"
                :key="i"
                class="list-group-item d-flex justify-content-between align-items-center"
                :class="{
                  'list-group-item-success': i === q.correct,
                  'list-group-item-danger': i === q.selected && q.selected !== q.correct
                }"
              >
                {{ opt }}
                <div class="d-flex gap-2">
                  <span
                    v-if="i === q.correct"
                    class="badge bg-success"
                  >Correct Answer</span>
                  <span
                    v-if="i === q.selected"
                    :class="['badge', q.selected === q.correct ? 'bg-success' : 'bg-danger']"
                  >Your Answer</span>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- Actions -->
        <div class="text-center">
          <button class="btn btn-primary me-2" @click="takeAnother">
            Take Another Quiz
          </button>
          <button class="btn btn-outline-secondary" @click="viewHistory">
            View All Attempts
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../api'
import { auth } from '../store/auth'
import Navigation from './Navigation.vue'

const route = useRoute()
const router = useRouter()
const attemptId = route.params.attempt_id

const attempt = ref(null)
const review = ref({ title: '', questions: [] })
const loading = ref(true)
const error = ref('')

// Fetch attempt detail (you need a GET /api/attempts/:id!)
onMounted(async () => {
  try {
    // 1. Fetch attempt details first to get the quiz_id
    const attemptData = await apiFetch(`/attempts/${attemptId}`)
    attempt.value = attemptData

    // 2. Then fetch the full quiz data using the quiz_id from the attempt
    const quizData = await apiFetch(`/quizzes/${attemptData.quiz_id}/full`)

    // 3. Merge the data for the review, using the 'correct' value from the attempt
    review.value.title = quizData.title
    review.value.questions = quizData.questions.map(q => {
      const userAns = attemptData.details.find(d => d.question_id === q.question_id)
      return {
        ...q, // statement, options
        selected: userAns?.selected,
        correct: userAns?.correct,
      }
    })

  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load attempt details'
  } finally {
    loading.value = false
  }
})

// Derived state
const scorePct = computed(() =>
  Math.round((attempt.value?.score / attempt.value?.details.length) * 100)
)
const scoreClass = computed(() =>
  scorePct.value >= 80 ? 'text-success' :
  scorePct.value >= 60 ? 'text-warning' : 'text-danger'
)
const scoreMessage = computed(() =>
  scorePct.value >= 80 ? 'Excellent work! 🌟' :
  scorePct.value >= 60 ? 'Good job! 👍' :
  'Keep practicing! 💪'
)
const formattedDate = computed(() =>
  new Date(attempt.value?.submitted_at).toLocaleString()
)

// Navigation
function goBack() {
  router.push({ name: 'history', params: { user_id: auth.state.user.id } })
}
function takeAnother() {
  router.push({ name: 'subjects' })
}
function viewHistory() {
  router.push({ name: 'history', params: { user_id: auth.state.user.id } })
}
function onNav(page) {
  const map = { home: 'subjects', history: 'history', reports: 'reports' }
  router.push({ name: map[page] || 'subjects' })
}
</script>

<style scoped>
.list-group-item-success { background-color: #e6ffe6; }
.list-group-item-danger  { background-color: #ffe6e6; }
</style>