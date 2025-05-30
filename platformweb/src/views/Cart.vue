<template>
  <div class="cart">
    <Header/>
    <div class="cart-main">
      <div class="cart-header">
        <div class="cart-header-warp">
          <div class="cart-title left">
            <h1 class="left">我的购物车</h1>
            <div class="left">
              共<span>{{cart.course_list.length}}</span>门，已选择<span>{{cart.selected_course_total}}</span>门
            </div>
          </div>
          <div class="right">
            <div class="">
              <span class="left"><router-link class="myorder-history" to="/myorder">我的订单列表</router-link></span>
            </div>
          </div>
        </div>
      </div>
      <div class="cart-body" id="cartBody">
        <div class="cart-body-title">
          <el-row class="full">
            <el-col :span="3">
              <div class="item-1 l"><el-checkbox v-model="cart.checked">全选</el-checkbox></div>
            </el-col>
            <el-col :span="11">
              <div class="item-2 l"><span class="course">课程</span></div>
            </el-col>
            <el-col :span="9">
              <div class="item-3 l"><span>金额</span></div>
            </el-col>
            <el-col :span="1">
              <div class="l"><span>操作</span></div>
            </el-col>
          </el-row>
        </div>
        <div class="cart-body-table">
          <div class="item" v-for="(course_info, key) in cart.course_list">
            <el-row class="full">
              <el-col :span="3">
                <div class="item-1">
                  <el-checkbox v-model="course_info.selected" @change="change_select_course(course_info)"></el-checkbox>
                </div>
              </el-col>
              <el-col :span="11">
                <div class="item-2">
                  <router-link class="img-box l" :to="`/project/${course_info.id}`">
                    <img :src="course_info.course_cover">
                  </router-link>
                  <dl class="l has-package">
                    <dt>【{{ course_info.course_type }}】{{ course_info.name }}</dt>
                    <p class="package-item" v-if="course_info.discount.type">{{ course_info.discount.type }}</p>
                    <p class="package-item" v-if="course_info.credit>0">可用{{course_info.credit}}积分抵扣</p>
                  </dl>
                </div>
              </el-col>
              <el-col :span="9">
                <div class="item-3 col">
                  <div class="price" v-if="course_info.discount.price>=0">
                    <span class="discount-price"><em>￥</em><span>{{course_info.discount.price.toFixed(2)}}</span></span><br>
                    <span class="original-price"><em>￥</em><span>{{course_info.price.toFixed(2)}}</span></span>
                  </div>
                  <div class="price" v-else>
                    <div class="discount-price"><em>￥</em><span>{{course_info.price.toFixed(2)}}</span></div>
                  </div>
                </div>
              </el-col>
              <el-col :span="1">
                <div class="item-4">
                  <el-popconfirm title="您确认要从购物车删除当前课程吗？" @confirm="del_cart(key)" confirmButtonText="删除！" cancelButtonText="手滑了！">
                    <template #reference>
                      <el-icon :size="26" class="close"><Close /></el-icon>
                    </template>
                  </el-popconfirm>
                </div>
              </el-col>
            </el-row>
          </div>

          <div class="cart-body-bot fixed">
            <div class=" cart-body-bot-box">
              <div class="right">
                <div class="add-coupon-box">
                  <div class="li-left">
                    <div class="li-2">
                      <span class="topdiv w70">总计金额：</span>
                      <span class="price price-red w100">
                        <em>￥</em>
                        <span>{{cart.total_price.toFixed(2)}}</span>
                      </span>
                    </div>
                  </div>
                  <div class="li-3"><router-link to="/order" class="btn">去结算</router-link></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer/>
  </div>
</template>

<script setup>
import {Close} from '@element-plus/icons-vue'
import {reactive, watch} from "vue"
import Header from "../components/Header.vue"
import Footer from "../components/Footer.vue"
import cart from '../api/cart.js'
import { ElMessage } from 'element-plus'
import {useStore} from "vuex"

const store = useStore()

// 获取购物车中的商品列表
const get_cart = () => {
  let token = sessionStorage.token || localStorage.token
  cart.get_course_from_cart(token).then(res=>{
    cart.course_list = res.data.cart

    get_cart_total()

    // 监听课程的勾选状态是否发生
    watch(
        [...cart.course_list],
        ()=>{
          get_cart_total();
        },
    )
  }).catch(err=>{
    if(err?.response?.status === 400){
      store.commit('logout')
      ElMessage.error('登录超时，请重新登录~')
    }
  })
}

get_cart()

// 获取商品总价
const get_cart_total = () => {
  let sum = 0
  let select_sum = 0
  cart.course_list.forEach((course, key)=>{
    if(course.selected){
      // 是否被勾选
      select_sum ++
      // 是否有优惠
      if(course.discount.price >= 0){
        sum += course.discount.price
      }else{
        sum += course.price
      }
    }
    cart.total_price = sum
    cart.selected_course_total = select_sum
  })
}

const change_select_course = (course)=>{
  // 切换指定课程的勾选状态
  let token = sessionStorage.token || localStorage.token;

  // 有一个没被选中就取消全选
  if(!(cart.selected_course_total === cart.course_list.length)){
    cart.checked = false
  }
  cart.select_course(course.id, course.selected, token).catch(error=>{
    ElMessage.error(error?.response?.data?.errmsg);
  })
}

// 监听全选按钮的状态切换
watch(
    ()=>cart.checked,
    ()=>{
      let token = sessionStorage.token || localStorage.token;
      // 如果全选，则所有课程的勾选状态都为true
      if(cart.checked){
        // 让客户端的所有课程状态先改变
        cart.course_list.forEach((course, key)=>{
          course.selected = true
        })

        // 所有课程的勾选状态都为true的情况下，不要发送全选的ajax请求
        if(!(cart.selected_course_total === cart.course_list.length)){
          cart.select_all_course(true, token)
        }
      }

      // 所有课程的勾选状态都为true的情况下，把全选去掉，所有课程的勾选状态也变成false
      if((cart.checked === false) && (cart.selected_course_total === cart.course_list.length)){
        cart.course_list.forEach((course, key)=>{
          course.selected = false
        })
        cart.select_all_course(false,token)
      }
    }
)

const del_cart = (key)=>{
  // 从购物车中删除商品课程
  let token = sessionStorage.token || localStorage.token;
  let course = cart.course_list[key];
  console.log("course", course)
  cart.delete_course(course.id, token).then(res=>{
    // 当课程的勾选状态为True时，删除课程以后，把已勾选状态的课程总数-1
    cart.course_list.splice(key, 1);
    // 在store中页要同步购物车商品总数量
    store.commit("cart_total", cart.course_list.length);
    // 重新计算购物车中的商品课程的总价格
    get_cart_total();
  })
}

</script>

<style scoped>
.full{
  width: 100%;
}

.cart-header {
  height: 160px;
  background: #e3e6e9 url("/src/assets/cart-header-bg.jpeg") repeat-x;
  background-size: cover;
  width: 100%;
}

.cart-header .cart-header-warp {
  width: 100%;
  height: 120px;
  line-height: 120px;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5px;
  font-size: 14px
}

.cart-header .cart-header-warp .myorder-history {
  margin-right: 16px;
  font-weight: 200
}

.cart-header .left {
  margin-left: 10px;
  float: left
}

.cart-header .right {
  float: right
}

.cart-header .cart-title {
  color: #4d555d;
  font-weight: 200;
  font-size: 14px
}

.cart-header .cart-title h1 {
  font-size: 32px;
  line-height: 115px;
  margin-right: 25px;
  color: #07111b;
  font-weight: 200
}

.cart-header .cart-title span {
  margin: 0 4px
}

.cart-header .cart-title .js-number-box-cart {
  line-height: 115px
}

.cart-header .num {
  display: none;
  padding: 4px 5px;
  background-color: #f01414;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  font-size: 12px;
  line-height: 10px;
  margin-top: 51px;
  margin-left: 5px
}

.l {
  float: left;
}

.cart-body {
  width: 100%;
  padding: 0 36px 32px;
  background-color: #fff;
  margin-top: -40px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 16px 0 rgba(7,17,27,.1);
  border-radius: 8px;
  box-sizing: border-box
}

.cart-body .left {
  float: left!important
}

.cart-body .right {
  float: right!important
}

.cart-body .cart-body-title {
  width: 100%;
  min-height: 88px;
  line-height: 88px;
  border-bottom: 1px solid #b7bbbf;
  box-sizing: border-box
}

.cart-body .priceprice i {
  float: left
}

body {
  background: #f8fafc
}

.cart-body .cart-body-title span {
  font-size: 14px
}

.cart-body .cart-body-title .item-1>span,
.cart-body .cart-body-title .item-2>span,
.cart-body .cart-body-title .item-3>span,
.cart-body .cart-body-title .item-4>span {
  display: inline-block;
  font-size: 14px;
  line-height: 24px;
  color: #4d555d
}

.cart-body .cart-body-title .item-1>span {
  color: #93999f
}

.cart-body .cart-body-title .item-2>span {
  margin-left: 55px
}
.cart-body .cart-body-title .item-2 .course{
  line-height: 88px;
}
.cart-body .cart-body-title .item-4>span {
  margin-right: 21px;
}

.cart-body .cart-body-table .title .title-content span {
  margin-right: 9px;
  position: relative
}

.cart-body .cart-body-table .title .title-content span::after {
  content: "/";
  position: absolute;
  right: -9px
}

.cart-body .cart-body-table .title .title-content span:last-child::after {
  content: ''
}

.cart-body .item {
  height: 88px;
  padding: 24px 0;
  border-bottom: 1px solid #d9dde1
}

.cart-body .item>div {
  float: left
}

.cart-body .item .item-1 {
  padding-top: 34px;
  position: relative;
  z-index: 1
}

.cart-body .item:last-child>.item-1::after {
  display: none
}

.cart-body .item.disabled .price,.cart-body .item.disabled dt {
  color: #93999f!important
}

.cart-body .item-1 {
  width: 120px
}

.cart-body .item-1 i {
  margin-left: 12px;
  margin-right: 8px;
  font-size: 24px
}

.cart-body .item-2 {
  position:relative;
}
.cart-body .item-2>span{
  line-height: 88px;
}
.cart-body .item-2 dl {
  margin-left: 24px;
  padding-top: 12px
}

.cart-body .item-2 dl a {
  display: block;
}

.cart-body .item-2 dl.has-package {
  padding-top: 4px;
}

.cart-body .item-2 dl.has-package .package-item {
  display: inline-block;
  padding: 0 12px;
  margin-top: 4px;
  font-size: 12px;
  color: rgba(240,20,20,.6);
  line-height: 24px;
  background: rgba(240,20,20,.08);
  border-radius: 12px;
  cursor: pointer
}

.cart-body .item-2 dl.has-package .package-item:hover {
  color: #fff;
  background: rgba(240,20,20,.2)
}

.cart-body .item-2 dt {
  font-size: 16px;
  color: #07111b;
  line-height: 24px;
  margin-bottom: 4px
}

.cart-body .item-2 .img-box {
  display: block;
}
.cart-body .item-2 .img-box img{
  height: 94px;
  width: 166px;
}
.cart-body .item-2 dd {
  font-size: 12px;
  color: #93999f;
  line-height: 24px;
  font-weight: 200
}

.cart-body .item-2 dd a {
  display: inline-block;
  margin-left: 12px;
  color: rgba(240,20,20,.4)
}

.cart-body .item-2 dd a:hover {
  color: #f01414
}

.cart-body .item-3 {
  width: 280px;
  position: relative;
}

.cart-body .col{
  margin-left: 30px;
}

.cart-body .item-3>span {
  margin-left: 50px;
}

.cart-body .item-3 .price {
  display: inline-block;
  color: #1c1f21;
  height: 46px;
  width: 96px;
  padding-top: 24px;
  padding-bottom: 24px;
  font-size: 18px;
}
.cart-body .item-3 .price .original-price
{
  color: #aaa;
  text-decoration: line-through;
}
.cart-body .item-4 .close {
  font-size: 40px;
  height: 90px;
  color: #b7bbbf;
  line-height: 90px;
  cursor: pointer
}
.cart-body .item-4 .close:hover{
  color: #ff0000;
}
.cart-body .cart-body-bot.fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #fff;
  z-index: 300;
  box-shadow: 10px -2px 12px rgba(7,17,27,.2)
}

.cart-body .cart-body-bot.fixed .cart-body-bot-box {
  padding-bottom: 70px;
  width: 100%;
  height: 20px;
  padding-top: 40px;
}

.cart-body .cart-body-bot.fixed .cart-body-bot-box .li-3 {
  margin-right: 36px
}

.cart-body .cart-body-bot .cart-body-bot-box {
  margin-left: auto;
  margin-right: auto;
  display: block;
  padding-top: 24px
}

.cart-body .cart-body-bot .cart-body-bot-box .add-coupon-box {
  display: flex;
  flex-direction: row;
  align-items: center
}

.cart-body .cart-body-bot li {
  float: left
}

.cart-body .cart-body-bot .li-left {
  text-align: right
}

.cart-body .cart-body-bot .li-3 {
  font-size: 12px;
  color: #07111b;
  line-height: 24px
}

.cart-body .cart-body-bot .li-1 em,.cart-body .cart-body-bot .li-3 em {
  font-style: normal;
  color: red
}

.cart-body .cart-body-bot .li-2 {
  font-size: 0
}

.cart-body .cart-body-bot .li-2 .topdiv {
  font-size: 14px;
  color: #07111b;
  line-height: 28px
}

.cart-body .cart-body-bot .li-2 .price {
  font-size: 16px;
  color: #f01414;
  line-height: 24px;
  font-weight: 700
}

.cart-body .cart-body-bot .li-3 .btn {
  margin-left: 38px;
  float: right;
  padding: 13px 32px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  font-weight: 200;
  background: #f01414;
  border-radius: 4px
}

.cart-body .cart-body-bot .w70 {
  display: inline-block;
  width: 120px;
  text-align: right
}

.cart-body .cart-body-bot .w100 {
  display: inline-block;
  width: 100px;
  text-align: right
}
</style>