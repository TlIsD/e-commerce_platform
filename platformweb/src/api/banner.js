import http from "../utils/http.js";
import { reactive, ref } from "vue";

const banner = reactive({
    // 头部导航
    banner_list: [],
    get_banner(){
        return http.get("/banner/");
    }
})

export default banner;
