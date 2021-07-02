<template>
  <div class="address">
    <div class="address__info">
      <div class="address__info__user">
        姓名:{{ address.name }}
      </div>
      <div class="address__info__phone">
        电话:{{ address.phone }}
      </div>
    </div>
    <div class="address__detail">
      住址:{{ address.city }}{{ address.department }}{{ address.houseNumber }}
    </div>
    <div class="iconfont address__icon">&#xe602;</div>
  </div>
</template>

<script>
export default {
  name: 'Address',
  props: ['address']
}
</script>

<style lang="scss" scoped>
.address {
  position: relative;
  margin: 0.16rem 0.18rem 0 0.18rem;
  padding: 0.18rem 0.64rem 0.18rem 0.16rem;
  background: #fff;
  border-radius: 0.04rem;
  &__info {
    display: flex;
    line-height: 0.2rem;
    font-size: 0.14rem;
    color: #333;
    &__user {
      width: 0.94rem;
    }
    &__phone {
      flex: 1;
    }
  }
  &__detail {
    margin-top: 0.08rem;
    line-height: 0.2rem;
    font-size: 0.14rem;
  }
  &__icon {
    position: absolute;
    right: 0.2rem;
    top: 0.4rem;
    transform: rotate(180deg);
    font-size: 0.2rem;
    color: #999;
  }
}
</style>
