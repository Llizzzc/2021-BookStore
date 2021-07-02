<template>
  <div class="content">
    <div class="category">
      <div
        :class="{category__item: true ,'category__item--active': currentTab === item.tab}"
        v-for="item in categories"
        :key="item.name"
        @click="() => handleTabClick(item.tab)"
      >{{ item.name }}</div>
    </div>
    <div class="product">
      <div
        class="product__item"
        v-for="item in list"
        :key="item.id"
      >
        <img
          class="product__item__img"
          :src="item.imgUrl"
        >
        <div class="product__item__detail">
          <h4 class="product__item__title">{{ item.name }}</h4>
          <p class="product__item__sales">月售{{ item.sales }}件 </p>
          <p class="product__item__stocks">现有{{ item.stock }}件</p>
          <p class="product__item__price">
            <span class="product__item__yen">&yen;</span>{{ item.price }}
            <span class="product__item__origin">&yen;{{ item.oldPrice }}</span>
          </p>
          <p class="product__item__button">
            <span
              class="product__item__edit"
              @click="() => handleEdit(item.book_id)"
            >编辑</span>
            <span
              class="product__item__delete"
              @click="() => handleDelete(item.book_id)"
            >删除</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { get } from '../../utils/request'
import { reactive, toRefs, ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'

// tab类
const categories = [{
  name: '漫画',
  tab: 'cartoon'
}, {
  name: '科幻',
  tab: 'sci-fi'
}, {
  name: '美食',
  tab: 'food'
}, {
  name: '教育',
  tab: 'education'
}, {
  name: '儿童',
  tab: 'children'
}, {
  name: '法律',
  tab: 'law'
}, {
  name: '历史',
  tab: 'history'
}, {
  name: '经济',
  tab: 'financial'
}, {
  name: '娱乐',
  tab: 'amusing'
}, {
  name: '旅游',
  tab: 'travel'
}]

// tab切换逻辑
const useTabEffect = () => {
  const currentTab = ref(categories[0].tab)
  const handleTabClick = (tab) => {
    currentTab.value = tab
  }
  return { currentTab, handleTabClick }
}

// 列表相关逻辑
const useCurrentListEffect = (currentTab, shopId) => {
  const content = reactive({ list: [] })
  const getContentData = async (tab) => {
    const result = await get('/showBook', { tab: currentTab.value, id: shopId })
    content.list = result.key
  }
  watchEffect(() => { getContentData() })
  const { list } = toRefs(content)
  return { list }
}

// 编辑书籍逻辑
const useEditBookEffect = (shopId) => {
  const router = useRouter()
  const handleEdit = (BookId) => {
    router.push(`/EditShopBook/${shopId}/${BookId}`)
  }
  return handleEdit
}

// 删除书籍逻辑
const useDeleteBookEffect = (shopId) => {
  const router = useRouter()
  const handleDelete = (BookId) => {
    router.push(`/DeleteShopBook/${shopId}/${BookId}`)
  }
  return handleDelete
}

export default {
  name: 'ShopContent',
  setup () {
    const route = useRoute()
    const shopId = route.params.id
    const { currentTab, handleTabClick } = useTabEffect()
    const { list } = useCurrentListEffect(currentTab, shopId)
    const handleEdit = useEditBookEffect(shopId)
    const handleDelete = useDeleteBookEffect(shopId)
    return { list, categories, currentTab, handleTabClick, shopId, handleEdit, handleDelete }
  }
}
</script>

<style lang="scss" scoped>
.content {
  display: flex;
  position: absolute;
  left: 0;
  right: 0;
  top: 1.6rem;
  bottom: 0.5rem;
}

.category {
  overflow-y: scroll;
  width: 0.76rem;
  height: 100%;
  background: #f5f5f5;
  &__item {
    line-height: 0.4rem;
    text-align: center;
    font-size: 0.14rem;
    color: #333;
    &--active {
      background: #fff;
    }
  }
}

.product {
  overflow-y: scroll;
  flex: 1;
  &__item {
    display: flex;
    position: relative;
    padding: 0.012rem;
    margin: 0 0.16rem;
    border-bottom: 0.01rem solid #f1f1f1;
    &__detail {
      overflow: hidden;
    }
    &__img {
      width: 0.68rem;
      height: 0.68rem;
      margin-right: 0.16rem;
    }
    &__title {
      margin: 0;
      line-height: 0.2rem;
      font-size: 0.14rem;
      color: #333;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    &__sales {
      display: inline;
      margin: 0.06rem 0;
      font-size: 0.12rem;
      color: #333;
    }
    &__stocks {
      display: inline;
      margin: 0.06rem 0;
      font-size: 0.12rem;
      color: #333;
    }
    &__price {
      margin: 0;
      line-height: 0.2rem;
      font-size: 0.14rem;
      color: #e93b3b;
    }
    &__yen {
      font-size: 0.12rem;
    }
    &__origin {
      margin-left: 0.06rem;
      line-height: 0.2rem;
      font-size: 0.12rem;
      color: #999;
      text-decoration: line-through;
    }
    &__button {
      margin-bottom: 0.2rem;
      font-size: 0.17rem;
    }
    &__edit {
      background: #0091ff;
      box-shadow: 0 0.04rem 0.08rem 0 rgba(0, 145, 255, 0.32);
      border-radius: 0.04rem;
      margin-right: 0.1rem;
      color: #fff;
    }
    &__delete {
      background: red;
      box-shadow: 0 0.04rem 0.08rem 0 rgba(0, 145, 255, 0.32);
      border-radius: 0.04rem;
      margin-left: 0.05rem;
      color: #fff;
    }
  }
}
</style>
