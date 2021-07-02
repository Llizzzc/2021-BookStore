<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        新建收货地址
      </div>
      <div
        class="title__save"
        @click="handleAdd"
      >保存</div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">所在城市:</div>
        <input
          class="form__item__content"
          placeholder="如长沙市"
          v-model="city"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">小区/大厦/学校:</div>
        <input
          class="form__item__content"
          placeholder="如湖南大学"
          v-model="department"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">楼号-门牌号:</div>
        <input
          class="form__item__content"
          placeholder="如1栋三单元406"
          v-model="houseNumber"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">收货人:</div>
        <input
          class="form__item__content"
          placeholder="请填写收货人的姓名"
          v-model="name"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">联系电话:</div>
        <input
          class="form__item__content"
          placeholder="请填写收货手机号"
          v-model="phone"
        />
      </div>
    </div>
  </div>
  <Toast
    v-if="show"
    :message="toastMessage"
  />
</template>

<script>
import { reactive, toRefs } from 'vue'
import { useRouter } from 'vue-router'
import { post } from '../../utils/request'
import Toast, { useToastEffect } from '../../components/Toast'

// 增加地址逻辑
const useAddAddressEffect = (showToast) => {
  const router = useRouter()
  const userInfo = JSON.parse(localStorage.getItem('user'))
  const data = reactive({
    city: '',
    department: '',
    houseNumber: '',
    name: '',
    phone: '',
    userId: userInfo.id
  })
  const handleAdd = async () => {
    if (data.city === '' || data.department === '' || data.houseNumber === '' || data.name === '' || data.phone === '') {
      showToast('信息不能为空!')
    } else {
      try {
        const result = await post('/addAddress', {
          city: data.city,
          department: data.department,
          houseNumber: data.houseNumber,
          name: data.name,
          phone: data.phone,
          userId: data.userId
        })
        if (result === 'ok') {
          showToast('添加成功!')
          setTimeout(() => {
            router.push({ name: 'MyAddressList' })
          }, 2000)
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { city, department, houseNumber, name, phone, userId } = toRefs(data)
  return { city, department, houseNumber, name, phone, handleAdd, userId }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'AddAdddress',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { handleAdd, city, department, houseNumber, name, phone, userId } = useAddAddressEffect(showToast)
    return { handleBackClick, show, toastMessage, handleAdd, city, department, houseNumber, name, phone, userId }
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
  &__save {
    margin-right: 0.2rem;
    font-size: 0.14rem;
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
        color: #b7b7b7;
      }
    }
  }
}
</style>
