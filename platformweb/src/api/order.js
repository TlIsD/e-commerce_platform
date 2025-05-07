import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
    total_price: 0,  // 勾选商品的总价格
    use_coupon: false,  // 用户是否使用优惠
    discount_price: 0,  // 本次下单的优惠抵扣价格
    discount_type: 0,  // 0表示优惠券，1表示积分
    coupon_list:[],  // 用户拥有的可用优惠券列表
    select: -1,  // 当前用户选中的优惠券下标，-1表示没有选择
    credit: 0,  // 当前用户选择抵扣的积分
    fixed: true,  // 底部订单总价是否固定浮动
    pay_type: 0,  // 支付方式

    credit_to_money: 0,  // 积分兑换现金的比例
    has_credit: 0,       // 用户拥有的积分

    max_use_credit: 0,   // 当前用户本次下单可用最大积分数量
    credit_course_list:[], // 可使用积分抵扣的课程列表

    course_list: [],     // 本次购买的商品课程列表
    real_price: 0,       // 付款金额
    pay_time: undefined, // 付款时间
    is_show: true,  // 是否展示支付成功页面

    // 生成订单
    create_order(user_coupon_id, token){
        return http.post("/orders/",{
            pay_type: this.pay_type,
            user_coupon_id,
            credit: this.credit,
        }, {
            headers:{
                Authorization: `jwt ${token}`,
            }
        })
    },
    // 获取本次下单的可用优惠券列表
    get_enable_coupon_list(token){
        return http.get("/coupon/enable/",{
            headers:{
                Authorization: `jwt ${token}`,
            }
        })
    },
    // 获取订单的支付宝支付链接信息
    alipay_page_pay(order_number){
        return http.get(`/payments/alipay/${order_number}/`)
    },
    // 把地址栏中的查询字符串(支付成功以后的同步回调通知)转发给后端
    relay_alipay_result(query_string){
        return http.get(`/payments/alipay/result/${query_string}`)
    }
})

export default order;