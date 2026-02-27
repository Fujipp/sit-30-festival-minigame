import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('../views/HomeView.vue'),
    },
    {
        path: '/level',
        name: 'level',
        component: () => import('../views/LevelView.vue'),
    },
    {
        path: '/board',
        name: 'board',
        component: () => import('../views/BoardView.vue'),
    },
    {
        path: '/question',
        name: 'question',
        component: () => import('../views/QuestionView.vue'),
    },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

export default router
