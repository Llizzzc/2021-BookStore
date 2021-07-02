<template>
  <div class="warpper">
    <div class="search">
      <div
        class="search__back iconfont"
        @click="handleBackClick"
      >&#xe602;</div>
    </div>
    <ShopInfo
      :item="item"
      :hideBorder="true"
    />
    <ShopContent />
    <Toast
      v-if="show"
      :message="toastMessage"
    />
  </div>
  <div
    class="add"
    @click="handleAdd"
  >增加书籍</div>
</template>

<script>
import { get, post } from '../../utils/request'
import { useRouter, useRoute } from 'vue-router'
import { reactive, toRefs } from 'vue'
import ShopInfo from '../../components/ShopInfo'
import ShopContent from '../admin/ShopContent'
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

// 点击回退
const useBackRouterEffect = () => {
  const router = useRouter()
  const handleBackClick = () => {
    router.back()
  }
  return { handleBackClick }
}

// 点击搜索
const useSearchEffect = (showToast) => {
  const route = useRoute()
  const shopId = route.params.id
  const data = reactive({
    name: '',
    tab: 0
  })
  const handleSearchClick = async () => {
    if (data.name === '') {
      showToast('请输入商品名称!')
    } else {
      try {
        const result = await post('/search', {
          id: shopId,
          name: data.name
        })
        if (result === 'None') {
          showToast('未找到该书籍!')
        } else {
          data.tab = result
        }
      } catch (e) {
        showToast('请求失败!')
      }
    }
  }
  const { name, tab } = toRefs(data)
  return { handleSearchClick, name, tab }
}

// 增加书籍逻辑
const useAddBook = () => {
  const router = useRouter()
  const route = useRoute()
  const handleAdd = () => {
    router.push(`/AddShopBook/${route.params.id}`)
  }
  return handleAdd
}

export default {
  name: 'TheShop',
  components: { ShopInfo, ShopContent, Toast },
  setup () {
    const { show, toastMessage, showToast } = useToastEffect()
    const { handleBackClick } = useBackRouterEffect()
    const { item, getItemData } = useShopInfoEffect()
    const handleAdd = useAddBook()
    const { handleSearchClick, name, tab } = useSearchEffect(showToast)
    getItemData()
    return { item, handleBackClick, handleSearchClick, show, toastMessage, name, tab, handleAdd }
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  padding: 0 0.18rem;
}

.search {
  display: flex;
  margin: 0.2rem 0 0.16rem 0;
  &__back {
    width: 0.3rem;
    font-size: 0.3rem;
    color: #b6b6b6;
  }
}
.add {
  position: absolute;
  width: 100%;
  bottom: 0;
  line-height: 0.32rem;
  background: #0091ff;
  color: #f8f8f8;
  text-align: center;
  border-radius: 0.04rem;
}
</style>
