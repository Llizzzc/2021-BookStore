<template>
  <div class="wrapper">
    <div class="title">
      <div
        class="iconfont title__back"
        @click="handleBackClick"
      >&#xe602;</div>
      <div class="title__text">
        增加书籍
      </div>
      <div
        class="title__save"
        @click="handleAdd"
      >确定</div>
    </div>
    <div class="form">
      <div class="form__item">
        <div class="form__item__label">类别:</div>
        <input
          class="form__item__content"
          placeholder="如cartoon"
          v-model="tab"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">书名:</div>
        <input
          class="form__item__content"
          placeholder="如西游记"
          v-model="name"
        />
      </div>
      <div class="form__item">
        <div class="form__item__label">封面:</div>
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

// 增加书籍逻辑
const useAddAddressEffect = (showToast) => {
  const router = useRouter()
  const data = reactive({
    tab: '',
    name: '',
    imgUrl: ''
  })
  const onChange = (e) => {
    data.imgUrl = e.target.files[0].name
  }
  const handleAdd = async () => {
    if (data.tab === '' || data.name === '' || data.imgUrl === '') {
      showToast('信息不能为空!')
    } else {
      try {
        const result = await post('/addBook', {
          tab: data.tab,
          name: data.name,
          imgUrl: data.imgUrl

        })
        if (result === 'ok') {
          showToast('添加成功!')
          setTimeout(() => {
            router.push({ name: 'AllBook' })
          }, 2000)
        } else if (result === 'exist') {
          showToast('该书已存在，请勿重复添加!')
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { tab, name, imgUrl } = toRefs(data)
  return { handleAdd, tab, name, imgUrl, onChange }
}

// 点击回退
const useHandleBack = () => {
  const router = useRouter()
  const handleBackClick = () => { router.back() }
  return handleBackClick
}

export default {
  name: 'AddBook',
  components: { Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const handleBackClick = useHandleBack()
    const { handleAdd, tab, name, imgUrl, onChange } = useAddAddressEffect(showToast)
    return { handleBackClick, show, toastMessage, handleAdd, tab, name, imgUrl, onChange }
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
