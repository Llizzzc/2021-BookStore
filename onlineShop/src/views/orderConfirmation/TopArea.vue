<template>
  <div class="top">
    <div class="top__header">
      <div
        class="iconfont top__header__back"
        @click="handleBackClick"
      >&#xe602;</div>
      确认订单
    </div>
    <div class="top__receiver">
      <div class="top__receiver__title">收货地址</div>
      <div v-if="address">
        <div class="top__receiver__address">
          {{ address.city }}{{ address.department }}{{ address.houseNumber }}
        </div>
        <div class="top__receiver__info">
          <span class="top__receiver__info__name">{{address.name}}</span>
          <span class="top__receiver__info__name">{{address.phone}}</span>
        </div>
        <div
          class="iconfont top__receiver__icon"
          @click="handleAddressClick"
        >&#xe602;</div>
      </div>
      <div v-else>
        <div class="top__receiver__address">
          暂无地址，请立即添加
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router'
import { get } from '../../utils/request'
import { reactive, toRefs } from 'vue'

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

// 选择地址逻辑
const useHandleAddress = () => {
  const router = useRouter()
  const route = useRoute()
  const shopId = route.params.id
  const handleAddressClick = () => { router.push(`/chooseAddressList/${shopId}`) }
  return handleAddressClick
}

// 获取一条地址信息
const useAddressEffect = () => {
  const userInfo = JSON.parse(localStorage.getItem('user'))
  const route = useRoute()
  const addressId = route.params.addressId || 0
  const data = reactive({ address: {} })
  const getaddressList = async () => {
    const result = await get('/oneAddress', {
      addressId,
      userId: userInfo.id
    })
    if (result === 'None') {
      data.address = NaN
      localStorage.setItem('orderAddressId', undefined)
    } else {
      data.address = result
      const orderAddressId = result.id
      localStorage.setItem('orderAddressId', orderAddressId)
    }
  }
  const { address } = toRefs(data)
  return { address, getaddressList }
}

export default {
  name: 'TopArea',
  setup () {
    const handleBackClick = useHandleBack()
    const handleAddressClick = useHandleAddress()
    const { address, getaddressList } = useAddressEffect()
    getaddressList()
    return { handleBackClick, handleAddressClick, address }
  }
}
</script>

<style lang="scss" scoped>
.top {
  position: relative;
  height: 1.96rem;
  background-size: 100% 1.59rem;
  background-image: linear-gradient(0deg, rgba(0, 145, 255, 0) 4%, #0091ff 50%);
  background-repeat: no-repeat;
  &__header {
    position: relative;
    padding-top: 0.2rem;
    line-height: 0.24rem;
    color: #fff;
    text-align: center;
    font-size: 0.16rem;
    &__back {
      position: absolute;
      left: 0.18rem;
      font-size: 0.22rem;
    }
  }
  &__receiver {
    position: absolute;
    left: 0.18rem;
    right: 0.18rem;
    bottom: 0;
    height: 1.11rem;
    background: #fff;
    border-radius: 0.04rem;
    &__title {
      line-height: 0.22rem;
      padding: 0.16rem 0 0.14rem 0.16rem;
      font-size: 0.16rem;
      color: #333;
    }
    &__address {
      line-height: 0.2rem;
      padding: 0 0.4rem 0 0.16rem;
      font-size: 0.14rem;
      color: #333;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    &__info {
      padding: 0.06rem 0 0 0.16rem;
      &__name {
        margin-right: 0.06rem;
        line-height: 0.18rem;
        font-size: 0.12rem;
        color: #666;
      }
    }
    &__icon {
      transform: rotate(180deg);
      position: absolute;
      right: 0.16rem;
      top: 0.5rem;
      color: #666;
      font-size: 0.2rem;
    }
  }
}
</style>
