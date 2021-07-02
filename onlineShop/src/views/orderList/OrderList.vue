<template>
  <div class="wrapper">
    <div class="title">我的订单</div>
    <div class="orders">
      <div
        class="order"
        v-for="(item, index) in list"
        :key="index"
      >
        <div class="order__title">
          {{ item.shopName }}
          <span class="order__status">
            {{ +item.isCanceled ? '已取消' : '已下单' }}
          </span>
        </div>
        <div class="order__content">
          <template
            v-for="(innerItem, innerIndex) in item.books"
            :key="innerIndex"
          >
            <div
              class="order__content__info"
              v-if="innerIndex <= 5"
            >
              <img
                class="order__content__info__img"
                :src="innerItem.bookInfo.imgUrl"
              />
              <div class="order__content__info__name">{{ innerItem.bookInfo.name }}</div>
              <div class="order__content__info__count">共{{ innerItem.book_sales }}件</div>
              <div class="order__content__info__price">￥{{ innerItem.book_sales * innerItem.bookInfo.price }}</div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
  <Docker :currentIndex="2" />
</template>

<script>
import { reactive, toRefs } from 'vue'
import { get } from '../../utils/request'
import Docker from '../../components/Docker'

// 处理订单列表逻辑
const useOrderListEffect = () => {
  const userInfo = JSON.parse(localStorage.getItem('user'))
  const data = reactive({ list: [] })
  const getOrderList = async () => {
    const result = await get('/order', { id: userInfo.id })
    if (result) {
      data.list = result.orders
    }
  }
  const { list } = toRefs(data)
  return { list, getOrderList }
}

export default {
  name: 'OrderList',
  components: { Docker },
  setup () {
    const { list, getOrderList } = useOrderListEffect()
    getOrderList()
    return { list }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  overflow-y: auto;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0.5rem;
  right: 0;
  background: #f8f8f8;
}
.title {
  line-height: 0.44rem;
  background: #fff;
  font-size: 0.16rem;
  color: #333;
  text-align: center;
}
.order {
  margin: 0.16rem 0.18rem;
  padding: 0.16rem;
  background: #fff;
  &__title {
    margin-bottom: 0.16rem;
    line-height: 0.22rem;
    font-size: 0.16rem;
    color: #333;
  }
  &__status {
    float: right;
    font-size: 0.14rem;
    color: #999;
  }
  &__content {
    display: flex;
    flex-flow: row wrap;
    align-content: flex-start;
    &__info {
      flex: 0 0 25%;
      margin: 0.05rem;
      height: 0.95rem;
      width: 0.6rem;
      &__img {
        width: 0.4rem;
        height: 0.4rem;
      }
      &__name {
        margin-bottom: 0.04rem;
        line-height: 0.2rem;
        font-size: 0.1rem;
        color: #e93b3b;
        text-align: left;
      }
      &__count,
      &__price {
        line-height: 0.14rem;
        font-size: 0.12rem;
        color: #333;
        text-align: left;
      }
    }
  }
}
</style>
