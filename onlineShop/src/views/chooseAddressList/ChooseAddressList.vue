<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__icon"
        @click="handleBackClick"
      >&#xe602;</div>
      收货地址
    </div>
    <Address
      v-for="address in addressList"
      :key="address.id"
      :address="address"
      @click="() => handleAddressClick(address.id)"
    />
  </div>
</template>

<script>
import Address from '../../components/Address'
import { useRouter, useRoute } from 'vue-router'
import { ref } from 'vue'
import { get } from '../../utils/request'

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

// 选择地址逻辑
const usePickAddressEffect = () => {
  const router = useRouter()
  const route = useRoute()
  const shopId = route.params.id
  const handleAddressClick = (addressId) => {
    router.push(`/orderConfirmation/${shopId}/${addressId}`)
  }
  return handleAddressClick
}

// 获取地址信息
const useAddressEffect = () => {
  const userInfo = JSON.parse(localStorage.getItem('user'))
  const addressList = ref([])
  const getaddressList = async () => {
    const result = await get('/showAddress', { id: userInfo.id })
    addressList.value = result.key
  }
  return { addressList, getaddressList }
}

export default {
  name: 'ChooseAddressList',
  components: { Address },
  setup () {
    const handleBackClick = useHandleBack()
    const handleAddressClick = usePickAddressEffect()
    const { addressList, getaddressList } = useAddressEffect()
    getaddressList()
    return { handleBackClick, handleAddressClick, addressList }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  overflow-y: auto;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  background: #f8f8f8;
}
.title {
  position: relative;
  line-height: 0.44rem;
  background: #fff;
  font-size: 0.16rem;
  color: #333;
  text-align: center;
  &__icon {
    position: absolute;
    left: 0.18rem;
    top: 0;
    font-size: 0.2rem;
  }
}
</style>
