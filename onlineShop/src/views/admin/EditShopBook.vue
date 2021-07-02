<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        编辑书籍
      </div>
      <div
        class="title__save"
        @click="handleUpdata"
      >修改</div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">库存:</div>
        <input
          class="form__item__content"
          :placeholder="item.stock"
          v-model="stock"
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
        <div class="form__item__label">现价:</div>
        <input
          class="form__item__content"
          :placeholder="item.price"
          v-model="price"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">原价:</div>
        <input
          class="form__item__content"
          :placeholder="item.oldPrice"
          v-model="oldPrice"
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

// 修改书籍逻辑
const useUpdataAddressEffect = (showToast) => {
  const route = useRoute()
  const router = useRouter()
  const data = reactive({
    stock: '',
    sales: '',
    price: '',
    oldPrice: ''
  })
  const handleUpdata = async () => {
    try {
      const result = await post('/updateShopBook', {
        shopId: route.params.id,
        bookId: route.params.bookId,
        stock: data.stock,
        sales: data.sales,
        price: data.price,
        oldPrice: data.oldPrice
      })
      if (result === 'ok') {
        showToast('修改成功!')
        setTimeout(() => {
          router.push({ name: 'TheShop' })
        }, 2000)
      }
    } catch (e) {
      showToast('请求失败!')
    }
  }
  const { stock, sales, price, oldPrice } = toRefs(data)
  return { handleUpdata, stock, sales, price, oldPrice }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

// 获取当前书籍信息
const useBookInfoEffect = () => {
  const route = useRoute()
  const data = reactive({ item: {} })
  const getItemData = async () => {
    const result = await get('/theShopBook', { shopId: route.params.id, bookId: route.params.bookId })
    data.item = result
  }
  const { item } = toRefs(data)
  return { item, getItemData }
}

export default {
  name: 'EditShopBook',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { item, getItemData } = useBookInfoEffect()
    const { handleUpdata, stock, sales, price, oldPrice } = useUpdataAddressEffect(showToast)
    getItemData()
    return { item, handleBackClick, show, toastMessage, handleUpdata, stock, sales, price, oldPrice }
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
