<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        编辑收货地址
      </div>
      <div
        class="title__save"
        @click="handleUpdata"
      >修改</div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">所在城市:</div>
        <input
          class="form__item__content"
          :placeholder="item.city"
          v-model="city"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">小区/大厦/学校:</div>
        <input
          class="form__item__content"
          :placeholder="item.department"
          v-model="department"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">楼号-门牌号:</div>
        <input
          class="form__item__content"
          :placeholder="item.houseNumber"
          v-model="houseNumber"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">收货人:</div>
        <input
          class="form__item__content"
          :placeholder="item.name"
          v-model="name"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">联系电话:</div>
        <input
          class="form__item__content"
          :placeholder="item.phone"
          v-model="phone"
        />
      </div>
    </div>
    <div
      class="delate"
      @click="handleDelete"
    > 删除</div>
  </div>
  <Toast
    v-if="show"
    :message="toastMessage"
  />
</template>

<script>
import { reactive, toRefs } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { post, get } from '../../utils/request'
import Toast, { useToastEffect } from '../../components/Toast'

// 获得当前地址逻辑
const useAddressInfoEffect = () => {
  const route = useRoute()
  const data = reactive({ item: {} })
  const getItemData = async () => {
    const result = await get('/currentAddress', { id: route.params.id })
    data.item = result
  }
  const { item } = toRefs(data)
  return { item, getItemData }
}

// 修改地址逻辑
const useUpdataAddressEffect = (showToast) => {
  const route = useRoute()
  const router = useRouter()
  const data = reactive({
    id: route.params.id,
    city: '',
    department: '',
    houseNumber: '',
    name: '',
    phone: ''
  })
  const handleUpdata = async () => {
    try {
      const result = await post('/updateAddress', {
        id: data.id,
        city: data.city,
        department: data.department,
        houseNumber: data.houseNumber,
        name: data.name,
        phone: data.phone
      })
      if (result === 'ok') {
        showToast('修改成功!')
        setTimeout(() => {
          router.push({ name: 'MyAddressList' })
        }, 2000)
      }
    } catch (e) {
      showToast('请求失败!')
    }
  }
  const { name, phone, houseNumber, department, city } = toRefs(data)
  return { handleUpdata, name, phone, houseNumber, department, city }
}

// 删除地址逻辑
const useDeletAddressEffect = (showToast) => {
  const route = useRoute()
  const router = useRouter()
  const handleDelate = async () => {
    try {
      const result = await post('/deleteAddress', {
        id: route.params.id
      })
      if (result === 'ok') {
        showToast('删除成功!')
        setTimeout(() => {
          router.push({ name: 'MyAddressList' })
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
  name: 'UpdateAddress',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { item, getItemData } = useAddressInfoEffect()
    const handleDelete = useDeletAddressEffect(showToast)
    const { handleUpdata, name, phone, houseNumber, department, city } = useUpdataAddressEffect(showToast)
    getItemData()
    return { item, getItemData, handleBackClick, show, toastMessage, handleUpdata, handleDelete, name, phone, houseNumber, department, city }
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
