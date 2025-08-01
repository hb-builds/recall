<template>
  <div>
    <!-- Top nav bar -->
    <Navigation
      :is-admin="false"
      current-page="subjects"
      @navigate="handleNavigate"
    />

    <div class="container py-4">
      <!-- Back button -->
      <button class="btn btn-link mb-3" @click="goBack">
        <i class="bi bi-arrow-left me-1"></i>
        Back to Subjects
      </button>

      <!-- Header -->
      <div class="text-center mb-4">
        <h1
          class="display-6 fw-bold"
          style="font-family: Montserrat, sans-serif; font-weight: 600;"
        >
          Select a Chapter 📖
        </h1>
        <p class="text-muted">Choose a chapter to explore available quizzes</p>
      </div>

      <!-- Loading / Error states -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary" role="status"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">
        {{ error }}
      </div>

      <!-- Chapters grid -->
      <div v-else class="row g-4">
        <div
          class="col-12 col-md-6"
          v-for="chapter in chapters"
          :key="chapter.id"
        >
          <div
            class="card h-100 shadow-sm cursor-pointer border-0"
            style="transition: box-shadow .2s, transform .2s;"
            @click="selectChapter(chapter)"
            @mouseover="hover = chapter.id"
            @mouseleave="hover = null"
            :class="{'hover-shadow': hover === chapter.id}"
          >
            <div class="card-body d-flex align-items-center">
              <div class="bg-success bg-opacity-10 p-2 rounded-3 me-3 d-flex align-items-center">
                <i class="bi bi-file-text fs-4 text-success"></i>
              </div>
              <div>
                <h5 class="card-title mb-1">{{ chapter.name }}</h5>
                <p class="card-text text-muted mb-0">{{ chapter.description }}</p>
              </div>
            </div>
          </div>
        </div>
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
const subjectId = route.params.subject_id

const chapters = ref([])
const loading = ref(true)
const error = ref('')
const hover = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    // hit your real API
    const res = await apiFetch(`/subjects/${subjectId}/chapters`)
    chapters.value = Array.isArray(res) ? res : res.items || []
  } catch (err) {
    console.error('Fetch chapters error:', err)
    error.value = err.msg || 'Failed to load chapters'
  } finally {
    loading.value = false
  }
})

function goBack() {
  router.push({ name: 'subjects' })
}

function selectChapter(chapter) {
  router.push({ name: 'quizzes', params: { chapter_id: chapter.id } })
}

function handleNavigate(page) {
  // wire Navigation component events here
  if (page === 'subjects') router.push({ name: 'subjects' })
  if (page === 'history')  router.push({ name: 'history' })
  if (page === 'reports')  router.push({ name: 'reports' })
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
.hover-shadow { box-shadow: 0 0.5rem 1rem rgba(0,0,0,.1) !important; transform: translateY(-2px); }
</style>