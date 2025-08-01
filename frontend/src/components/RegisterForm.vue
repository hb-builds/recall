<template>
  <div class="container mt-5" style="max-width:450px;">
    <div class="card shadow">
      <div class="card-body">
        <h3 class="mb-4 text-center">Register</h3>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label class="form-label">Full Name</label>
            <input v-model="full_name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Qualification</label>
            <input v-model="qualification" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label">Date of Birth</label>
            <input v-model="dob" type="date" class="form-control" required />
          </div>
          <button class="btn btn-success w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Register
          </button>
          <div class="text-center mt-3">
            <router-link to="/login" class="btn btn-link p-0">Already have an account? Login</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { apiFetch } from '../api'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const full_name = ref('')
const qualification = ref('')
const dob = ref('')
const loading = ref(false)
const router = useRouter()

async function handleSubmit() {
  loading.value = true
  try {
    await apiFetch('/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        full_name: full_name.value,
        qualification: qualification.value,
        dob: dob.value,
      }),
    })
    // Registration successful
    router.push('/login')
  } catch (err) {
    console.error('Registration error:', err)
  } finally {
    loading.value = false
  }
}
</script>