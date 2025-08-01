<!-- src/components/SettingsPage.vue -->
<template>
  <div class="container py-4">
    <Navigation
      :is-admin="false"
      current-page="settings"
      @navigate="handleNavigate"
    />

    <div class="text-center mb-4">
      <h1 class="display-6 fw-bold" style="font-family: Montserrat, sans-serif;">
        Settings ⚙️
      </h1>
      <p class="text-muted">Customize your Recall experience</p>
    </div>

    <div class="row g-4">
      <!-- Notifications -->
      <div class="col-12 col-lg-6">
        <div class="card">
          <div class="card-header d-flex align-items-center gap-2">
            <i class="bi bi-bell fs-5 text-primary"></i>
            Notifications
          </div>
          <div class="card-body">
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="email_notifications"
                v-model="settings.email_notifications"
              />
              <label class="form-check-label" for="email_notifications">
                Email Notifications
                <div class="form-text">Receive updates via email</div>
              </label>
            </div>
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="quiz_reminders"
                v-model="settings.quiz_reminders"
              />
              <label class="form-check-label" for="quiz_reminders">
                Quiz Reminders
                <div class="form-text">Get reminded about scheduled quizzes</div>
              </label>
            </div>
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="achievement_alerts"
                v-model="settings.achievement_alerts"
              />
              <label class="form-check-label" for="achievement_alerts">
                Achievement Alerts
                <div class="form-text">Celebrate your milestones</div>
              </label>
            </div>
            <div class="form-check form-switch">
              <input
                class="form-check-input"
                type="checkbox"
                id="weekly_reports"
                v-model="settings.weekly_reports"
              />
              <label class="form-check-label" for="weekly_reports">
                Weekly Reports
                <div class="form-text">Summary of your weekly progress</div>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Privacy -->
      <div class="col-12 col-lg-6">
        <div class="card">
          <div class="card-header d-flex align-items-center gap-2">
            <i class="bi bi-shield-lock-fill fs-5 text-success"></i>
            Privacy & Security
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label for="profile_visibility" class="form-label">Profile Visibility</label>
              <select
                id="profile_visibility"
                class="form-select"
                v-model="settings.profile_visibility"
              >
                <option value="public">Public</option>
                <option value="friends">Friends Only</option>
                <option value="private">Private</option>
              </select>
            </div>
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="show_in_leaderboards"
                v-model="settings.show_in_leaderboards"
              />
              <label class="form-check-label" for="show_in_leaderboards">
                Show in Leaderboards
                <div class="form-text">Appear in public rankings</div>
              </label>
            </div>
            <div class="form-check form-switch">
              <input
                class="form-check-input"
                type="checkbox"
                id="share_progress"
                v-model="settings.share_progress"
              />
              <label class="form-check-label" for="share_progress">
                Share Progress
                <div class="form-text">Allow others to see your achievements</div>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Appearance -->
      <div class="col-12 col-lg-6">
        <div class="card">
          <div class="card-header d-flex align-items-center gap-2">
            <i class="bi bi-palette-fill fs-5 text-purple"></i>
            Appearance
          </div>
          <div class="card-body">
            <div class="mb-3" v-for="opt in appearanceOptions" :key="opt.key">
              <label :for="opt.key" class="form-label">{{ opt.label }}</label>
              <select
                :id="opt.key"
                class="form-select"
                v-model="settings[opt.key]"
              >
                <option v-for="item in opt.choices" :key="item.value" :value="item.value">
                  {{ item.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Preferences -->
      <div class="col-12 col-lg-6">
        <div class="card">
          <div class="card-header d-flex align-items-center gap-2">
            <i class="bi bi-gear-fill fs-5 text-warning"></i>
            Quiz Preferences
          </div>
          <div class="card-body">
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="auto_submit"
                v-model="settings.auto_submit"
              />
              <label class="form-check-label" for="auto_submit">
                Auto-submit Quizzes
                <div class="form-text">Automatically submit when time runs out</div>
              </label>
            </div>
            <div class="form-check form-switch mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                id="show_correct_answers"
                v-model="settings.show_correct_answers"
              />
              <label class="form-check-label" for="show_correct_answers">
                Show Correct Answers
                <div class="form-text">Display answers after quiz completion</div>
              </label>
            </div>
            <div class="mb-3">
              <label for="difficulty_preference" class="form-label">Difficulty Preference</label>
              <select
                id="difficulty_preference"
                class="form-select"
                v-model="settings.difficulty_preference"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
                <option value="adaptive">Adaptive</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Save Button -->
      <div class="col-12 text-center">
        <button class="btn btn-primary btn-lg" @click="handleSave">
          <i class="bi bi-save me-2"></i>
          Save All Settings
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Navigation from './Navigation.vue'

const props = defineProps({
  showSystemMessage: Function,
  navigate: Function
})

const settings = ref({
  email_notifications: true,
  quiz_reminders: true,
  achievement_alerts: true,
  weekly_reports: false,
  profile_visibility: "public",
  show_in_leaderboards: true,
  share_progress: false,
  theme: "light",
  language: "en",
  timezone: "UTC",
  auto_submit: false,
  show_correct_answers: true,
  difficulty_preference: "adaptive",
})

const appearanceOptions = [
  {
    key: 'theme',
    label: 'Theme',
    choices: [
      { value: 'light', text: 'Light' },
      { value: 'dark', text: 'Dark' },
      { value: 'system', text: 'System' },
    ]
  },
  {
    key: 'language',
    label: 'Language',
    choices: [
      { value: 'en', text: 'English' },
      { value: 'es', text: 'Español' },
      { value: 'fr', text: 'Français' },
      { value: 'de', text: 'Deutsch' },
    ]
  },
  {
    key: 'timezone',
    label: 'Timezone',
    choices: [
      { value: 'UTC', text: 'UTC' },
      { value: 'EST', text: 'Eastern Time' },
      { value: 'PST', text: 'Pacific Time' },
      { value: 'GMT', text: 'GMT' },
    ]
  },
]

function handleSave() {
  props.showSystemMessage("/api/users/settings", settings.value)
}
</script>