<template>
  <div>
    <!-- Top nav -->
    <Navigation
      :is-admin="false"
      current-page="quizzes"
      @navigate="onNav"
    />

    <div class="container py-4">
      <!-- Back button -->
      <button class="btn btn-link mb-3" @click="goBack">
        <i class="bi bi-arrow-left me-1"></i>
        Back to Chapters
      </button>

      <!-- Start screen -->
      <div v-if="!quizStarted && !loadingQuiz" class="text-center">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          {{ quiz.title }} ⚡
        </h1>
        <p class="text-muted mb-4">
          {{ quiz.questions.length }} questions · {{ quiz.duration_min }} min
        </p>
        <button class="btn btn-primary px-4 py-2" @click="startQuiz">
          Start Quiz ({{ quiz.duration_min }} min)
        </button>
      </div>

      <!-- Loading or error for quiz fetch -->
      <div v-if="loadingQuiz" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="quizError" class="alert alert-danger">{{ quizError }}</div>

      <!-- Quiz in progress -->
      <div v-if="quizStarted && !quizSubmitted">
        <!-- Timer + Progress -->
        <div class="mb-4">
          <div class="d-flex justify-content-between">
            <small>Question {{ currentIndex + 1 }} / {{ quiz.questions.length }}</small>
            <small class="text-danger">
              <i class="bi bi-clock me-1"></i>{{ formatTime(timeRemaining) }}
            </small>
          </div>
          <div class="progress" style="height:6px;">
            <div
              class="progress-bar"
              role="progressbar"
              :style="{ width: `${((currentIndex+1)/quiz.questions.length)*100}%` }"
            ></div>
          </div>
        </div>

        <!-- Current Question -->
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">{{ quiz.questions[currentIndex].statement }}</h5>
            <div class="mt-3">
              <div
                v-for="(opt, idx) in quiz.questions[currentIndex].options"
                :key="idx"
                class="form-check mb-2"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  :name="'q'+quiz.questions[currentIndex].question_id"
                  :id="'q'+quiz.questions[currentIndex].question_id+'-opt'+idx"
                  :value="idx"
                  @change="answerQuestion(quiz.questions[currentIndex].question_id, idx)"
                  :checked="answers[quiz.questions[currentIndex].question_id] === idx"
                />
                <label
                  class="form-check-label"
                  :for="'q'+quiz.questions[currentIndex].question_id+'-opt'+idx"
                >
                  {{ opt }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Prev / Next / Submit -->
        <div class="d-flex justify-content-between">
          <button
            class="btn btn-outline-secondary"
            :disabled="currentIndex === 0"
            @click="currentIndex--"
          >
            Previous
          </button>
          <button
            v-if="currentIndex < quiz.questions.length - 1"
            class="btn btn-primary"
            @click="currentIndex++"
          >
            Next
          </button>
          <button
            v-else
            class="btn btn-success"
            :disabled="Object.keys(answers).length < quiz.questions.length"
            @click="submitQuiz"
          >
            Submit Quiz
          </button>
        </div>
      </div>

      <!-- Submission screen -->
      <div v-if="quizSubmitted" class="text-center my-5">
        <div class="spinner-border text-success mb-3"></div>
        <p>Submitting...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiFetch } from '../api'
// import { auth } from '../store/auth'
import Navigation from './Navigation.vue'

// Routing & state
const route = useRoute()
const router = useRouter()
const quizId = route.params.quiz_id

const quiz = ref({ title: '', duration_min: 0, questions: [] })
const loadingQuiz = ref(true)
const quizError = ref('')
const quizStarted = ref(false)
const quizSubmitted = ref(false)

const currentIndex = ref(0)
const answers = ref({})      // { question_id: selected_option_index }
const timeRemaining = ref(0) // seconds
const attemptId = ref(null)

// Fetch quiz on mount
onMounted(async () => {
  try {
    const data = await apiFetch(`/quizzes/${quizId}/full`)
    quiz.value = data
    timeRemaining.value = data.duration_min * 60
  } catch (e) {
    quizError.value = e.msg || 'Failed to load quiz'
  } finally {
    loadingQuiz.value = false
  }
})

// Timer
watch([quizStarted, timeRemaining], ([started, t]) => {
  if (started && t > 0 && !quizSubmitted.value) {
    setTimeout(() => timeRemaining.value--, 1000)
  }
  if (started && t === 0 && !quizSubmitted.value) {
    submitQuiz()
  }
})

// Handlers
async function startQuiz() {
  try {
    const data = await apiFetch(`/quizzes/${quizId}/start`, { method: 'POST' })
    attemptId.value = data.attempt_id
    quizStarted.value = true
  } catch (e) {
    quizError.value = e.msg || 'Failed to start quiz'
  }
}

function answerQuestion(qid, optIdx) {
  answers.value[qid] = optIdx
}

async function submitQuiz() {
  quizSubmitted.value = true
  try {
    const payload = {
      answers: Object.entries(answers.value).map(([qid, opt]) => ({
        question_id: +qid,
        selected_option: opt
      }))
    }
    const result = await apiFetch(`/attempts/${attemptId.value}/submit`, {
      method: 'POST',
      body: JSON.stringify(payload)
    })
    // navigate to attempt detail
    router.push({ name: 'attempt-detail', params: { attempt_id: result.attempt_id } })
  } catch (e) {
    console.error('Submit failed', e)
    quizSubmitted.value = false
  }
}

function formatTime(sec) {
  const m = String(Math.floor(sec/60)).padStart(2,'0')
  const s = String(sec%60).padStart(2,'0')
  return `${m}:${s}`
}

function goBack() {
  router.push({ name: 'quizzes', params: { chapter_id: route.params.chapter_id } })
}

function onNav(page) {
  const m = { subjects: '/', history: '/history', reports: '/reports' }
  router.push(m[page] || '/')
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
</style>