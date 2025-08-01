<!-- src/components/AdminQuestionsPage.vue -->
<template>
  <div>
    <Navigation is-admin current-page="admin-questions" @navigate="handleNavigate" />

    <div class="container py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 class="h3 fw-bold">Manage Questions ❓</h1>
          <p class="text-muted mb-0">Create and manage questions within quizzes</p>
        </div>
        <button class="btn btn-primary" @click="openCreateModal">
          <i class="bi bi-plus me-1"></i>Add Question
        </button>
      </div>

      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else class="row g-4">
        <div class="col-12 col-md-6" v-for="q in questions" :key="q.id">
          <div class="card h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div class="flex-grow-1">
                  <h5 class="card-title">{{ q.statement }}</h5>
                  <small class="text-muted">
                    {{ getQuizInfo(q.quiz_id).title }} • {{ getQuizInfo(q.quiz_id).chapter_name }}
                  </small>
                </div>
                <span class="badge bg-success">
                  Answer: {{ getCorrectOptionText(q) }}
                </span>
              </div>
              <div class="row row-cols-2 g-2 mb-3">
                <div :class="['col p-2 rounded', q.correct_option===1?'bg-emerald-50 border border-emerald-200':'bg-gray-50']">
                  A: {{ q.option1 }}
                </div>
                <div :class="['col p-2 rounded', q.correct_option===2?'bg-emerald-50 border border-emerald-200':'bg-gray-50']">
                  B: {{ q.option2 }}
                </div>
                <div :class="['col p-2 rounded', q.correct_option===3?'bg-emerald-50 border border-emerald-200':'bg-gray-50']">
                  C: {{ q.option3 }}
                </div>
                <div :class="['col p-2 rounded', q.correct_option===4?'bg-emerald-50 border border-emerald-200':'bg-gray-50']">
                  D: {{ q.option4 }}
                </div>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-secondary flex-fill" @click="openEditModal(q)">
                  <i class="bi bi-pencil me-1"></i>Edit
                </button>
                <button class="btn btn-sm btn-outline-danger flex-fill" @click="deleteQuestion(q)">
                  <i class="bi bi-trash me-1"></i>Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modalOpen">
      <div class="modal-backdrop fade show"></div>
      <div class="modal d-block" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ editing ? 'Edit Question' : 'Create New Question' }}</h5>
              <button type="button" class="btn-close" @click="closeModal"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Quiz</label>
                <select class="form-select" v-model="form.quiz_id">
                  <option value="" disabled>Select a quiz</option>
                  <option v-for="z in quizzes" :key="z.id" :value="z.id">{{ z.title }} ({{ z.chapter_name }})</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Question</label>
                <textarea v-model="form.statement" class="form-control" rows="2"></textarea>
              </div>
              <div class="row g-2 mb-3">
                <div class="col"><input v-model="form.option1" class="form-control" placeholder="Option 1" /></div>
                <div class="col"><input v-model="form.option2" class="form-control" placeholder="Option 2" /></div>
                <div class="col"><input v-model="form.option3" class="form-control" placeholder="Option 3" /></div>
                <div class="col"><input v-model="form.option4" class="form-control" placeholder="Option 4" /></div>
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Option</label>
                <select class="form-select" v-model="form.correct_option">
                  <option value="" disabled>Select correct option</option>
                  <option value="1">Option 1</option>
                  <option value="2">Option 2</option>
                  <option value="3">Option 3</option>
                  <option value="4">Option 4</option>
                </select>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button class="btn btn-primary" :disabled="!form.statement.trim()||!form.quiz_id||!form.correct_option" @click="editing?updateQuestion():createQuestion()">
                {{ editing ? 'Save' : 'Create' }}
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

const router      = useRouter()
const questions   = ref([])
const quizzes     = ref([])
const loading     = ref(true)
const error       = ref('')
const modalOpen   = ref(false)
const editing     = ref(false)
const form        = ref({ id:null, quiz_id:'', statement:'', option1:'', option2:'', option3:'', option4:'', correct_option:'' })

async function fetchData() {
  loading.value = true
  try {
    const qz = await apiFetch('/admin/quizzes?page=1&limit=100&search=')
    quizzes.value = qz.items||[]
    const qs = await apiFetch('/admin/questions?page=1&limit=100&search=')
    questions.value = qs.items||[]
  } catch(e) {
    console.error(e)
    error.value = e.msg||'Load failed'
  } finally {
    loading.value = false
  }
}

async function createQuestion() {
  const p = {
    quiz_id: Number(form.value.quiz_id),
    statement: form.value.statement,
    option1: form.value.option1,
    option2: form.value.option2,
    option3: form.value.option3,
    option4: form.value.option4,
    correct_option: Number(form.value.correct_option)
  }
  try {
    const r = await apiFetch('/admin/questions',{method:'POST',body:JSON.stringify(p)})
    questions.value.push({ id:r.id, ...p })
    closeModal()
  } catch(e){ console.error(e); alert(e.msg||'Create failed') }
}

async function updateQuestion() {
  const id = form.value.id
  const p = {
    quiz_id: Number(form.value.quiz_id),
    statement: form.value.statement,
    option1: form.value.option1,
    option2: form.value.option2,
    option3: form.value.option3,
    option4: form.value.option4,
    correct_option: Number(form.value.correct_option)
  }
  try {
    await apiFetch(`/admin/questions/${id}`,{method:'PUT',body:JSON.stringify(p)})
    const i = questions.value.findIndex(x=>x.id===id)
    questions.value[i] = { id, ...p }
    closeModal()
  } catch(e){ console.error(e); alert(e.msg||'Update failed') }
}

async function deleteQuestion(q) {
  if(!confirm(`Delete "${q.statement}"?`))return
  try {
    await apiFetch(`/admin/questions/${q.id}`,{method:'DELETE'})
    questions.value = questions.value.filter(x=>x.id!==q.id)
  } catch(e){ console.error(e); alert(e.msg||'Delete failed') }
}

function openCreateModal() {
  editing.value = false
  form.value = { id:null, quiz_id:'', statement:'', option1:'', option2:'', option3:'', option4:'', correct_option:'' }
  modalOpen.value = true
}
function openEditModal(q) {
  editing.value = true
  form.value = { id:q.id, quiz_id:q.quiz_id, statement:q.statement, option1:q.option1, option2:q.option2, option3:q.option3, option4:q.option4, correct_option:q.correct_option.toString() }
  modalOpen.value = true
}
function closeModal() { modalOpen.value = false }

function getQuizInfo(id){ return quizzes.value.find(x=>x.id===id)||{title:'Unknown',chapter_name:''} }
function getCorrectOptionText(q){ const o=[q.option1,q.option2,q.option3,q.option4]; return o[q.correct_option-1]||'' }

function handleNavigate(page){ router.push({ name: page }) }

onMounted(fetchData)
</script>

<style scoped>
.modal-backdrop{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);z-index:1040}
.modal{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:1050;width:90%;max-width:800px}
</style>