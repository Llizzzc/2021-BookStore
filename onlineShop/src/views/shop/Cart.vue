<template>
  <div
    class="mask"
    v-if="showCart && calculations.total > 0"
    @click="handleCartShowChange"
  >
  </div>
  <div class="cart">
    <div
      class="product"
      v-if="showCart && calculations.total > 0"
    >
      <div class="product__header">
        <div
          class="product__header__all"
          @click="() => setCartItemsCheck(shopId)"
        >
          <span
            class="product__header__icon iconfont"
            v-html="calculations.allChecked ? '&#xe612;' : '&#xe63f;'"
          ></span>
          全选
        </div>
        <div class="product__header__clear">
          <span
            class="product__header__clear__btn"
            @click="() => cleanCartProducts(shopId)"
          >清空购物车</span>
        </div>
      </div>
      <div
        v-for="item in productList"
        :key="item.id"
        class="product__item"
      >
        <div
          class="product__item__checked iconfont"
          v-html="item.check ? '&#xe612;' : '&#xe63f;'"
          @click="() => changeCartItemChecked(shopId, item.id)"
        >
        </div>
        <img
          class="product__item__img"
          :src="item.imgUrl"
        >
        <div class="product__item__detail">
          <h4 class="product__item__title">{{ item.name }}</h4>
          <p class="product__item__price">
            <span class="product__item__yen">&yen;</span>{{ item.price }}
            <span class="product__item__origin">&yen;{{ item.oldPrice }}</span>
          </p>
        </div>
        <div class="product__number">
          <span
            class="product__number__minus iconfont"
            @click="() => { changeCartItemInfo(shopId, item.id, item, -1) }"
          >&#xe687;</span>
          {{ item.count || 0 }}
          <span
            class="product__number__plus iconfont"
            @click="() => { changeCartItemInfo(shopId, item.id, item, 1) }"
          >&#xe619;</span>
        </div>
      </div>
    </div>
    <div class="check">
      <div class="check__icon">
        <img
          src="../../img/others/3.png"
          class="check__icon__img"
          @click="handleCartShowChange"
        >
        <div class="check__icon__tag">{{ calculations.total }}</div>
      </div>
      <div class="check__info">
        总计(起送{{ expressLimit }}元): <span class="check__info__price">&yen; {{ calculations.price }}</span>
      </div>
      <div
        class="check__btn"
        v-show="calculations.total > 0"
      >
        <div v-if="calculations.price >= expressLimit">
          <router-link :to="{path: `/OrderConfirmation/${shopId}`}">
            去结算
          </router-link>
        </div>
        <div v-else>还差{{ expressLimit - calculations.price }}元起送</div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useCommonCartEffect } from '../../effects/cartEffects'

// 获取购物车信息逻辑
const useCartEffect = (shopId) => {
  const store = useStore()
  const { calculations, changeCartItemInfo, productList } = useCommonCartEffect(shopId)

  const changeCartItemChecked = (shopId, productId) => {
    store.commit('changeCartItemChecked', {
      shopId,
      productId
    })
  }

  const cleanCartProducts = (shopId) => {
    store.commit('cleanCartProducts', { shopId })
  }

  const setCartItemsCheck = (shopId) => {
    store.commit('setCartItemsCheck', { shopId })
  }

  return {
    productList, changeCartItemInfo, changeCartItemChecked, cleanCartProducts, calculations, setCartItemsCheck
  }
}

// 展示隐藏购物车逻辑
const toggleCartEffect = () => {
  const showCart = ref(false)
  const handleCartShowChange = () => {
    showCart.value = !showCart.value
  }
  return { showCart, handleCartShowChange }
}

export default {
  name: 'Cart',
  props: ['expressLimit'],
  setup () {
    const route = useRoute()
    const shopId = route.params.id
    const { showCart, handleCartShowChange } = toggleCartEffect()
    const { calculations, productList, changeCartItemInfo, changeCartItemChecked, cleanCartProducts, setCartItemsCheck } = useCartEffect(shopId)
    return { calculations, shopId, productList, changeCartItemInfo, changeCartItemChecked, cleanCartProducts, setCartItemsCheck, showCart, handleCartShowChange }
  }
}
</script>

<style lang="scss" scoped>
.mask {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.cart {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  background: #fff;
}

.product {
  overflow-y: scroll;
  flex: 1;
  background: #fff;
  &__header {
    display: flex;
    height: 0.52rem;
    border-bottom: .01rem solid #f1f1f1;
    font-size: 0.145rem;
    color: #333;
    &__all {
      width: 0.64rem;
      margin-top: 0.15rem;
      margin-left: 0.18rem;
    }
    &__icon {
      display: inline-block;
      vertical-align: top;
      color: #0091ff;
      font-size: 0.15rem;
    }
    &__clear {
      flex: 1;
      margin-top: 0.15rem;
      margin-right: 0.16rem;
      text-align: right;
      &__btn {
        display: inline-block;
      }
    }
  }
  &__item {
    display: flex;
    position: relative;
    padding: 0.012rem;
    margin: 0 0.16rem;
    border-bottom: 0.01rem solid #f1f1f1;
    &__checked {
      line-height: 0.5rem;
      margin-right: 0.2rem;
      color: #0091ff;
      font-size: 0.2rem;
    }
    &__detail {
      overflow: hidden;
    }
    &__img {
      width: 0.46rem;
      height: 0.46rem;
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
    &__price {
      margin: 0.06rem 0 0 0;
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

.check {
  display: flex;
  height: 0.51rem;
  border-top: 0.01rem solid #f1f1f1;
  line-height: 0.49rem;
  &__icon {
    position: relative;
    width: 0.84rem;
    &__img {
      display: block;
      margin: 0.12rem auto;
      width: 0.28rem;
      height: 0.26rem;
    }
    &__tag {
      position: absolute;
      left: 0.46rem;
      top: 0.04rem;
      padding: 0 0.04rem;
      min-width: 0.2rem;
      height: 0.2rem;
      line-height: 0.2rem;
      background-color: #e93b3b;
      border-radius: 0.1rem;
      font-size: 0.12rem;
      text-align: center;
      color: #fff;
      transform: scale(0.5);
      transform-origin: left center;
    }
  }
  &__info {
    flex: 1;
    color: #333;
    font-size: 0.12rem;
    &__price {
      color: #e93b3b;
      font-size: 0.18rem;
    }
  }
  &__btn {
    width: 0.98rem;
    line-height: 0.49rem;
    background-color: #4fb0f9;
    color: #fff;
    font-size: 0.14rem;
    text-align: center;
    a {
      color: #fff;
      text-decoration: none;
    }
  }
}
</style>
