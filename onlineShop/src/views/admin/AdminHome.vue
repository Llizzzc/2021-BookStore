<template>
  <div class="wrapper">
    <div class="header">
      <div class="header__info">
        <div class="header__info__user">{{ adminInfo.name }}</div>
        <div class="header__info__id">ID: {{ adminInfo.id }}</div>
      </div>
      <img
        class="header__avatar"
        src="../../img/others/6.jpg"
      />
    </div>
    <div
      class="wrapper__button"
      @click="handleBookInfo"
    >图书信息</div>
    <div
      class="wrapper__button"
      @click="handleNearbyInfo"
    >店铺信息</div>
    <div
      class="logout"
      @click="handleLogout"
    >退出</div>
  </div>
  <Toast
    v-if="show"
    :message="toastMessage"
  />
</template>

<script>
import { useRouter } from 'vue-router'
import Toast, { useToastEffect } from '../../components/Toast'

// 退出
const useLogOutEffect = (showToast) => {
  const router = useRouter()
  const handleLogout = () => {
    localStorage.removeItem('isLogin')
    localStorage.removeItem('admin')
    showToast('退出成功!')
    setTimeout(() => {
      router.replace({ name: 'Admin' })
    }, 2000)
  }
  return { handleLogout }
}

// 获取信息
const useUserEffect = () => {
  const adminInfo = JSON.parse(localStorage.getItem('admin'))
  return adminInfo
}

// 店铺信息
const useNearbyEffect = () => {
  const router = useRouter()
  const handleNearbyInfo = () => {
    router.push({ name: 'AllShop' })
  }
  return handleNearbyInfo
}

// 图书信息
const useBookInfoEffect = () => {
  const router = useRouter()
  const handleBookInfo = () => {
    router.push({ name: 'AllBook' })
  }
  return handleBookInfo
}

export default {
  name: 'AdminHome',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const { handleLogout } = useLogOutEffect(showToast)
    const adminInfo = useUserEffect()
    const handleNearbyInfo = useNearbyEffect()
    const handleBookInfo = useBookInfoEffect()
    return { handleLogout, show, toastMessage, adminInfo, handleNearbyInfo, handleBookInfo }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  overflow-y: auto;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0.5rem;
  right: 0;
  background: #f8f8f8;
  &__button {
    margin: 0.32rem 0.4rem 0 0.4rem;
    line-height: 0.48rem;
    background: #0091ff;
    box-shadow: 0 0.04rem 0.08rem 0 rgba(0, 145, 255, 0.32);
    border-radius: 0.04rem;
    border-radius: 0.04rem;
    color: #fff;
    font-size: 0.16rem;
    text-align: center;
  }
}

.header {
  position: relative;
  height: 1.5rem;
  background-image: linear-gradient(239deg, #3a6ff3 0%, #50c7fb 100%);
  padding-top: 0.4rem;
  &__info {
    margin: 0.3rem 0.18rem 0 0.18rem;
    padding-top: 0.46rem;
    height: 0.66rem;
    background: #fff;
    border-radius: 0.08rem;
    &__user {
      font-size: 0.24rem;
      color: #262628;
      text-align: center;
      line-height: 0.36rem;
    }
    &__id {
      margin-top: 0.04rem;
      font-size: 0.14rem;
      color: #c1c0c9;
      text-align: center;
    }
  }
  &__avatar {
    position: absolute;
    left: 50%;
    top: 0.2rem;
    transform: translateX(-50%);
    width: 0.94rem;
    height: 0.94rem;
    border-radius: 50%;
  }
}

.logout {
  margin: 0.18rem;
  margin-top: 0.3rem;
  line-height: 0.32rem;
  background: red;
  color: #f8f8f8;
  text-align: center;
  border-radius: 0.04rem;
}
</style>
