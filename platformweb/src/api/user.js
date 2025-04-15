import http from '../utils/http.js'
import {reactive, ref} from "vue";

const user = reactive({
    login_type: 0,
    account: localStorage.getItem('account'),  // 用户名/手机号/邮箱
    password: localStorage.getItem('password'),
    remember: localStorage.getItem('remember'),
    phone:'',
    captcha: '',
    r_password:'',  // 注册密码
    re_password: '',  // 确认密码

    // 登录请求处理
    login(res){
        return http.post('/users/login/', {
            'ticket': res.ticket,
            'randstr': res.randstr,
            'username': this.account,
            'password': this.password,
        })
    },

    check_phone(res){
        return http.get(`/users/phone/${this.phone}/`)
    }
})

export default user