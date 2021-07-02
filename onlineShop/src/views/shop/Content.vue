<template>
  <div class="content">
    <div class="category">
      <div
        :class="{category__item: true ,'category__item--active': currentTab === item.tab}"
        v-for="item in categories"
        :key="item.name"
        @click="() => handleTabClick(item.tab)"
      >{{ item.name }}</div>
    </div>
    <div class="product">
      <div
        class="product__item"
        v-for="item in list"
        :key="item.id"
      >
        <img
          class="product__item__img"
          :src="item.imgUrl"
        >
        <div class="product__item__detail">
          <h4 class="product__item__title">{{ item.name }}</h4>
          <p class="product__item__sales">月售{{ item.sales }}件 </p>
          <p class="product__item__stocks">现有{{ item.stock }}件</p>
          <p class="product__item__price">
            <span class="product__item__yen">&yen;</span>{{ item.price }}
            <span class="product__item__origin">&yen;{{ item.oldPrice }}</span>
          </p>
        </div>
        <div class="product__number">
          <span
            class="product__number__minus iconfont"
            @click="() => { changeCartItem(shopId, item.id, item, -1, shopName) }"
          >&#xe687;</span>
          {{ getProductCartCount(shopId, item.id) }}
          <span
            class="product__number__plus iconfont"
            @click="() => { changeCartItem(shopId, item.id, item, 1, shopName) }"
          >&#xe619;</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { get } from '../../utils/request'
import { reactive, toRefs, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useCommonCartEffect } from '../../effects/cartEffects'

// tab类
const categories = [{
  name: '漫画',
  tab: 'cartoon'
}, {
  name: '科幻',
  tab: 'sci-fi'
}, {
  name: '美食',
  tab: 'food'
}, {
  name: '教育',
  tab: 'education'
}, {
  name: '儿童',
  tab: 'children'
}, {
  name: '法律',
  tab: 'law'
}, {
  name: '历史',
  tab: 'history'
}, {
  name: '经济',
  tab: 'financial'
}, {
  name: '娱乐',
  tab: 'amusing'
}, {
  name: '旅游',
  tab: 'travel'
}]

// tab切换逻辑
const useTabEffect = () => {
  const currentTab = ref(categories[0].tab)
  const handleTabClick = (tab) => {
    currentTab.value = tab
  }
  return { currentTab, handleTabClick }
}

// 列表相关逻辑
const useCurrentListEffect = (currentTab, shopId) => {
  const content = reactive({ list: [] })
  const getContentData = async (tab) => {
    const result = await get('/showBook', { tab: currentTab.value, id: shopId })
    content.list = result.key
  }
  watchEffect(() => { getContentData() })
  const { list } = toRefs(content)
  return { list }
}

// 购物车相关逻辑
const useCartEffect = () => {
  const store = useStore()
  const { changeCartItemInfo, cartList } = useCommonCartEffect()
  const changeShopName = (shopId, shopName) => {
    store.commit('changeShopName', {
      shopId,
      shopName
    })
  }
  const changeCartItem = (shopId, productId, item, num, shopName) => {
    changeCartItemInfo(shopId, productId, item, num)
    changeShopName(shopId, shopName)
  }
  const getProductCartCount = (shopId, productId) => {
    return cartList?.[shopId]?.productList?.[productId]?.count || 0
  }
  return { cartList, changeCartItem, getProductCartCount }
}

export default {
  name: 'Content',
  props: ['shopName'],
  setup () {
    const route = useRoute()
    const shopId = route.params.id
    const { currentTab, handleTabClick } = useTabEffect()
    const { list } = useCurrentListEffect(currentTab, shopId)
    const { cartList, changeCartItem, getProductCartCount } = useCartEffect()
    return { list, categories, currentTab, handleTabClick, shopId, cartList, changeCartItem, getProductCartCount }
  }
}
</script>

<style lang="scss" scoped>
.content {
  display: flex;
  position: absolute;
  left: 0;
  right: 0;
  top: 1.6rem;
  bottom: 0.5rem;
}

.category {
  overflow-y: scroll;
  width: 0.76rem;
  height: 100%;
  background: #f5f5f5;
  &__item {
    line-height: 0.4rem;
    text-align: center;
    font-size: .14rem;
    color: #333;
    &--active {
      background: #fff;
    }
  }
}

.product {
  overflow-y: scroll;
  flex: 1;
  &__item {
    display: flex;
    position: relative;
    padding: 0.012rem;
    margin: 0 0.16rem;
    border-bottom: 0.01rem solid #f1f1f1;
    &__detail {
      overflow: hidden;
    }
    &__img {
      width: 0.68rem;
      height: 0.68rem;
      margin-right: 0.16rem;
    }
    &__title {
      margin: 0;
      line-height: 0.2rem;
      font-size: 0.14rem;
      color: #333;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    &__sales {
      display: inline;
      margin: 0.06rem 0;
      font-size: 0.12rem;
      color: #333;
    }
    &__stocks {
      display: inline;
      margin: 0.06rem 0;
      font-size: 0.12rem;
      color: #333;
    }
    &__price {
      margin: 0;
      line-height: 0.2rem;
      font-size: 0.14rem;
      color: #e93b3b;
    }
    &__yen {
      font-size: 0.12rem;
    }
    &__origin {
      margin-left: 0.06rem;
      line-height: 0.2rem;
      font-size: 0.12rem;
      color: #999;
      text-decoration: line-through;
    }
    .product__number {
      position: absolute;
      right: 0;
      bottom: 0.12rem;
      line-height: 0.18rem;
      &__minus {
        color: #666;
        margin-right: 0.05rem;
      }
      &__plus {
        color: #0091ff;
        margin-left: 0.05rem;
      }
    }
  }
}
</style>
