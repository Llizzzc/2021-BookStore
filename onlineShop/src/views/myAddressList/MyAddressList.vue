<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">管理收货地址</div>
      <div
        class="title__add"
        @click="handleAddClick"
      >新建</div>
    </div>
    <Address
      v-for="address in addressList"
      :key="address.id"
      :address="address"
      @click="() => handleUpdateClick(address.id)"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { get } from '../../utils/request'
import Address from '../../components/Address'
import { useRouter } from 'vue-router'

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

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

// 新增地址
const useAddressAdd = () => {
  const router = useRouter()
  const handleAddClick = () => { router.push({ name: 'AddAddress' }) }
  return handleAddClick
}

// 更新地址
const useAddressUpdate = (addressId) => {
  const router = useRouter()
  const handleUpdateClick = (addressId) => {
    router.push(`/UpdateAddress/${addressId}`)
  }
  return handleUpdateClick
}

export default {
  name: 'MyAddressList',
  components: { Address },
  setup () {
    const { addressList, getaddressList } = useAddressEffect()
    const handleBackClick = useHandleBack()
    const handleAddClick = useAddressAdd()
    const handleUpdateClick = useAddressUpdate()
    getaddressList()
    return { handleBackClick, handleAddClick, handleUpdateClick, addressList }
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
  display: flex;
  line-height: 0.44rem;
  background: #fff;
  font-size: 0.16rem;
  color: #333;
  text-align: center;
  &__back {
    width: 0.2rem;
    margin-left: 0.18rem;
    font-size: 0.2rem;
    color: #b6b6b6;
  }
  &__text {
    flex: 1;
    text-align: center;
  }
  &__add {
    margin-right: 0.2rem;
    font-size: 0.14rem;
  }
}
</style>
