<!-- src/components/ProfilePage.vue -->
<template>
  <div class="container py-4">
    <Navigation 
      :is-admin="false" 
      current-page="profile" 
      @navigate="onNavigate" 
    />

    <div class="text-center mb-4">
      <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
        Your Profile 👤
      </h1>
      <p class="text-muted">Manage your account info and view achievements</p>
    </div>

    <div class="row gy-4">
      <!-- Profile Info -->
      <div class="col-12 col-lg-8">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0 d-flex align-items-center gap-2">
              <i class="bi bi-person-fill fs-5 text-primary"></i>
              Profile Information
            </h5>
            <div>
              <button 
                v-if="!isEditing" 
                class="btn btn-outline-secondary btn-sm"
                @click="isEditing = true"
              >
                <i class="bi bi-pencil me-1"></i>
                Edit
              </button>
              <template v-else>
                <button 
                  class="btn btn-outline-secondary btn-sm me-2" 
                  @click="cancelEdit"
                >
                  <i class="bi bi-x me-1"></i>
                  Cancel
                </button>
                <button 
                  class="btn btn-primary btn-sm" 
                  @click="saveProfile"
                >
                  <i class="bi bi-save me-1"></i>
                  Save
                </button>
              </template>
            </div>
          </div>

          <div class="card-body">
            <!-- Avatar + Basic -->
            <div class="d-flex align-items-center gap-4 mb-4">
              <div
                class="rounded-circle bg-primary text-white d-flex justify-content-center align-items-center"
                style="width: 5rem; height: 5rem;"
              >
                <span class="fs-3">{{ initials }}</span>
              </div>
              <div>
                <h3 class="h5 mb-1">{{ profile.full_name }}</h3>
                <div class="text-muted">{{ profile.email }}</div>
                <span class="badge bg-secondary mt-1">
                  Member since {{ formatDate(profile.joined_date) }}
                </span>
              </div>
            </div>

            <!-- Fields -->
            <div class="row gy-3">
              <div class="col-12 col-md-6" v-for="field in fields" :key="field.key">
                <label :for="field.key" class="form-label">{{ field.label }}</label>
                <template v-if="isEditing">
                  <input
                    :id="field.key"
                    v-model="editForm[field.key]"
                    :type="field.type"
                    class="form-control rounded-pill"
                  />
                </template>
                <template v-else>
                  <div class="d-flex align-items-center gap-2 p-2 bg-light rounded-pill">
                    <i :class="field.iconClass"></i>
                    <span>
                      {{ field.key === 'dob'
                           ? formatDate(profile.dob)
                           : profile[field.key] || '—' }}
                    </span>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats & Achievements -->
      <div class="col-12 col-lg-4">
        <!-- Stats -->
        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0 d-flex align-items-center gap-2">
              <i class="bi bi-bar-chart-line-up fs-5 text-success"></i>
              Your Stats
            </h5>
          </div>
          <div class="card-body row text-center">
            <div class="col-6 mb-3">
              <div class="h3 text-primary">{{ stats.total_quizzes }}</div>
              <small class="text-muted">Quizzes</small>
            </div>
            <div class="col-6 mb-3">
              <div class="h3 text-success">{{ Math.round(stats.average_score) }}%</div>
              <small class="text-muted">Avg Score</small>
            </div>
            <div class="col-6 mb-3">
              <div class="h3 text-warning">{{ stats.best_score }}%</div>
              <small class="text-muted">Best Score</small>
            </div>
            <div class="col-6">
              <div class="h3 text-purple">{{ stats.streak }}</div>
              <small class="text-muted">Day Streak</small>
            </div>
          </div>
        </div>

        <!-- Achievements -->
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0 d-flex align-items-center gap-2">
              <i class="bi bi-award fs-5 text-warning"></i>
              Achievements
            </h5>
          </div>
          <div class="card-body">
            <div 
              v-for="ach in achievements" 
              :key="ach.title" 
              class="d-flex align-items-center gap-3 p-2 bg-light rounded mb-2"
            >
              <div class="fs-4">{{ ach.icon }}</div>
              <div>
                <div class="fw-semibold">{{ ach.title }}</div>
                <small class="text-muted">{{ ach.desc }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api'
import Navigation from './Navigation.vue'

const router     = useRouter()
const profile    = reactive({ full_name:'', email:'', qualification:'', dob:'', joined_date:'' })
const editForm   = reactive({})
const isEditing  = ref(false)
const stats      = reactive({ total_quizzes:0, average_score:0, best_score:0, streak:0 })
const achievements = [
  { title:'Quiz Master',   desc:'Completed 20+ quizzes', icon:'🏆' },
  { title:'High Achiever', desc:'90%+ average score',  icon:'🎯' },
  { title:'On Fire',       desc:'7-day streak',         icon:'🔥' }
]

const fields = [
  { key:'full_name',     label:'Full Name', type:'text', iconClass:'bi bi-person-fill' },
  { key:'email',         label:'Email',     type:'email',iconClass:'bi bi-envelope-fill' },
  { key:'qualification', label:'Qualification', type:'text', iconClass:'bi bi-mortarboard-fill' },
  { key:'dob',           label:'Date of Birth', type:'date', iconClass:'bi bi-calendar-date-fill' }
]

const initials = computed(() =>
  profile.full_name.split(' ').map(n=>n[0]).join('').toUpperCase()
)

function formatDate(s) {
  return new Date(s).toLocaleDateString(undefined, {
    year:'numeric', month:'long', day:'numeric'
  })
}

function onNavigate(page) {
  router.push({ name: page })
}

onMounted(async ()=>{
  try {
    // load profile
    const data = await apiFetch('/users/1')
    Object.assign(profile, {
      full_name:     data.full_name,
      email:         data.email,
      qualification: data.qualification,
      dob:           data.dob,
      joined_date:   data.created_at
    })
    Object.assign(editForm, profile)

    // load attempts for stats
    const atts = await apiFetch('/users/1/attempts')
    stats.total_quizzes = atts.length
    stats.average_score = atts.length
      ? atts.reduce((sum,a)=> sum + (a.score/a.total_questions)*100 ,0)/atts.length
      : 0
    stats.best_score = atts.length
      ? Math.max(...atts.map(a=> Math.round((a.score/a.total_questions)*100)))
      : 0

    // compute streak
    const days = Array.from(new Set(atts.map(a=>a.submitted_at.split('T')[0])))
      .sort((a,b)=>new Date(b)-new Date(a))
    let count = 0
    for (let i=0; i<days.length; i++) {
      if (i===0) count = 1
      else if ((new Date(days[i-1]) - new Date(days[i]))/(1000*60*60*24) === 1) count++
      else break
    }
    stats.streak = count
  } catch(e) {
    console.error(e)
  }
})

function cancelEdit() {
  Object.assign(editForm, profile)
  isEditing.value = false
}

async function saveProfile() {
  try {
    await apiFetch('/users/1', {
      method:'PUT',
      body: JSON.stringify(editForm)
    })
    Object.assign(profile, editForm)
    isEditing.value = false
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Save failed')
  }
}
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
</style>