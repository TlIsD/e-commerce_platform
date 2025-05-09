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
            title: "个人中心",
            keepAlive: true,
            authorization: true,
        },
        path: '/user',
        name: "User",
        component: ()=> import("../views/User.vue"),
        children: [
            {
                meta:{
                    title: "个人信息",
                    keepAlive: true,
                    authorization: true,
                },
                path: '',
                name: "UserInfo",
                component: ()=> import("../components/user/Info.vue"),
            },
            {
                meta:{
                    title: "我的订单",
                    keepAlive: true,
                    authorization: true,
                },
                path: 'order',
                name: "UserOrder",
                component: ()=> import("../components/user/Order.vue"),
            },
            {
                meta:{
                    title: "我的课程",
                    keepAlive: true,
                    authorization: true,
                },
                path: 'course',
                name: "UserCourse",
                component: ()=> import("../components/user/Course.vue"),
            },
        ]
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
    {
        meta:{
            title: '课程详情',
            keepAlive: true,
        },
        path: '/project/:id',
        name: 'Info',
        component: () => import('../views/Info.vue'),
    },
    {
        meta:{
            title: '购物车',
            keepAlive: true,
        },
        path: '/cart',
        name: 'Cart',
        component: () => import('../views/Cart.vue'),
    },
    {
        meta:{
            title: '下单',
            keepAlive: true,
        },
        path: '/order',
        name: 'Order',
        component: () => import('../views/Order.vue'),
    },
    {
        meta:{
            title: "支付成功",
            keepAlive: true
        },
        path: '/alipay',
        name: "PaySuccess",
        component: ()=> import("../views/AliPaySuccess.vue"),
    },
    {
        meta:{
            title: "学习中心",
            keepAlive: true,
            authorization: true
        },
        path: '/user/study/:course',
        name: "Study",
        component: ()=> import("../views/Study.vue"),
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