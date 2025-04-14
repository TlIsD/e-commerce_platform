import http from '../utils/http.js'
import {reactive, ref} from "vue";

const user = reactive({
    login_type: 0,
    account: '',  // 用户名/手机号/邮箱
    password: '',
    remember: false,
    phone:'',
    captcha: '',

    // 登录请求处理
    login(){
        return http.post('/users/login/', {
            'username': user.account,
            'password': user.password,
        })
    }
})

export default user