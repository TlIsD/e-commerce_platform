import http from '../utils/http.js'
import {reactive, ref} from "vue";

const user = reactive({
    login_type: 0,
    rem_account: localStorage.getItem('rem_account'),  // 用户名/手机号/邮箱
    account: '',
    rem_password: localStorage.getItem('rem_password'),
    password: '',
    remember: localStorage.getItem('remember'),
    phone:'',
    captcha: '',
    r_password:'',  // 注册密码
    re_password: '',  // 确认密码
    captcha_interval: 60, //短信发送冷却时间
    interval: null, // 定时器
    captcha_btn_text: '点击获取验证码',

    // 登录请求处理
    login(res){
        if (this.login_type === 0){
            return http.post('/users/login/', {
                'ticket': res.ticket,
                'randstr': res.randstr,
                'type': this.login_type,
                'username': this.account,
                'password': this.password,
            })

        }else if (this.login_type === 1){
            return http.get(`/users/phone_login/${this.phone}`, {
                'ticket': res.ticket,
                'randstr': res.randstr,
                'type': this.login_type,
            })
        }
    },

    check_phone(res){
        return http.get(`/users/phone/${this.phone}/`)
    },

    // 注册请求处理
    register(data){
        data.phone = this.phone
        data.password = this.password
        data.sms_captcha = this.captcha
        return http.post('/users/register/', data)
    },

    get_sms_captcha(){
        return http.get(`/users/code/${this.phone}/`)
    }
})

export default user