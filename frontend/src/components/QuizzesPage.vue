<template>
  <div>
    <!-- Top navigation bar -->
    <Navigation
      :is-admin="false"
      current-page="quizzes"
      @navigate="handleNavigate"
    />

    <div class="container py-4">
      <!-- Back button -->
      <button class="btn btn-link mb-3" @click="goBack">
        <i class="bi bi-arrow-left me-1"></i>
        Back to Chapters
      </button>

      <!-- Header -->
      <div class="text-center mb-4">
        <h1
          class="display-6 fw-bold"
          style="font-family: Montserrat, sans-serif; font-weight: 600;"
        >
          Available Quizzes ⚡
        </h1>
        <p class="text-muted">Ready when you are! Pick a quiz to test your knowledge</p>
      </div>

      <!-- Loading / Error states -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary" role="status"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <!-- Quizzes grid -->
      <div v-else class="row g-4 row-cols-1 row-cols-md-2">
        <div
          class="col"
          v-for="quiz in quizzes"
          :key="quiz.id"
        >
          <div
            class="card h-100 shadow-sm border-0 cursor-pointer hover-shadow"
            @click="selectQuiz(quiz)"
            @mouseover="hover = quiz.id"
            @mouseleave="hover = null"
          >
            <div class="card-body d-flex justify-content-between align-items-start pb-3">
              <div class="d-flex align-items-start gap-3">
                <div class="bg-warning bg-opacity-10 p-2 rounded-3 d-flex align-items-center">
                  <i class="bi bi-play-fill fs-4 text-warning"></i>
                </div>
                <div>
                  <h5 class="card-title mb-1">{{ quiz.title }}</h5>
                  <div class="d-flex align-items-center gap-2 mt-1">
                    <i class="bi bi-clock me-1 text-muted"></i>
                    <span class="text-muted small">{{ quiz.duration_min }} minutes</span>
                  </div>
                </div>
              </div>
              <span class="badge bg-secondary text-uppercase small">
                {{ formatDate(quiz.scheduled_at) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Pro tip -->
      <div class="text-center text-secondary mt-5 small">
        🎯 Pro tip: Take your time and read each question carefully!
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
const chapterId = route.params.chapter_id

const quizzes = ref([])
const loading = ref(true)
const error = ref('')
const hover = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    // Fetch real quizzes from API
    const res = await apiFetch(`/chapters/${chapterId}/quizzes`)
    quizzes.value = Array.isArray(res) ? res : res.items || []
  } catch (err) {
    console.error('Fetch quizzes error:', err)
    error.value = err.msg || 'Failed to load quizzes'
  } finally {
    loading.value = false
  }
})

function goBack() {
  router.push({ name: 'chapters', params: { subject_id: route.params.subject_id } })
}

function selectQuiz(quiz) {
  router.push({ name: 'quiz-detail', params: { quiz_id: quiz.id } })
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function handleNavigate(page) {
  switch (page) {
    case 'subjects':
      router.push({ name: 'subjects' })
      break
    case 'history':
      router.push({ name: 'history' })
      break
    case 'reports':
      router.push({ name: 'reports' })
      break
    case 'admin-subjects':
      router.push({ name: 'admin-subjects' })
      break
    default:
      break
  }
}
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
.hover-shadow {
  transition: box-shadow .2s, transform .2s;
}
.hover-shadow:hover {
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,.1) !important;
  transform: translateY(-2px);
}
</style>