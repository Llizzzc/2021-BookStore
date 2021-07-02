<template>
  <div class="wrapper">
    <img
      class="wrapper__img"
      src="../../img/others/5.jpg"
    />
    <div class="wrapper__input">
      <div class="wrapper__input__content">admin</div>
    </div>
    <div class="wrapper__input">
      <input
        type="password"
        class="wrapper__input__content"
        placeholder="请输入密码"
        v-model="password"
        autocomplete="new-password"
      />
    </div>
    <div
      class="wrapper__login-button"
      @click="handleLogin"
    >登录</div>
    <div
      class="wrapper__login-link"
      @click="handleLoginClick"
    >用户登录</div>
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
    password: ''
  })
  const handleLogin = async () => {
    if (data.password === '') {
      showToast('密码不能为空!')
    } else {
      try {
        const result = await post('/admin', {
          name: 'admin',
          password: data.password
        })
        if (typeof result !== 'string') {
          localStorage.isLogin = true
          const adminInfo = {
            id: result.id,
            name: result.name
          }
          localStorage.setItem('admin', JSON.stringify(adminInfo))
          showToast('登录成功!')
          setTimeout(() => {
            router.push({ name: 'AdminHome' })
          }, 2000)
        } else if (result === 'error') {
          showToast('密码错误!')
          data.password = ''
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { password } = toRefs(data)
  return { password, handleLogin }
}

// 登录跳转
const useGoLoginEffect = () => {
  const router = useRouter()
  const handleLoginClick = () => {
    router.push({ name: 'Login' })
  }
  return { handleLoginClick }
}

export default {
  name: 'Admin',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const { password, handleLogin } = useLoginEffect(showToast)
    const { handleLoginClick } = useGoLoginEffect()
    return { password, handleLogin, show, toastMessage, handleLoginClick }
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
}
</style>
