<template>
  <div
    class="iconfont title__back"
    @click="handleBackClick"
  >&#xe602;</div>
  <div class="wrapper">
    <div class="wrapper__input">
      <input
        class="wrapper__input__content"
        placeholder="请输入新用户名"
        v-model="username"
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
    username: ''
  })
  const handleChange = async () => {
    if (data.username === '') {
      showToast('用户名不能为空!')
    } else {
      try {
        const result = await post('/usernameChange', {
          username: data.username,
          id: userInfo.id
        })
        if (typeof result !== 'string') {
          const userInfo = {
            id: result.id,
            name: result.username
          }
          localStorage.setItem('user', JSON.stringify(userInfo))
          showToast('修改成功!')
          setTimeout(() => {
            router.push({ name: 'PersonalInfo' })
          }, 2000)
        } else if (result === 'exist') {
          showToast('该用户名已存在!')
          data.username = ''
        } else if (result === 'again') {
          showToast('新旧用户名不能相同!')
          data.username = ''
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { username } = toRefs(data)
  return { username, handleChange }
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
    const { username, handleChange } = useChangeEffect(showToast)
    return { username, handleChange, show, toastMessage, handleBackClick }
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
