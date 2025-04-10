import {createRouter, createWebHistory} from "vue-router";

// 路由列表
const routes = [
    {
        meta:{
            title: '首页',
            keepAlive: true,
        },
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue'),
    },
    {
        meta:{
            title: '登录',
            keepAlive: true,
        },
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
    },
]

// 实例化
const router = createRouter({
    // 指定路由模式
    history: createWebHistory(),
    routes,
});

export default router;