<template>
  <div class="shop">
    <img
      class="shop__img"
      :src="item.imgUrl"
    >
    <div :class="{'shop__content':true, 'shop__content--bordered': hideBorder ? false: true}">
      <div class="shop__content__title">{{ item.title }}</div>
      <div class="shop__content__tags">
        <span class="shop__content__tag">月售{{ item.sales }}件</span>
        <span class="shop__content__tag">起送{{ item.expressLimit }}元</span>
        <span class="shop__content__tag">配送费{{ item.expressPrice }}元</span>
      </div>
      <p class="shop__content__highlight">{{ item.slogan }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ShopInfo',
  props: ['item', 'hideBorder']
}
</script>

<style lang="scss" scoped>
.shop {
  display: flex;
  padding-top: 0.12rem;
  &__img {
    margin-right: 0.16rem;
    width: 0.7rem;
    height: 0.7rem;
  }
  &__content {
    flex: 1;
    padding-bottom: 0.12rem;
    &--bordered {
      border-bottom: .01rem solid #b7b7b7;
    }
    &__title {
      line-height: 0.22rem;
      font-size: 0.16rem;
    }
    &__tags {
      margin-top: 0.08rem;
      line-height: 0.18rem;
      font-size: 0.13rem;
    }
    &__tag {
      margin-right: 0.16rem;
    }
    &__highlight {
      margin: 0.08rem 0 0 0;
      line-height: 0.18rem;
      font-size: 0.13rem;
      color: #e93b3b;
    }
  }
}
</style>
