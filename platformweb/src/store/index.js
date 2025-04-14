import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

export default createStore({
    plugins: [createPersistedState()],

    state(){
        // 相当于data
        return {
            user:{

            }
        }
    },

    getters: {
        getUserInfo(state){
            let now = parseInt(new Date() / 1000)
            if(state.user.exp === undefined || parseInt(state.user.exp) < now){
                // 未登录或登录过期
                state.user = {}
                localStorage.token = null
                sessionStorage.token = null
                return null
            }

            return state.user
        }
    },

    mutations:{
        // 相当于method
        login(state, user){
            state.user = user
        },
        logout(state){
            state.user = {}
            localStorage.token = null
            sessionStorage.token = null
        }
    }
})