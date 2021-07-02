<template>
  <div class="nearby">
    <h3 class="nearby__title">附近店铺</h3>
    <router-link
      v-for="item in nearbyList"
      :key="item.id"
      :to="`/shop/${item.id}`"
    >
      <ShopInfo :item="item" />
    </router-link>
  </div>
</template>

<script>
import ShopInfo from '../../components/ShopInfo'
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

export default {
  name: 'Nearby',
  components: { ShopInfo },
  setup () {
    const { nearbyList, getNearbyList } = useNearbyListEffect()
    getNearbyList()
    return { nearbyList }
  }
}

</script>

<style lang="scss" scoped>
.nearby {
  background: #fff;
  &__title {
    margin: 0.16rem 0 0.04rem 0;
    font-size: 0.18rem;
    font-weight: normal;
  }
}

a {
  text-decoration: none;
  color: #000;
}
</style>
