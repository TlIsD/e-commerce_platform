import http from "../utils/http.js";
import { reactive, ref } from "vue";

const nav = reactive({
    // 头部导航
    nav_header_list: [],
    get_nav_header(){
      return http.get("/nav/header/");
    },

    // 脚部导航
    nav_footer_list: [],
    get_nav_footer(){
        return http.get("/nav/footer/");
    }
})

export default nav;
