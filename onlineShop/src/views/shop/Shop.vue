<template>
  <div class="warpper">
    <div class="search">
      <div
        class="search__back iconfont"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="search__content">
        <span class="search__content__icon iconfont">&#xe6a0;</span>
        <div class="search__content__input">
          欢迎新老顾客光临
        </div>
        <span class="search__content__icon iconfont">&#xe6a0;</span>
      </div>
    </div>
    <ShopInfo
      :item="item"
      :hideBorder="true"
    />
    <Content :shopName="item.title" />
    <Cart :expressLimit="item.expressLimit" />
  </div>
</template>

<script>
import { get } from '../../utils/request'
import { useRouter, useRoute } from 'vue-router'
import { reactive, toRefs } from 'vue'
import ShopInfo from '../../components/ShopInfo'
import Content from '../shop/Content'
import Cart from '../shop/Cart'

// 获取当前商铺信息
const useShopInfoEffect = () => {
  const route = useRoute()
  const data = reactive({ item: {} })
  const getItemData = async () => {
    const result = await get('/showShop', { id: route.params.id })
    data.item = result
  }
  const { item } = toRefs(data)
  return { item, getItemData }
}

// 点击回退
const useBackRouterEffect = () => {
  const router = useRouter()
  const handleBackClick = () => {
    router.back()
  }
  return { handleBackClick }
}

export default {
  name: 'Shop',
  components: { ShopInfo, Content, Cart },
  setup () {
    const { handleBackClick } = useBackRouterEffect()
    const { item, getItemData } = useShopInfoEffect()
    getItemData()
    return { item, handleBackClick }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  padding: 0 0.18rem;
}

.search {
  display: flex;
  margin: 0.2rem 0 0.16rem 0;
  &__back {
    width: 0.3rem;
    font-size: 0.3rem;
    color: #b6b6b6;
  }
  &__content {
    display: flex;
    flex: 1;
    background: #f5f5f5;
    border-radius: 0.16rem;
    &__icon {
      width: 0.44rem;
      font-size: 0.2rem;
      text-align: center;
      color: red;
      padding-top: 0.06rem;
    }
    &__input {
      display: block;
      width: 100%;
      padding-right: 0.2rem;
      border: none;
      outline: none;
      background: none;
      height: 0.32rem;
      font-size: 0.24rem;
      text-align: center;
      color: red;
    }
  }
}
</style>
