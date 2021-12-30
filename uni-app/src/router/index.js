import Vue from "vue"
import Router from 'vue-router'

Vue.use(Router)

// import Layout from '@/layout'


export const constantRoutes = [
    {
        path: '/login',
        component: () => import('@/pages/users/index'),
        hidden: true
    }
]