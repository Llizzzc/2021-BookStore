<template>
  <div class="title">
    <div
      class="iconfont title__back"
      @click="handleBackClick"
    >&#xe602;</div>
    <div class="title__text">
    </div>
    <div
      class="title__add"
      @click="handleAddNearby"
    >新开店铺</div>
  </div>
  <div class="nearby">
    <h3 class="nearby__title">所有店铺</h3>
    <template
      v-for="item in nearbyList"
      :key="item.id"
    >
      <router-link :to="`/TheShop/${item.id}`">
        <ShopInfo :item="item" />
      </router-link>
      <div
        class="nearby__edit"
        @click="() => handleEditNearby(item.id)"
      >编辑店铺</div>
      <div
        class="nearby__delete"
        @click="() => handleDeleteNearby(item.id)"
      >关闭店铺</div>
    </template>
  </div>
</template>

<script>
import ShopInfo from '../../components/ShopInfo'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { get } from '../../utils/request'

// 附近店铺展示
const useNearbyListEffect = () => {
  const nearbyList = ref([])
  const getNearbyList = async () => {
    const result = await get('/showNearby')
    nearbyList.value = result.key
  }
  return { nearbyList, getNearbyList }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

// 编辑店铺
const useEditNearby = (shopId) => {
  const router = useRouter()
  const handleEditNearby = (shopId) => {
    router.push(`/EditShop/${shopId}`)
  }
  return handleEditNearby
}

// 关闭店铺
const useDeleteNearby = (shopId) => {
  const router = useRouter()
  const handleDeleteNearby = (shopId) => {
    router.push(`/DeleteShop/${shopId}`)
  }
  return handleDeleteNearby
}

// 新开店铺
const useAddNearby = () => {
  const router = useRouter()
  const handleAddNearby = () => {
    router.push({ name: 'AddShop' })
  }
  return handleAddNearby
}

export default {
  name: 'AllShop',
  components: { ShopInfo },
  setup () {
    const { nearbyList, getNearbyList } = useNearbyListEffect()
    const handleBackClick = useHandleBack()
    const handleEditNearby = useEditNearby()
    const handleDeleteNearby = useDeleteNearby()
    const handleAddNearby = useAddNearby()
    getNearbyList()
    return { nearbyList, handleBackClick, handleEditNearby, handleAddNearby, handleDeleteNearby }
  }
}

</script>

<style lang="scss" scoped>
.nearby {
  overflow-y: auto;
  background: #fff;
  &__title {
    margin: 0.16rem 0 0.2rem 0;
    font-size: 0.28rem;
    font-weight: normal;
  }
  &__edit {
    line-height: 0.28rem;
    background: #0091ff;
    box-shadow: 0 0.04rem 0.08rem 0 rgba(0, 145, 255, 0.32);
    border-radius: 0.04rem;
    border-radius: 0.04rem;
    color: #fff;
    font-size: 0.16rem;
    text-align: center;
  }
  &__delete {
    line-height: 0.28rem;
    margin-bottom: 0.2rem;
    background: red;
    box-shadow: 0 0.04rem 0.08rem 0 rgba(0, 145, 255, 0.32);
    border-radius: 0.04rem;
    border-radius: 0.04rem;
    color: #fff;
    font-size: 0.16rem;
    text-align: center;
  }
}

a {
  text-decoration: none;
  color: #000;
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
    color: #b7b7b7;
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
