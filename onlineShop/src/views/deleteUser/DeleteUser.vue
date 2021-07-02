<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        用户注销
      </div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">ID:</div>
        <div class="form__item__content">
          {{ userInfo.id }}
        </div>
      </div>
      <div class="form__item">
        <div class="form__item__label">姓名:</div>
        <div class="form__item__content">
          {{ userInfo.name }}
        </div>
      </div>
    </div>
    <div
      class="delate"
      @click="handleDelete"
    > 确认</div>
  </div>
  <Toast
    v-if="show"
    :message="toastMessage"
  />
</template>

<script>
import { useRouter } from 'vue-router'
import { post } from '../../utils/request'
import Toast, { useToastEffect } from '../../components/Toast'

// 获取用户信息
const useUserEffect = () => {
  const userInfo = JSON.parse(localStorage.getItem('user'))
  return userInfo
}

// 删除用户逻辑
const useDeletAddressEffect = (showToast) => {
  const router = useRouter()
  const userInfo = JSON.parse(localStorage.getItem('user'))
  const handleDelate = async () => {
    try {
      const result = await post('/deleteUser', {
        id: userInfo.id
      })
      if (result === 'ok') {
        localStorage.removeItem('isLogin')
        localStorage.removeItem('user')
        showToast('注销成功!')
        setTimeout(() => {
          router.push({ name: 'Login' })
        }, 2000)
      }
    } catch (e) {
      showToast('请求失败!')
    }
  }
  return handleDelate
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'DeleteUser',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const userInfo = useUserEffect()
    const handleDelete = useDeletAddressEffect(showToast)
    return { handleBackClick, show, toastMessage, handleDelete, userInfo }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  overflow-y: auto;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  background: #f8f8f8;
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
}
.form {
  padding: 0 0.2rem;
  margin-top: 0.12rem;
  background: #fff;
  border-top: 0.01rem solid #f1f1f1;
  border-bottom: 0.01rem solid #f1f1f1;
  &__item {
    display: flex;
    padding: 0.12rem 0;
    line-height: 0.2rem;
    font-size: 0.14rem;
    border-bottom: 0.01rem solid #f1f1f1;
    &:last-of-type {
      border-bottom: none;
    }
    &__label {
      margin-right: 0.05rem;
      color: #666;
    }
    &__content {
      flex: 1;
      border: none;
      outline: none;
      color: #3f3f3f;
      &::placeholder {
        color: #3f3f3f;
      }
    }
  }
}
.delate {
  margin: 0.18rem;
  line-height: 0.32rem;
  background: crimson;
  color: #f8f8f8;
  text-align: center;
  border-radius: 0.04rem;
}
</style>
