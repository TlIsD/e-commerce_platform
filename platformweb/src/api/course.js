import http from "../utils/http.js";
import { reactive, ref } from "vue";

const course = reactive({
    current_direction: 0,  // 当前选中的学习方向
    direction_list:[],
    current_category: 0,  // 当前选中的课程分类
    category_list:[],
    course_list:[],

    ordering: '-id',  // 课程排序条件
    page: 1,  // 当前页码
    size: 8,  // 当前页数据量
    count: 0,  // 课程列表的数量
    has_perv: false,  // 是否有上一页
    has_next: false,  // 是否有下一页
    timer: null,  // 定时器

    text: "",  // 搜索框内容
    hot_word_list: [],  // 热词列表

    course_id: null,  // 课程id
    info:{
      teacher: {},  // 课程相关教师信息
      discount: {  // 课程相关折扣信息
          type: ''
      },
    },
    tabIndex: 1,  // 课程详情页默认展示的选项卡

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
        let params = {
            page: this.page,
            size: this.size,
        }
        if(this.ordering){
            params.ordering = this.ordering;
        }
        return http.get(`/courses/${this.current_direction}/${this.current_category}/`, {params: params});
    },

    // 课程优惠时间倒计时
    start_timer(){
        clearTimeout(this.timer);
        this.timer = setInterval(() => {
            this.course_list.forEach(course => {
                if (course.discount.expire && course.discount.expire > 0){
                    course.discount.expire--
                }
            })
        }, 1000)
    },

    // 课程搜索
    search_course(){
        let params = {
            page: this.page,
            size: this.size,
            text: this.text,
        }
        if (this.ordering){
            params['ordering'] = this.ordering
        }
        return http.get(`/courses/search/`, {params})
    },

    // 课程热搜关键词
    get_hot_word(){
        return http.get('/courses/hotword/')
    },

    // 课程详情信息
    get_course(){
        return http.get(`/courses/${this.course_id}`)
    }
})

export default course;