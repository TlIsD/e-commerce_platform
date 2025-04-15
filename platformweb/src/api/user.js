import http from '../utils/http.js'
import {reactive, ref} from "vue";

const user = reactive({
    login_type: 0,
    account: localStorage.getItem('account'),  // 用户名/手机号/邮箱
    password: localStorage.getItem('password'),
    remember: localStorage.getItem('remember'),
    phone:'',
    captcha: '',

    // 登录请求处理
    login(res){
        return http.post('/users/login/', {
            'ticket': res.ticket,
            'randstr': res.randstr,
            'username': this.account,
            'password': this.password,
        })
    }
})

export default user