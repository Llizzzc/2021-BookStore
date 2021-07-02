<template>
  <div
    class="iconfont title__back"
    @click="handleBackClick"
  >&#xe602;</div>
  <div class="wrapper">
    <div class="wrapper__input">
      <input
        type="password"
        class="wrapper__input__content"
        placeholder="请输入原密码"
        v-model="password"
        autocomplete="new-password"
      />
    </div>
    <div class="wrapper__input">
      <input
        type="password"
        class="wrapper__input__content"
        placeholder="请输入新密码"
        v-model="newpswword"
        autocomplete="new-password"
      />
    </div>
    <div class="wrapper__input">
      <input
        type="password"
        class="wrapper__input__content"
        placeholder="请再次输入新密码"
        v-model="confirm"
        autocomplete="new-password"
      />
    </div>
    <div
      class="wrapper__change-button"
      @click="handleChange"
    >修改</div>
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

// 改密逻辑
const useChangeEffect = (showToast) => {
  const router = useRouter()
  const userInfo = JSON.parse(localStorage.getItem('user'))
  const data = reactive({
    password: '',
    newpswword: '',
    confirm: ''
  })
  const handleChange = async () => {
    if (data.password === '' || data.newpswword === '' || data.confirm === '') {
      showToast('密码不能为空!')
    } else if (data.newpswword !== data.confirm) {
      showToast('两次密码输入不一致,重新输入!')
      data.newpswword = ''
      data.confirm = ''
    } else {
      try {
        const result = await post('/pswChange', {
          password: data.password,
          newpswword: data.newpswword,
          id: userInfo.id
        })
        if (result === 'ok') {
          showToast('改密成功，请重新登录!')
          localStorage.removeItem('isLogin')
          localStorage.removeItem('cartList')
          setTimeout(() => {
            router.push({ name: 'Login' })
          }, 2000)
        } else if (result === 'error') {
          showToast('原密码输入错误!')
          data.password = ''
        } else if (result === 'again') {
          showToast('新旧密码不能相同!')
          data.newpswword = ''
          data.confirm = ''
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { password, newpswword, confirm } = toRefs(data)
  return { password, newpswword, confirm, handleChange }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'PswChange',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { password, newpswword, confirm, handleChange } = useChangeEffect(showToast)
    return { password, newpswword, confirm, handleChange, show, toastMessage, handleBackClick }
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
  &__change-button {
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
.title__back {
  display: flex;
  line-height: 0.44rem;
  background: #fff;
  font-size: 0.16rem;
  color: #333;
  text-align: center;
  width: 0.2rem;
  margin-left: 0.18rem;
  font-size: 0.2rem;
  color: #b6b6b6;
}
</style>
