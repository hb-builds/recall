<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="exports"
      @navigate="onNav"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Export Your Data 📁
        </h1>
        <p class="text-muted">Download your quiz attempts and performance data</p>
      </div>

      <!-- Generate Export -->
      <div class="card mb-4">
        <div class="card-header">Generate New Export</div>
        <div class="card-body">
          <p class="text-muted">Export all your quiz attempts as a CSV file.</p>
          <button
            class="btn btn-primary"
            :disabled="exporting"
            @click="handleExportAttempts"
          >
            <span v-if="exporting">
              <i class="bi bi-hourglass-split me-1"></i>Generating…
            </span>
            <span v-else>
              <i class="bi bi-download me-1"></i>Export Quiz Attempts
            </span>
          </button>
        </div>
      </div>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-secondary"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

      <!-- Available Exports -->
      <div v-else class="card mb-4">
        <div class="card-header">Available Exports</div>
        <ul class="list-group list-group-flush">
          <li
            v-for="name in availableExports"
            :key="name"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ name }}
            <button
              class="btn btn-sm btn-outline-secondary"
              @click="downloadFile(name,'exports')"
            >
              <i class="bi bi-download"></i>
            </button>
          </li>
        </ul>
      </div>

      <!-- Available Reports (if any) -->
      <div v-if="availableReports.length" class="card">
        <div class="card-header">Available Reports</div>
        <ul class="list-group list-group-flush">
          <li
            v-for="name in availableReports"
            :key="name"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            {{ name }}
            <button
              class="btn btn-sm btn-outline-secondary"
              @click="downloadFile(name,'reports')"
            >
              <i class="bi bi-download"></i>
            </button>
          </li>
        </ul>
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
const userId = route.params.user_id

const availableExports = ref([])
const availableReports = ref([])
const loading         = ref(true)
const error           = ref('')
const exporting       = ref(false)

async function fetchReports() {
  loading.value = true
  try {
    const res = await apiFetch(`/users/${userId}/reports`)
    availableExports.value = res.exports || []
    availableReports.value = res.reports || []
  } catch (e) {
    console.error(e)
    error.value = e.msg || 'Failed to load reports'
  } finally {
    loading.value = false
  }
}

async function handleExportAttempts() {
  exporting.value = true
  try {
    await apiFetch(`/users/${userId}/exports/attempts`, { method: 'POST' })
    await fetchReports()
  } catch (e) {
    console.error(e)
    alert(e.msg || 'Export failed')
  } finally {
    exporting.value = false
  }
}

function downloadFile(filename, type) {
  const apiRoot = (window.API_ROOT || 'http://localhost:5000').replace(/\/api$/, '')
  window.open(`${apiRoot}/${type}/${filename}`, '_blank')
}

function onNav(page) {
  router.push({ name: page, params: { user_id: userId } })
}

onMounted(fetchReports)
</script>