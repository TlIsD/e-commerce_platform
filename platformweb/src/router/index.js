import {createRouter, createWebHistory} from "vue-router";
import store from "../store/index.js";

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
    {
        meta:{
            title: '注册',
            keepAlive: true,
        },
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
    },
    {
        meta:{
            title: '个人中心',
            keepAlive: true,
            authorization: true,  // 是否要验证
        },
        path: '/user',
        name: 'User',
        component: () => import('../views/User.vue'),
    },
    {
        meta:{
            title: '课程信息',
            keepAlive: true,
        },
        path: '/project',
        name: 'Course',
        component: () => import('../views/Course.vue'),
    },
]

// 实例化
const router = createRouter({
    // 指定路由模式
    history: createWebHistory(),
    routes,
});

// 导航守卫
router.beforeEach((to, from, next) => {
    document.title = to.meta.title
    if(to.meta.authorization && !store.getters.getUserInfo){
        next({name: 'Login'})
    }else {
        next()
    }
})

export default router;