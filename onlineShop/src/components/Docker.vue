<template>
  <div class="docker">
    <div
      v-for="(item, index) in dockerlist"
      :class="{'docker__item': true, 'docker__item--active': index === currentIndex}"
      :key="item.icon"
    >
      <router-link :to="item.to">
        <div
          class="iconfont"
          v-html="item.icon"
        />
        <div class="docker__title">{{ item.text }}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Docker',
  props: ['currentIndex'],
  setup () {
    const dockerlist = [
      { icon: '&#xe61e;', text: '首页', to: { name: 'Home' } },
      { icon: '&#xe683;', text: '购物车', to: { name: 'CartList' } },
      { icon: '&#xe600;', text: '订单', to: { name: 'OrderList' } },
      { icon: '&#xe604;', text: '我的', to: { name: 'PersonalInfo' } }
    ]
    return { dockerlist }
  }
}
</script>

<style lang="scss" scoped>
.docker {
  display: flex;
  box-sizing: border-box;
  padding: 0 0.18rem;
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 0.49rem;
  border-top: 0.01rem solid;
  background: white;
  &__item {
    flex: 1;
    text-align: center;
    a {
      color: #333;
      text-decoration: none;
    }
    .iconfont {
      font-size: 0.18rem;
      margin: 0.07rem 0 0.02rem;
    }
    &--active {
      a {
        color: deepskyblue;
      }
    }
  }
  &__title {
    font-size: 0.2rem;
    transform: scale(0.5, 0.5);
    transform-origin: center top;
  }
}
</style>
