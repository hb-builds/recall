<!-- src/components/ReportsPage.vue -->
<template>
  <div>
    <Navigation
      :is-admin="false"
      current-page="reports"
    />

    <div class="container py-4">
      <div class="text-center mb-4">
        <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
          Analytics & Reports 📈
        </h1>
        <p class="text-muted">Dive deep into your learning analytics</p>
      </div>

      <div class="row row-cols-1 row-cols-md-2 g-4">
        <div v-for="(card, i) in cards" :key="i" class="col">
          <div
            class="card h-100 cursor-pointer shadow-sm"
            @click="card.action"
          >
            <div class="card-body d-flex flex-column">
              <div class="d-flex align-items-center mb-3">
                <div :class="['p-3 rounded', card.colorClass]">
                  <i :class="card.iconClass" class="fs-4"></i>
                </div>
                <h5 class="card-title mb-0">{{ card.title }}</h5>
              </div>
              <p class="text-muted flex-grow-1">{{ card.description }}</p>
              <button class="btn btn-outline-primary mt-auto align-self-start">
                View Report
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center text-secondary small mt-4">
        📊 Use these insights to identify areas for improvement
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { auth } from '../store/auth'
import Navigation from './Navigation.vue'

const router = useRouter()
const userId = auth.state.user.id

const cards = [
  {
    title: "Monthly Performance",
    description: "Track your average scores over time",
    iconClass: "bi bi-bar-chart-line",
    colorClass: "bg-primary text-white",
    action: () => router.push({ name: "monthly-analytics", params: { user_id: userId } }),
  },
  {
    title: "Quiz Leaderboards",
    description: "See how you rank against other students",
    iconClass: "bi bi-trophy-fill",
    colorClass: "bg-success text-white",
    action: () => router.push({ name: "quiz-leaderboard", params: { quiz_id: "1" } }),
  },
  {
    title: "Your Global Ranking",
    description: "Your position among all users",
    iconClass: "bi bi-people-fill",
    colorClass: "bg-warning text-dark",
    action: () => router.push({ name: "user-ranking", params: { user_id: userId } }),
  },
  {
    title: "Quiz Difficulty Analysis",
    description: "Understand which questions are most challenging",
    iconClass: "bi bi-graph-down",
    colorClass: "bg-secondary text-white",
    action: () => router.push({ name: "quiz-difficulty", params: { quiz_id: "1" } }),
  },
]
</script>

<style scoped>
.cursor-pointer { cursor: pointer; }
.shadow-sm      { transition: box-shadow .2s; }
.shadow-sm:hover { box-shadow: 0 .5rem 1rem rgba(0,0,0,.15); }
</style>