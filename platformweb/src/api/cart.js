import http from "../utils/http";
import {reactive, ref} from "vue"

const cart = reactive({
    course_list: [],  // 购物车中商品列表
    total_price: 0,  // 选中商品总价
    selected_course_total: 0,  // 选中商品数量
    checked: false,  // 是否全选

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
        return http.get("/cart/", {
            headers:{
                Authorization: `jwt ${token}`,
            }
        })
    },
    // 切换指定商品课程的勾选状态
    select_course(course_id, selected, token){
        return http.patch("/cart/", {
            course_id,
            selected,
        },{
            headers:{
                Authorization: `jwt ${token}`,
            }
        })
    },
    // 切换购物车全选/全不选状态
    select_all_course(selected, token){
        return http.put("/cart/", {
            selected,
        },{
            headers:{
                Authorization: `jwt ${token}`,
            }
        })
    },
    // 从购物车中删除商品课程
    delete_course(course_id, token){
        return http.delete("/cart/", {
            params:{
                course_id,
            },
            headers:{
                Authorization: "jwt " + token,
            }
        })
    }
})

export default cart;