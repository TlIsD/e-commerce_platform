import http from "../utils/http.js";
import { reactive, ref } from "vue";

const course = reactive({
    current_direction: 0,  // 当前选中的学习方向
    direction_list:[],
    current_category: 0,  // 当前选中的课程分类
    category_list:[],
    course_list:[],

    // 获取学习方向信息
    get_course_direction(){
        return http.get('/courses/directions/')
    },

    // 获取课程分类信息
    get_course_category(){
        return http.get(`/courses/categories/${this.current_direction}/`);
    },

    // 获取课程列表信息
    get_course_list(){
        return http.get(`/courses/${this.current_direction}/${this.current_category}/`);
    }
})

export default course;