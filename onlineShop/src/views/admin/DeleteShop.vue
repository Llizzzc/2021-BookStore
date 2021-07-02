<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        关闭店铺
      </div>
      <div class="title__save"></div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">书店名:</div>
        <div class="form__item__content">
          {{ item.title }}
        </div>
      </div>
      <div class="form__item">
        <div class="form__item__label">月售:</div>
        <div class="form__item__content">
          {{ item.sales }}
        </div>
      </div>
      <div class="form__item">
        <div class="form__item__label">起送:</div>
        <div class="form__item__content">
          {{ item.expressLimit }}
        </div>
      </div>
      <div class="form__item">
        <div class="form__item__label">配送费:</div>
        <div class="form__item__content">
          {{ item.expressPrice }}
        </div>
      </div>
      <div class="form__item">
        <div class="form__item__label">标语:</div>
        <div class="form__item__content">
          {{ item.slogan }}
        </div>
      </div>
    </div>
    <div
      class="delate"
      @click="handleDelete"
    >关闭</div>
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

// 删除逻辑
const useUpdataAddressEffect = (showToast) => {
  const router = useRouter()
  const route = useRoute()
  const handleDelete = async () => {
    try {
      const result = await post('/deleteShop', {
        id: route.params.id
      })
      if (result === 'ok') {
        showToast('关闭成功!')
        setTimeout(() => {
          router.push({ name: 'AllShop' })
        }, 2000)
      }
    } catch (e) {
      showToast('请求失败!')
    }
  }
  return { handleDelete }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'DeleteShop',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const { item, getItemData } = useShopInfoEffect()
    const handleBackClick = useHandleBack()
    const { handleDelete } = useUpdataAddressEffect(showToast)
    getItemData()
    return { handleBackClick, show, toastMessage, handleDelete, item }
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
.delate {
  margin: 0.18rem;
  line-height: 0.32rem;
  background: crimson;
  color: #f8f8f8;
  text-align: center;
  border-radius: 0.04rem;
}
</style>
