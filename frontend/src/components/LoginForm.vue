<template>
  <div class="container mt-5" style="max-width:400px;">
    <div class="card shadow">
      <div class="card-body">
        <h3 class="mb-4 text-center">Login</h3>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="email" id="email" type="email" class="form-control" required autofocus />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="password" id="password" type="password" class="form-control" required />
          </div>
          <button class="btn btn-primary w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            Login
          </button>
          <div class="text-center mt-3">
            <router-link to="/register" class="btn btn-link p-0">Don't have an account? Register</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiFetch } from '../api'
import { auth } from '../store/auth'

const email = ref('')
const password = ref('')
const loading = ref(false)
const router = useRouter()

async function handleSubmit() {
  loading.value = true
  try {
    const data = await apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email: email.value, password: password.value }),
    })
    auth.login(data.access_token)
    if (auth.state.user?.role === 'admin') {
      router.push('/admin/subjects')
    } else {
      router.push('/subjects')
    }
  } catch (err) {
    console.error('Login error:', err)
    // You might want to show an error message to the user here
  } finally {
    loading.value = false
  }
}
</script>
