import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../store/auth'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'
import SubjectsPage   from '../components/SubjectsPage.vue'
import ChaptersPage   from '../components/ChaptersPage.vue'
import QuizzesPage from '../components/QuizzesPage.vue'
import QuizDetailPage  from '../components/QuizDetailPage.vue'
import AttemptDetailPage from '../components/AttemptDetailPage.vue'
import AdminSubjectsPage  from '../components/AdminSubjectsPage.vue'
import AdminChaptersPage  from '../components/AdminChaptersPage.vue'
import AdminQuizzesPage   from '../components/AdminQuizzesPage.vue'
import AdminQuestionsPage from '../components/AdminQuestionsPage.vue'
import QuizLeaderboardPage from '../components/QuizLeaderboardPage.vue'
import UserRankingPage     from '../components/UserRankingPage.vue'
import MonthlyAnalyticsPage from '../components/MonthlyAnalyticsPage.vue'
import QuizDifficultyPage   from '../components/QuizDifficultyPage.vue'
import ProfilePage from '../components/ProfilePage.vue'
import ReportsPage  from '../components/ReportsPage.vue'
import SettingsPage from '../components/SettingsPage.vue'
import ExportsPage from '../components/ExportsPage.vue'
import HistoryPage from '../components/HistoryPage.vue'

const routes = [
{
    path: '/',
    redirect: () => {
      if (auth.state.user) {
        return auth.state.user.role === 'admin' ? '/admin/subjects' : '/subjects'
      }
      return '/login'
    }
  },
  { path: '/login', component: LoginForm },
  { path: '/register', component: RegisterForm },
  { path: '/subjects', name: 'subjects', component: SubjectsPage },
  { path: '/chapters/:subject_id', name: 'chapters', component: ChaptersPage, props: true },
  { path: '/quizzes/:chapter_id', name: 'quizzes', component: QuizzesPage,props: true },
  { path: '/quiz/:quiz_id', name: 'quiz-detail', component: QuizDetailPage, props: true },
  { path: '/attempt/:attempt_id', name: 'attempt-detail', component: AttemptDetailPage, props: true },
  { path:'/admin/subjects',  name:'admin-subjects',  component:AdminSubjectsPage  },
  { path:'/admin/chapters',  name:'admin-chapters',  component:AdminChaptersPage  },
  { path:'/admin/quizzes',   name:'admin-quizzes',   component:AdminQuizzesPage   },
  { path:'/admin/questions', name:'admin-questions', component:AdminQuestionsPage },
  { path:'/leaderboard/quiz/:quiz_id', name:'quiz-leaderboard', component:QuizLeaderboardPage, props:true },
  { path:'/leaderboard/user/:user_id', name:'user-ranking',    component:UserRankingPage,    props:true },
  { path:'/analytics/user/:user_id', name:'monthly-analytics', component:MonthlyAnalyticsPage, props:true },
  { path:'/analytics/quiz/:quiz_id', name:'quiz-difficulty',   component:QuizDifficultyPage,   props:true },
  { path:'/reports',  name:'reports',  component:ReportsPage  },
  { path:'/settings', name:'settings', component:SettingsPage },
  { path:'/exports/:user_id', name:'exports', component:ExportsPage, props:true },
  { path:'/history/:user_id', name:'history', component:HistoryPage, props:true },
  { path: '/profile', name: 'profile', component: ProfilePage }
]
  // ...other routes

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router