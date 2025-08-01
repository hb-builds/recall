<template>
  <nav class="bg-white border-bottom px-4 py-3 shadow-sm">
    <div class="d-flex align-items-center justify-content-between mx-auto" style="max-width: 1100px;">
      <!-- Left side - Navigation Links -->
      <div class="d-flex align-items-center gap-2">
        <button
          :class="['btn btn-sm rounded-pill', currentPage === 'subjects' ? 'btn-primary' : 'btn-outline-secondary']"
          @click="handleNavigate('subjects')"
        >
          <i class="bi bi-house me-1"></i><span class="d-none d-sm-inline">Home</span>
        </button>
        <button
          :class="['btn btn-sm rounded-pill', currentPage === 'history' ? 'btn-primary' : 'btn-outline-secondary']"
          @click="handleNavigate('history')"
        >
          <i class="bi bi-clock-history me-1"></i><span class="d-none d-sm-inline">History</span>
        </button>
        <button
          :class="['btn btn-sm rounded-pill', currentPage === 'reports' ? 'btn-primary' : 'btn-outline-secondary']"
          @click="handleNavigate('reports')"
        >
          <i class="bi bi-file-earmark-text me-1"></i><span class="d-none d-sm-inline">Reports</span>
        </button>
        <button
          v-if="isAdmin"
          :class="['btn btn-sm rounded-pill', currentPage.startsWith('admin') ? 'btn-primary' : 'btn-outline-secondary']"
          @click="handleNavigate('admin-subjects')"
        >
          <i class="bi bi-gear me-1"></i><span class="d-none d-sm-inline">Admin</span>
        </button>
      </div>

      <!-- Right side - User dropdown -->
      <div class="d-flex align-items-center gap-3">
        <div class="d-none d-md-block text-end">
          <div class="fw-semibold">{{ userName }}</div>
          <div class="text-muted small">{{ userEmail }}</div>
        </div>
        <div class="dropdown">
          <button
            class="btn btn-light rounded-circle p-0 d-flex align-items-center"
            type="button"
            data-bs-toggle="dropdown"
          >
            <div
              class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
              style="width: 38px; height: 38px;"
            >
              <span class="fw-bold">{{ initials }}</span>
            </div>
            <i class="bi bi-chevron-down ms-2 d-none d-sm-block"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-end">
            <li class="d-md-none px-3 py-2">
              <div class="fw-semibold">{{ userName }}</div>
              <div class="text-muted small">{{ userEmail }}</div>
            </li>
            <li><hr class="dropdown-divider d-md-none" /></li>
            <li>
              <button class="dropdown-item" @click="handleNavigate('profile')">
                <i class="bi bi-person me-2"></i> View Profile
              </button>
            </li>
            <li>
              <button class="dropdown-item" @click="handleNavigate('settings')">
                <i class="bi bi-gear me-2"></i> Settings
              </button>
            </li>
            <li><hr class="dropdown-divider" /></li>
            <li>
              <button class="dropdown-item text-danger" @click="logout">
                <i class="bi bi-box-arrow-right me-2"></i> Sign Out
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../store/auth'

export default defineComponent({
  name: 'AppNavigation',
  props: {
    currentPage: { type: String, default: '' }
  },
  setup() {
    const router = useRouter()
    const user = computed(() => auth.state.user)
    const isAdmin = computed(() => user.value?.role === 'admin')

    const userName = computed(() => {
      if (!user.value) return ''
      const role = user.value.role.charAt(0).toUpperCase() + user.value.role.slice(1)
      return `${role} (ID: ${user.value.id})`
    })
    const userEmail = computed(() => '') // Email is not available in the token

    const initials = computed(() => {
      if (!user.value) return ''
      return user.value.role.charAt(0).toUpperCase()
    })

    function handleNavigate(page) {
      const routes = {
        'subjects': { name: 'subjects' },
        'history': { name: 'history', params: { user_id: user.value.id } },
        'reports': { name: 'reports' },
        'admin-subjects': { name: 'admin-subjects' },
        'profile': { name: 'profile' },
        'settings': { name: 'settings' }
      }
      if (routes[page]) {
        router.push(routes[page])
      }
    }

    return {
      userName,
      userEmail,
      initials,
      isAdmin,
      logout: auth.logout,
      handleNavigate
    }
  }
})
</script>