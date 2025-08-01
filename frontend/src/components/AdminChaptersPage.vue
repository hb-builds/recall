<!-- src/components/AdminChaptersPage.vue -->
<template>
  <div>
    <Navigation
      is-admin
      current-page="admin-chapters"
      @navigate="handleNavigate"
    />

    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="h3 fw-bold">Manage Chapters 📖</h1>
          <p class="text-muted mb-0">Create and manage chapters within subjects</p>
        </div>
        <button class="btn btn-primary" @click="openCreateModal">
          <i class="bi bi-plus me-1"></i>Add Chapter
        </button>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <!-- Chapters grid -->
      <div v-else class="row g-4">
        <div
          class="col-12 col-md-6 col-lg-4"
          v-for="ch in chapters"
          :key="ch.id"
        >
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <i class="bi bi-file-text fs-4 text-success me-2"></i>
                <h5 class="card-title mb-0">{{ ch.name }}</h5>
              </div>
              <p class="card-text text-muted">{{ ch.description }}</p>
              <p class="text-sm text-secondary mb-3">
                Subject: {{ subjectName(ch.subject_id) }}
              </p>
              <div class="d-flex gap-2">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="openEditModal(ch)"
                >
                  <i class="bi bi-pencil me-1"></i>Edit
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteChapter(ch)"
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
                {{ editing ? 'Edit Chapter' : 'Create New Chapter' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Subject</label>
                <select
                  class="form-select"
                  v-model="form.subject_id"
                >
                  <option value="" disabled>Select a subject</option>
                  <option
                    v-for="s in subjects"
                    :key="s.id"
                    :value="s.id"
                  >{{ s.name }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Chapter Name</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  placeholder="Enter chapter name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  v-model="form.description"
                  class="form-control"
                  rows="3"
                  placeholder="Enter chapter description"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button
                class="btn btn-primary"
                :disabled="!form.name.trim() || !form.subject_id"
                @click="editing ? updateChapter() : createChapter()"
              >
                {{ editing ? 'Save Changes' : 'Create Chapter' }}
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

const router = useRouter()

// State
const chapters     = ref([])
const subjects     = ref([])
const loading      = ref(true)
const error        = ref('')
const modalOpen    = ref(false)
const editing      = ref(false)
const form         = ref({ id: null, subject_id: '', name: '', description: '' })

// Fetch subjects & chapters
async function fetchData() {
  loading.value = true
  try {
    // fetch subjects for dropdown
    const subjRes = await apiFetch('/admin/subjects?page=1&limit=100&search=')
    subjects.value = subjRes.items || []

    // fetch chapters
    const chapRes = await apiFetch('/admin/chapters?page=1&limit=100&search=')
    chapters.value = chapRes.items || []
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load data'
  } finally {
    loading.value = false
  }
}

// Create
async function createChapter() {
  try {
    const payload = {
      subject_id: Number(form.value.subject_id),
      name: form.value.name,
      description: form.value.description
    }
    const res = await apiFetch('/admin/chapters', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
    chapters.value.push({ id: res.id, ...payload })
    closeModal()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Create failed')
  }
}

// Update
async function updateChapter() {
  try {
    const id = form.value.id
    const payload = {
      subject_id: Number(form.value.subject_id),
      name: form.value.name,
      description: form.value.description
    }
    await apiFetch(`/admin/chapters/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload)
    })
    const idx = chapters.value.findIndex(c => c.id === id)
    chapters.value[idx] = { id, ...payload }
    closeModal()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Update failed')
  }
}

// Delete
async function deleteChapter(ch) {
  if (!confirm(`Delete chapter "${ch.name}"?`)) return
  try {
    await apiFetch(`/admin/chapters/${ch.id}`, { method: 'DELETE' })
    chapters.value = chapters.value.filter(x => x.id !== ch.id)
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Delete failed')
  }
}

// Modal controls
function openCreateModal() {
  editing.value = false
  form.value = { id: null, subject_id: '', name: '', description: '' }
  modalOpen.value = true
}
function openEditModal(ch) {
  editing.value = true
  form.value = {
    id: ch.id,
    subject_id: ch.subject_id,
    name: ch.name,
    description: ch.description
  }
  modalOpen.value = true
}
function closeModal() {
  modalOpen.value = false
}

// Helpers
function subjectName(id) {
  return subjects.value.find(s => s.id === id)?.name || 'Unknown'
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