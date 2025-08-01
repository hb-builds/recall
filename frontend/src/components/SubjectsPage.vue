<template>
  <div>
    <Navigation
      current-page="subjects"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Choose Your Subject 📚
        </h1>
        <p class="text-muted">Select a subject to start your quiz journey</p>
      </div>

      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <div v-else class="row g-4">
        <div
          class="col-12 col-md-6 col-lg-4"
          v-for="subject in subjects"
          :key="subject.id"
        >
          <div
            class="card h-100 shadow-sm cursor-pointer border-0 hover-shadow"
            @click="selectSubject(subject)"
          >
            <div class="card-body d-flex align-items-center">
              <div class="bg-primary bg-opacity-10 p-2 rounded-3 me-3 d-flex align-items-center">
                <i class="bi bi-book fs-4 text-primary"></i>
              </div>
              <div>
                <h5 class="card-title mb-1">{{ subject.name }}</h5>
                <p class="card-text text-muted mb-0">{{ subject.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center text-secondary mt-5 small">
        💡 Tip: Tap here to start your first quiz!
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api'
// import { auth } from '../store/auth'
import Navigation from './Navigation.vue'

const router = useRouter()
const subjects = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  loading.value = true
  try {
    const res = await apiFetch('/subjects')
    subjects.value = Array.isArray(res) ? res : res.items || []
  } catch (err) {
    console.error(err)
    error.value = err.msg || 'Failed to fetch subjects'
  } finally {
    loading.value = false
  }
})

function selectSubject(subject) {
  router.push({ name: 'chapters', params: { subject_id: subject.id } })
}

</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
.hover-shadow {
  transition: box-shadow .2s, transform .2s;
}
.hover-shadow:hover {
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,.10) !important;
  transform: translateY(-2px);
}
</style>