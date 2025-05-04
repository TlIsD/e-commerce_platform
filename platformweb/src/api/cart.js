import http from "../utils/http";
import {reactive, ref} from "vue"

const cart = reactive({
    course_list: [],  // 购物车中商品列表
    total_price: 0,  // 选中商品总价
    selected_course_total: 0,  // 选中商品数量

    // 添加课程到购物车
    add_course_to_cart(course_id, token) {
        return http.post("/cart/", {
            course_id: course_id
        }, {
            // 添加课程商品到购物车必须登录，所以接口操作时必须发送jwt
            headers: {
                Authorization: `jwt ${token}`,
            }
        })
    },

    // 获取购物车的商品列表
    get_course_from_cart(token){
        // 获取购物车的商品课程列表
        return http.get("/cart/", {
            headers:{
                Authorization: `jwt ${token}`,
            }
        })
    }
})

export default cart;