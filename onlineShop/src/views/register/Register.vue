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
    <div class="wrapper__input">
      <input
        type="password"
        class="wrapper__input__content"
        placeholder="确认密码"
        v-model="ensurement"
      />
    </div>
    <div
      class="wrapper__register-button"
      @click="handleRegister"
    >注册</div>
    <div
      class="wrapper__register-link"
      @click="handleLoginClick"
    >已有账号去登录</div>
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

// 注册逻辑
const useRegisterEffect = (showToast) => {
  const router = useRouter()
  const data = reactive({
    username: '',
    password: '',
    ensurement: ''
  })
  const handleRegister = async () => {
    if (data.username === '' || data.password === '' || data.ensurement === '') {
      showToast('用户名或密码不能为空!')
    } else if (data.password !== data.ensurement) {
      showToast('两次密码不一致，请重新输入!')
      data.password = ''
      data.ensurement = ''
    } else {
      try {
        const result = await post('/register', {
          username: data.username,
          password: data.password,
          ensurement: data.ensurement
        })
        if (result === 'ok') {
          showToast('注册成功!')
          setTimeout(() => {
            router.push({ name: 'Login' })
          }, 2000)
        } else if (result === 'exist') {
          data.username = ''
          data.password = ''
          data.ensurement = ''
          showToast('用户存在，请前往登录!')
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { username, password, ensurement } = toRefs(data)
  return { username, password, ensurement, handleRegister }
}

// 登录跳转
const useLoginEffect = () => {
  const router = useRouter()
  const handleLoginClick = () => {
    router.push({ name: 'Login' })
  }
  return { handleLoginClick }
}

export default {
  name: 'Register',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const { username, password, ensurement, handleRegister } = useRegisterEffect(showToast)
    const { handleLoginClick } = useLoginEffect()
    return { username, password, ensurement, handleRegister, handleLoginClick, show, toastMessage }
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
      line-height: 0.48rem;
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
  &__register-button {
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
  &__register-link {
    margin-top: 0.2rem;
    text-align: center;
    font-size: 0.14rem;
    color: #777;
  }
}
</style>
