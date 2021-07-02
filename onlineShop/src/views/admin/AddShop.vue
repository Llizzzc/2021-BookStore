<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        新开店铺
      </div>
      <div
        class="title__save"
        @click="handleUpdata"
      >确定</div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">书店名:</div>
        <input
          class="form__item__content"
          placeholder="如新华书店"
          v-model="title"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">月售:</div>
        <div class="form__item__content">{{ sales }}
        </div>
      </div>
      <div class="form__item">
        <div class="form__item__label">起送:</div>
        <input
          class="form__item__content"
          placeholder="如100"
          v-model="expressLimit"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">配送费:</div>
        <input
          class="form__item__content"
          placeholder="如20"
          v-model="expressPrice"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">标语:</div>
        <input
          class="form__item__content"
          placeholder="如全场折扣!"
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
import { useRouter } from 'vue-router'
import { post } from '../../utils/request'
import Toast, { useToastEffect } from '../../components/Toast'

// 修改信息逻辑
const useUpdataAddressEffect = (showToast) => {
  const router = useRouter()
  const data = reactive({
    title: '',
    sales: 0,
    expressLimit: '',
    expressPrice: '',
    slogan: '',
    imgUrl: ''
  })
  const onChange = (e) => {
    data.imgUrl = e.target.files[0].name
  }
  const handleUpdata = async () => {
    if (data.title === '' || data.expressLimit === '' || data.expressPrice === '' || data.sales === '' || data.imgUrl === '') {
      showToast('信息不能为空!')
    } else {
      try {
        const result = await post('/addShop', {
          title: data.title,
          sales: data.sales,
          expressLimit: data.expressLimit,
          expressPrice: data.expressPrice,
          slogan: data.slogan,
          imgUrl: data.imgUrl
        })
        if (result === 'ok') {
          showToast('开店成功!')
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
  }
  const { title, expressLimit, expressPrice, slogan, sales } = toRefs(data)
  return { handleUpdata, title, expressLimit, expressPrice, slogan, onChange, sales }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'AddShop',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { handleUpdata, title, expressLimit, expressPrice, slogan, onChange, sales } = useUpdataAddressEffect(showToast)
    return { handleBackClick, show, toastMessage, handleUpdata, title, expressLimit, expressPrice, slogan, onChange, sales }
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
