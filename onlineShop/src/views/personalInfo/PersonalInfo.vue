<template>
  <div class="wrapper">
    <div class="header">
      <div class="header__info">
        <div class="header__info__user">用户名: {{ userInfo.name }}</div>
        <div class="header__info__id">ID: {{ userInfo.id }}</div>
      </div>
      <img
        class="header__avatar"
        src="../../img/others/4.jpeg"
      />
    </div>
    <div class="list">
      <div class="list__item">
        <div class="list__item__icon iconfont">&#xf05a;</div>
        <div class="list__item__test">我的地址</div>
        <div
          class="list__item__arrow iconfont"
          @click="handleAddressClick"
        >&#xe602;</div>
      </div>
      <div class="list__item">
        <div class="list__item__icon iconfont">&#xe65a;</div>
        <div class="list__item__test">名字变更</div>
        <div
          class="list__item__arrow iconfont"
          @click="handleUsernameClick"
        >&#xe602;</div>
      </div>
      <div class="list__item">
        <div class="list__item__icon iconfont">&#xe654;</div>
        <div class="list__item__test">修改密码</div>
        <div
          class="list__item__arrow iconfont"
          @click="handlePswClick"
        >&#xe602;</div>
      </div>
      <div class="list__item">
        <div class="list__item__icon iconfont">&#xe660;</div>
        <div class="list__item__test">账号注销</div>
        <div
          class="list__item__arrow iconfont"
          @click="handleUserClick"
        >&#xe602;</div>
      </div>
    </div>
    <div
      class="logout"
      @click="handleLogout"
    >退出登陆</div>
  </div>
  <Toast
    v-if="show"
    :message="toastMessage"
  />
  <Docker :currentIndex="3" />
</template>

<script>
import { useRouter } from 'vue-router'
import Docker from '../../components/Docker'
import Toast, { useToastEffect } from '../../components/Toast'

// 获取用户信息
const useUserEffect = () => {
  const userInfo = JSON.parse(localStorage.getItem('user'))
  return userInfo
}

// 用户退出
const useLogOutEffect = (showToast) => {
  const router = useRouter()
  const handleLogout = () => {
    localStorage.removeItem('isLogin')
    localStorage.removeItem('cartList')
    localStorage.removeItem('user')
    showToast('退出成功!')
    setTimeout(() => {
      router.replace({ name: 'Login' })
    }, 2000)
  }
  return handleLogout
}

// 获取地址跳转
const useGetAddressEffect = () => {
  const router = useRouter()
  const handleAddressClick = () => {
    router.push({ name: 'MyAddressList' })
  }
  return handleAddressClick
}

// 改密跳转
const usePswEffect = () => {
  const router = useRouter()
  const handlePswClick = () => {
    router.push({ name: 'PswChange' })
  }
  return handlePswClick
}

// 改名跳转
const useUsernameEffect = () => {
  const router = useRouter()
  const handleUsernameClick = () => {
    router.push({ name: 'UsernameChange' })
  }
  return handleUsernameClick
}

// 账号注销
const useDeleteUserEffect = () => {
  const router = useRouter()
  const handleUserClick = () => {
    router.push({ name: 'DeleteUser' })
  }
  return handleUserClick
}

export default {
  name: 'PersonalInfo',
  components: { Docker, Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleLogout = useLogOutEffect(showToast)
    const handleAddressClick = useGetAddressEffect()
    const userInfo = useUserEffect()
    const handlePswClick = usePswEffect()
    const handleUsernameClick = useUsernameEffect()
    const handleUserClick = useDeleteUserEffect()
    return { handleUserClick, userInfo, handleLogout, handleAddressClick, show, toastMessage, handlePswClick, handleUsernameClick }
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
.list {
  margin: 0.16rem 0.18rem 0 0.18rem;
  background: #f8f8f8;
  box-shadow: 0 0.08rem 0.16rem 0 rgba(0, 0, 0, 0.08);
  border-radius: 0.08rem;
  &__item {
    display: flex;
    padding: 0.2rem;
    line-height: 0.22rem;
    font-size: 0.14rem;
    color: #262626;
    &__icon {
      margin-right: 0.12rem;
      width: 0.22rem;
      height: 0.22rem;
      background: #32c5ff;
      border-radius: 0.08rem;
      text-align: center;
      font-weight: bold;
      color: #f8f8f8;
    }
    &__test {
      flex: 1;
    }
    &__arrow {
      width: 0.2rem;
      transform: rotate(180deg);
      font-weight: bold;
      color: #c2c4ca;
    }
  }
}
.logout {
  margin: 0.18rem;
  line-height: 0.32rem;
  background: red;
  color: #f8f8f8;
  text-align: center;
  border-radius: 0.04rem;
}
</style>
