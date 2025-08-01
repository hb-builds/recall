<!-- src/components/AdminSubjectsPage.vue -->
<template>
  <div>
    <Navigation
      current-page="admin-subjects"
      @navigate="handleNavigate"
    />

    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="h3 fw-bold">Manage Subjects 📚</h1>
          <p class="text-muted mb-0">Create and manage quiz subjects</p>
        </div>
        <button class="btn btn-primary" @click="openCreateModal">
          <i class="bi bi-plus me-1"></i> Add Subject
        </button>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <!-- Subjects Grid -->
      <div v-else class="row g-4">
        <div
          class="col-12 col-md-6 col-lg-4"
          v-for="subj in subjects"
          :key="subj.id"
        >
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3">
                <i class="bi bi-book-open fs-4 text-primary me-2"></i>
                <h5 class="card-title mb-0">{{ subj.name }}</h5>
              </div>
              <p class="card-text text-muted">{{ subj.description }}</p>
              <div class="d-flex gap-2">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  @click="openEditModal(subj)"
                >
                  <i class="bi bi-pencil me-1"></i>Edit
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="deleteSubject(subj)"
                >
                  <i class="bi bi-trash me-1"></i>Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal">
      <div class="modal-backdrop fade show"></div>
      <div class="modal d-block" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                {{ editing ? 'Edit Subject' : 'Create New Subject' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Subject Name</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  placeholder="Enter subject name"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  v-model="form.description"
                  class="form-control"
                  placeholder="Enter subject description"
                  rows="3"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">
                Cancel
              </button>
              <button
                class="btn btn-primary"
                @click="editing ? updateSubject() : createSubject()"
                :disabled="!form.name.trim()"
              >
                {{ editing ? 'Save Changes' : 'Create Subject' }}
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
const subjects = ref([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)
const editing = ref(false)
const form = ref({ id: null, name: '', description: '' })

// Fetch list
async function fetchSubjects() {
  loading.value = true
  try {
    const res = await apiFetch('/admin/subjects?page=1&limit=10&search=')
    subjects.value = res.items || []
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load subjects'
  } finally {
    loading.value = false
  }
}

// Create
async function createSubject() {
  try {
    const payload = { name: form.value.name, description: form.value.description }
    const res = await apiFetch('/admin/subjects', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
    // use returned id
    subjects.value.push({ id: res.id, ...payload })
    closeModal()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Create failed')
  }
}

// Update
async function updateSubject() {
  try {
    const { id, name, description } = form.value
    await apiFetch(`/admin/subjects/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ name, description })
    })
    // update local list
    const idx = subjects.value.findIndex(s => s.id === id)
    subjects.value[idx] = { id, name, description }
    closeModal()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Update failed')
  }
}

// Delete
async function deleteSubject(subj) {
  if (!confirm(`Delete "${subj.name}"?`)) return
  try {
    await apiFetch(`/admin/subjects/${subj.id}`, { method: 'DELETE' })
    subjects.value = subjects.value.filter(s => s.id !== subj.id)
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Delete failed')
  }
}

// Modal controls
function openCreateModal() {
  editing.value = false
  form.value = { id: null, name: '', description: '' }
  showModal.value = true
}
function openEditModal(subj) {
  editing.value = true
  form.value = { ...subj }
  showModal.value = true
}
function closeModal() {
  showModal.value = false
}

// Navigation
function handleNavigate(page) {
  if (page === 'admin-subjects') return
  router.push({ name: page })
}

// lifecycle
onMounted(fetchSubjects)
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