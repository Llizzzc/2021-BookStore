<template>
  <div class="wrapper">
    <img
      class="wrapper__img"
      src="../../img/others/2.jpg"
    />
    <div class="wrapper__input">
      <input
        class="wrapper__input__content"
        placeholder="请输入用户名"
        v-model="username"
      />
    </div>
    <div class="wrapper__input">
      <input
        type="password"
        class="wrapper__input__content"
        placeholder="请输入密码"
        v-model="password"
      />
    </div>
    <div
      class="wrapper__login-button"
      @click="handleLogin"
    >登录</div>
    <div
      class="wrapper__login-link"
      @click="handleRegisterClick"
    >立即注册</div>
    <div
      class="wrapper__admin-link"
      @click="handleAdminClick"
    >管理员登录</div>
    <Toast
      v-if="show"
      :message="toastMessage"
    />
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { reactive, toRefs } from 'vue'
import { post } from '../../utils/request'
import Toast, { useToastEffect } from '../../components/Toast'

// 登录逻辑
const useLoginEffect = (showToast) => {
  const router = useRouter()
  const data = reactive({
    username: '',
    password: ''
  })
  const handleLogin = async () => {
    if (data.username === '' || data.password === '') {
      showToast('用户名或密码不能为空!')
    } else {
      try {
        const result = await post('/login', {
          username: data.username,
          password: data.password
        })
        if (typeof result !== 'string') {
          localStorage.isLogin = true
          const userInfo = {
            id: result.id,
            name: result.username
          }
          localStorage.setItem('user', JSON.stringify(userInfo))
          showToast('登录成功!')
          setTimeout(() => {
            router.push({ name: 'Home' })
          }, 2000)
        } else if (result === 'error') {
          showToast('用户名或密码错误!')
          data.password = ''
          data.username = ''
        } else if (result === 'none') {
          showToast('无此用户，请立即注册!')
          data.username = ''
          data.password = ''
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { username, password } = toRefs(data)
  return { username, password, handleLogin }
}

// 注册跳转
const useRegisterEffect = () => {
  const router = useRouter()
  const handleRegisterClick = () => {
    router.push({ name: 'Register' })
  }
  return { handleRegisterClick }
}

// 管理员跳转
const useAdminEffect = () => {
  const router = useRouter()
  const handleAdminClick = () => {
    router.push({ name: 'Admin' })
  }
  return { handleAdminClick }
}

export default {
  name: 'Login',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const { username, password, handleLogin } = useLoginEffect(showToast)
    const { handleRegisterClick } = useRegisterEffect()
    const { handleAdminClick } = useAdminEffect()
    return { username, password, handleLogin, handleRegisterClick, show, toastMessage, handleAdminClick }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  &__img {
    display: block;
    margin: 0 auto 0.4rem auto;
    width: 0.68rem;
    height: 0.68rem;
  }
  &__input {
    height: 0.48rem;
    margin: 0 0.4rem 0.16rem 0.4rem;
    padding: 0 0.16rem;
    background: #f9f9f9;
    border: 0.01rem solid rgba(0, 0, 0, 0.1);
    border-radius: 0.06rem;
    &__content {
      margin-top: 0.12rem;
      line-height: 0.22rem;
      border: none;
      outline: none;
      width: 100%;
      background: none;
      font-size: 0.16rem;
      color: rgba(0, 0, 0, 0.5);
      &::placeholder {
        color: rgba(0, 0, 0, 0.5);
      }
    }
  }
  &__login-button {
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
  &__login-link {
    margin-top: 0.2rem;
    text-align: center;
    font-size: 0.14rem;
    color: #777;
  }
  &__admin-link {
    margin-top: 0.2rem;
    text-align: center;
    font-size: 0.14rem;
    font-weight: bold;
    color: rebeccapurple;
  }
}
</style>
