<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        编辑店铺
      </div>
      <div
        class="title__save"
        @click="handleUpdata"
      >修改</div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">书店名:</div>
        <input
          class="form__item__content"
          :placeholder="item.title"
          v-model="title"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">月售:</div>
        <input
          class="form__item__content"
          :placeholder="item.sales"
          v-model="sales"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">起送:</div>
        <input
          class="form__item__content"
          :placeholder="item.expressLimit"
          v-model="expressLimit"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">配送费:</div>
        <input
          class="form__item__content"
          :placeholder="item.expressPrice"
          v-model="expressPrice"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">标语:</div>
        <input
          class="form__item__content"
          :placeholder="item.slogan"
          v-model="slogan"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">图片:</div>
        <input
          class="form__item__content"
          type="file"
          @change="onChange($event)"
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
import { useRouter, useRoute } from 'vue-router'
import { post, get } from '../../utils/request'
import Toast, { useToastEffect } from '../../components/Toast'

// 获取当前商铺信息
const useShopInfoEffect = () => {
  const route = useRoute()
  const data = reactive({ item: {} })
  const getItemData = async () => {
    const result = await get('/showShop', { id: route.params.id })
    data.item = result
  }
  const { item } = toRefs(data)
  return { item, getItemData }
}

// 修改信息逻辑
const useUpdataAddressEffect = (showToast) => {
  const route = useRoute()
  const router = useRouter()
  const data = reactive({
    id: route.params.id,
    title: '',
    sales: '',
    expressLimit: '',
    expressPrice: '',
    slogan: '',
    imgUrl: ''
  })
  const onChange = (e) => {
    data.imgUrl = e.target.files[0].name
  }
  const handleUpdata = async () => {
    try {
      const result = await post('/updateShop', {
        id: data.id,
        title: data.title,
        sales: data.sales,
        expressLimit: data.expressLimit,
        expressPrice: data.expressPrice,
        slogan: data.slogan,
        imgUrl: data.imgUrl
      })
      if (result === 'ok') {
        showToast('修改成功!')
        setTimeout(() => {
          router.push({ name: 'AllShop' })
        }, 2000)
      } else if (result === 'exist') {
        showToast('店名已被注册!')
      }
    } catch (e) {
      showToast('请求失败!')
    }
  }
  const { title, sales, expressLimit, expressPrice, slogan } = toRefs(data)
  return { handleUpdata, title, sales, expressLimit, expressPrice, slogan, onChange }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'EditShop',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { item, getItemData } = useShopInfoEffect()
    const { handleUpdata, title, sales, expressLimit, expressPrice, slogan, onChange } = useUpdataAddressEffect(showToast)
    getItemData()
    return { item, handleBackClick, show, toastMessage, handleUpdata, title, sales, expressLimit, expressPrice, slogan, onChange }
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
</style>
