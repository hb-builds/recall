<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="history"
      @navigate="onNav"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Your Quiz History 📊
        </h1>
        <p class="text-muted">Track your progress and review past attempts</p>
      </div>

      <!-- Stats Overview -->
      <div v-if="!loading && !error" class="row g-4 mb-4">
        <div class="col-12 col-md-4">
          <div class="card text-center">
            <div class="card-body">
              <i class="bi bi-bar-chart-line-fill text-primary fs-3 mb-2"></i>
              <div class="h4 fw-bold">{{ Math.round(averageScore) }}%</div>
              <small class="text-muted">Average Score</small>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="card text-center">
            <div class="card-body">
              <i class="bi bi-clipboard-check text-success fs-3 mb-2"></i>
              <div class="h4 fw-bold">{{ attempts.length }}</div>
              <small class="text-muted">Total Attempts</small>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="card text-center">
            <div class="card-body">
              <i class="bi bi-clock-history text-warning fs-3 mb-2"></i>
              <div class="h6 text-warning">{{ formatDate(lastAttempt) }}</div>
              <small class="text-muted">Last Quiz</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <!-- Attempts List -->
      <div v-else class="row g-4">
        <div
          class="col-12 col-md-6"
          v-for="att in attempts"
          :key="att.id"
        >
          <div
            class="card h-100 cursor-pointer hover-shadow"
            @click="goDetail(att)"
          >
            <div class="card-body d-flex justify-content-between align-items-start">
              <div>
                <h5 class="card-title">{{ att.quiz_title }}</h5>
                <small class="text-muted">{{ formatDate(att.submitted_at) }}</small>
              </div>
              <span
                class="badge"
                :class="scoreBadge(att.score, att.details?.length || 0)"
              >
                {{ att.score }}/{{ att.total_questions }}
                <span v-if="att.total_questions">({{ Math.round((att.score/att.total_questions)*100) }}%)</span>
              </span>
            </div>
          </div>
        </div>
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

const attempts = ref([])
const loading  = ref(true)
const error    = ref('')

onMounted(async () => {
  try {
    const attemptsData = await apiFetch(`/users/${userId}/attempts`)
    
    const quizIds = [...new Set(attemptsData.map(a => a.quiz_id))]
    
    const quizzes = await Promise.all(
      quizIds.map(id => apiFetch(`/quizzes/${id}/full`))
    )
    
    const quizMap = quizzes.reduce((acc, quiz) => {
      acc[quiz.quiz_id] = quiz
      return acc
    }, {})

    attempts.value = attemptsData.map(att => ({
      ...att,
      quiz_title: quizMap[att.quiz_id]?.title,
      total_questions: quizMap[att.quiz_id]?.questions.length
    }))
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load attempts'
  } finally {
    loading.value = false
  }
})

const averageScore = computed(() => {
  if (!attempts.value.length) return 0
  const validAttempts = attempts.value.filter(a => a.total_questions > 0)
  if (!validAttempts.length) return 0
  const sum = validAttempts.reduce((acc, a) => acc + a.score/a.total_questions, 0)
  return (sum/validAttempts.length)*100
})
const lastAttempt = computed(() =>
  {
    const submitted = attempts.value.filter(a => a.submitted_at)
    return submitted.length ? submitted[0].submitted_at : ''
  }
)

function formatDate(s) {
  return new Date(s).toLocaleString(undefined, {
    month:'short', day:'numeric', year:'numeric', hour:'2-digit', minute:'2-digit'
  })
}

function scoreBadge(score, total) {
  if (total === undefined || total === null) return 'bg-secondary text-white';
  if (total === 0) return 'bg-secondary text-white';
  const pct = (score/total)*100
  return pct>=80 ? 'bg-success text-white'
       : pct>=60 ? 'bg-warning text-dark'
                  : 'bg-danger text-white'
}

function goDetail(attempt) {
  router.push({
    name:'attempt-detail',
    params:{ attempt_id: attempt.id },
    query: { quiz_id: attempt.quiz_id }
  })
}

function onNav(page) {
  router.push({ name: page, params:{ user_id:userId }})
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
.hover-shadow { transition: box-shadow .2s, transform .2s; }
.hover-shadow:hover { box-shadow: 0 0.5rem 1rem rgba(0,0,0,.1); transform: translateY(-2px); }
</style>