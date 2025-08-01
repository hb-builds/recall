<!-- src/components/AdminQuizzesPage.vue -->
<template>
  <div>
    <Navigation
      is-admin
      current-page="admin-quizzes"
      @navigate="handleNavigate"
    />

    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="h3 fw-bold">Manage Quizzes ⚡</h1>
          <p class="text-muted mb-0">Create and manage quizzes within chapters</p>
        </div>
        <button class="btn btn-primary" @click="openCreateModal">
          <i class="bi bi-plus me-1"></i>Add Quiz
        </button>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <!-- Quizzes Grid -->
      <div v-else class="row g-4">
        <div
          class="col-12 col-md-6"
          v-for="quiz in quizzes"
          :key="quiz.id"
        >
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="card-title mb-0">{{ quiz.title }}</h5>
                <span class="badge bg-secondary text-uppercase small">
                  {{ formatDate(quiz.scheduled_at) }}
                </span>
              </div>
              <p class="text-muted mb-3">
                <i class="bi bi-clock me-1"></i>{{ quiz.duration_min }} min
              </p>
              <div class="d-flex gap-2">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="openEditModal(quiz)"
                >
                  <i class="bi bi-pencil me-1"></i>Edit
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteQuiz(quiz)"
                >
                  <i class="bi bi-trash me-1"></i>Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create / Edit Modal -->
    <div v-if="modalOpen">
      <div class="modal-backdrop fade show"></div>
      <div class="modal d-block" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                {{ editing ? 'Edit Quiz' : 'Create New Quiz' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select
                  class="form-select"
                  v-model="form.chapter_id"
                >
                  <option value="" disabled>Select a chapter</option>
                  <option
                    v-for="ch in chapters"
                    :key="ch.id"
                    :value="ch.id"
                  >{{ getChapterName(ch.id) }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Quiz Title</label>
                <input
                  v-model="form.title"
                  type="text"
                  class="form-control"
                  placeholder="Enter quiz title"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (minutes)</label>
                <input
                  v-model.number="form.duration_min"
                  type="number"
                  min="1"
                  class="form-control"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Scheduled At</label>
                <input
                  v-model="form.scheduled_at"
                  type="datetime-local"
                  class="form-control"
                />
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button
                class="btn btn-primary"
                :disabled="!form.title.trim() || !form.chapter_id || !form.scheduled_at"
                @click="editing ? updateQuiz() : createQuiz()"
              >
                {{ editing ? 'Save Changes' : 'Create Quiz' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api'
import Navigation from './Navigation.vue'

const router    = useRouter()
const quizzes   = ref([])
const chapters  = ref([])
const loading   = ref(true)
const error     = ref('')
const modalOpen = ref(false)
const editing   = ref(false)
const form      = ref({
  id: null,
  chapter_id: '',
  title: '',
  duration_min: 30,
  scheduled_at: ''
})

// Fetch chapters & quizzes
async function fetchData() {
  loading.value = true
  try {
    const chRes = await apiFetch('/admin/chapters?page=1&limit=100&search=')
    chapters.value = chRes.items || []
    const qRes = await apiFetch('/admin/quizzes?page=1&limit=100&search=')
    quizzes.value = qRes.items || []
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load data'
  } finally {
    loading.value = false
  }
}

// Create
async function createQuiz() {
  try {
    // convert scheduled_at to ISO
    const payload = {
      chapter_id: Number(form.value.chapter_id),
      title: form.value.title,
      duration_min: form.value.duration_min,
      scheduled_at: new Date(form.value.scheduled_at).toISOString()
    }
    const res = await apiFetch('/admin/quizzes', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
    quizzes.value.push({ id: res.id, ...payload })
    closeModal()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Create failed')
  }
}

// Update
async function updateQuiz() {
  try {
    const id = form.value.id
    const payload = {
      chapter_id: Number(form.value.chapter_id),
      title: form.value.title,
      duration_min: form.value.duration_min,
      scheduled_at: new Date(form.value.scheduled_at).toISOString()
    }
    await apiFetch(`/admin/quizzes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload)
    })
    const idx = quizzes.value.findIndex(q => q.id === id)
    quizzes.value[idx] = { id, ...payload }
    closeModal()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Update failed')
  }
}

// Delete
async function deleteQuiz(q) {
  if (!confirm(`Delete quiz "${q.title}"?`)) return
  try {
    await apiFetch(`/admin/quizzes/${q.id}`, { method: 'DELETE' })
    quizzes.value = quizzes.value.filter(x => x.id !== q.id)
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Delete failed')
  }
}

// Modal controls
function openCreateModal() {
  editing.value = false
  form.value = {
    id: null,
    chapter_id: '',
    title: '',
    duration_min: 30,
    scheduled_at: ''
  }
  modalOpen.value = true
}
function openEditModal(q) {
  editing.value = true
  form.value = {
    id: q.id,
    chapter_id: q.chapter_id,
    title: q.title,
    duration_min: q.duration_min,
    scheduled_at: q.scheduled_at.slice(0,16) // for datetime-local
  }
  modalOpen.value = true
}
function closeModal() {
  modalOpen.value = false
}

// Helpers
function formatDate(iso) {
  return new Date(iso).toLocaleString(undefined, {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}
function getChapterName(id) {
  return chapters.value.find(c => c.id === id)?.name || 'Unknown'
}

// Navigation
function handleNavigate(page) {
  router.push({ name: page })
}

// Lifecycle
onMounted(fetchData)
</script>

<style scoped>
.modal-backdrop {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,.5); z-index: 1040;
}
.modal {
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%,-50%); z-index: 1050;
}
</style>