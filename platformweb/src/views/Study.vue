<template>
  <div class="player">
    <div id="player"></div>
    <div class="chapter-list">
      <h2>{{course.course_info.name}}</h2>
      <el-tree
          v-if="course.current_lesson"
          highlight-current
          class="filter-tree"
          :data="course.lesson_list"
          default-expand-all
          node-key="id"
          @node-click="node_click"
          :current-node-key="`lesson-`+course.current_lesson"
      >
      </el-tree>
    </div>
  </div>
</template>

<script setup>
import {onMounted, reactive, watch} from "vue"
import http from "../utils/http"
import course from "../api/course"
import "../utils/player"
import {useRoute} from "vue-router"
import settings from "../settings"
const route = useRoute()

// 获取路由参数[课程ID]
course.course_id = route.params.course

// 获取课程信息
course.get_course().then(res=>{
  course.course_info = res.data
})

course.get_course_chapters().then(res=>{
  let ret = []
  let chapter_item = {}
  for(let chapter of res.data){
    chapter_item = {id: 'chapter-'+chapter.id, label: `${chapter.orders}. ${chapter.name}`, children: []}
    // 判断当前章节下如果有课时列表
    if(chapter.get_lesson_list.length>0){
      for(let lesson of chapter.get_lesson_list){
        chapter_item.children.push({id: 'lesson-'+lesson.id, label: `${chapter.orders}.${lesson.orders} ${lesson.name}`, lesson: lesson})
      }
    }
    ret.push(chapter_item)
  }

  course.lesson_list = ret
})

// 当用户点击右侧课程的章节课时的回调函数
const node_click = (data)=>{
  console.log(data.lesson.lesson_link)
  if(!data.lesson){
    return
  }

  let token = sessionStorage.token || localStorage.token
  course.get_lesson_study_time(data.lesson.id, token,).then(res=>{
    // 先删除原来的播放器
    try {
      course.player.destroy()
    } catch (error){}
    // 重置视频播放时间
    course.current_time = res.data

    // 重置当前播放的课时ID
    course.current_lesson = data.lesson.id

    // 新建一个播放器
    polyv(data.lesson.lesson_link)
  })
}

let polyv = (vid)=>{
  let token = sessionStorage.token || localStorage.token

  course.player = polyvPlayer({
    wrap: '#player',
    width: document.documentElement.clientWidth - 300, // 页面宽度
    height: document.documentElement.clientHeight,     // 页面高度
    forceH5: true,
    vid: vid,
    code: "root", // 一般是用户昵称
    // 视频加密播放的配置
    playsafe(vid, next){ // 向后端发送请求获取加密的token
      http.get(`courses/polyv/token/${vid}/`, {
        headers: {
          "Authorization": `jwt ${token}`
        }
      }).then(res=>{
        // 获取播放视频的token令牌
        next(res.data.token)
      })
    }
  })

  // 设置播放进度
  course.player.on('s2j_onPlayerInitOver',(e)=>{
    course.player.j2s_seekVideo(course.current_time)
  })

  // 设置自动播放，但是谷歌浏览器会拦截自动播放
  try {
    course.player.j2s_resumeVideo()
  } catch (error){

  }

  let video = document.querySelector(".pv-video")
  // 监听是否是否播放中
  video.ontimeupdate = ()=>{
    let time = parseInt(video.currentTime)
    console.log(time)
    if( time % settings.seed_time === 0 ){
      if(course.current_time < time){
        // 监听当前课时的播放时间
        course.current_time = time
      }
    }
  }

}

onMounted(()=>{
  // 页面加载完成以后，自动从服务端获取用户在当前课程课程的学习进度。【要直到当前学到第几章、第几节、什么时间？】
  let token = sessionStorage.token || localStorage.token

  course.get_user_course(token).then(res=>{
    // 获取到服务端返回的课程学习进度记录
    course.user_course = res.data   // 用户在当前课程的学习进度记录
    course.current_chapter = res.data.chapter_id  // 正在学习的章节ID
    course.current_lesson  = res.data.lesson_id  // 正在学习的课时ID
    course.lesson_link = res.data.lesson_link  // 当前正在学习的课时视频ID
    // 从学习进度记录中提取正在学习的课时的视频ID
    polyv(course.lesson_link)
  })

  // 监听当前浏览器窗口的大小是否发生变化，让播放器随着窗口变化大小
  window.onresize = ()=>{
    document.querySelector(".pv-video-player").style.width = `${document.documentElement.clientWidth - 300}px`
    document.querySelector(".pv-video-player").style.height = `${document.documentElement.clientHeight}px`
  }

  // 开始自动播放
  try {
    course.player.j2s_resumeVideo()
  } catch (error){

  }

})

watch(
    ()=>course.current_time,
    ()=>{
      let token = sessionStorage.token || localStorage.token
      let lesson = course.current_lesson
      if(isNaN(course.current_lesson)) {
        lesson = course.current_lesson.split('-')[1]
      }
      course.update_user_study_progress(lesson, settings.seed_time, token).then(res=>{
        console.log(res.data)
      })
    }
)

</script>

<style scoped>
.chapter-list{
  position: absolute;
  top: 0;
  right: 0;
  width: 300px;
  background-color: #ccc;
}
.chapter-list h2 {
  height: 40px;
  line-height: 40px;
  text-indent: 1rem;
}
</style>