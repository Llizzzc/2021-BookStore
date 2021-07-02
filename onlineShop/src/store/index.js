import {
  createStore
} from 'vuex'

const setLocalCartList = (state) => {
  const {
    cartList
  } = state
  const cartListString = JSON.stringify(cartList)
  localStorage.cartList = cartListString
}

const getLocalCartList = () => {
  try {
    return JSON.parse(localStorage.cartList)
  } catch (e) {
    return {}
  }
}

export default createStore({
  state: {
    cartList: getLocalCartList()
    //   shopId: {
    //     shopName: productList: {
    //       productId: {
    //         id: name: imgUrl: sales: price: oldPrice: stock: count: check:
    //       }
    //     }
    //   }
  },
  mutations: {
    changeCartItemInfo (state, payload) {
      const {
        shopId,
        productId,
        productInfo
      } = payload
      // eslint-disable-next-line prefer-const
      let shopInfo = state.cartList[shopId] || {
        shopName: '',
        productList: {}
      }
      let product = shopInfo.productList[productId]
      if (!product) {
        productInfo.count = 0
        product = productInfo
      }
      if (payload.num > 0) {
        product.check = true
      }
      // eslint-disable-next-line no-mixed-operators
      if (product.count < product.stock && payload.num > 0 || product.count > 0 && payload.num < 0) {
        product.count = product.count + payload.num
      }
      shopInfo.productList[productId] = product
      state.cartList[shopId] = shopInfo
      setLocalCartList(state)
    },
    changeShopName (state, payload) {
      const {
        shopId,
        shopName
      } = payload
      const shopInfo = state.cartList[shopId] || {
        shopName: '',
        productList: {}
      }
      shopInfo.shopName = shopName
      state.cartList[shopId] = shopInfo
      setLocalCartList(state)
    },
    changeCartItemChecked (state, payload) {
      const {
        shopId,
        productId
      } = payload
      const product = state.cartList[shopId].productList[productId]
      product.check = !product.check
      setLocalCartList(state)
    },
    cleanCartProducts (state, payload) {
      const {
        shopId
      } = payload
      state.cartList[shopId].productList = {}
      setLocalCartList(state)
    },
    setCartItemsCheck (state, payload) {
      const {
        shopId
      } = payload
      const products = state.cartList[shopId].productList
      if (products) {
        // eslint-disable-next-line prefer-const
        for (let key in products) {
          const product = products[key]
          product.check = true
        }
      }
      setLocalCartList(state)
    },
    cleanCartData (state, shopId) {
      state.cartList[shopId].productList = {}
      setLocalCartList(state)
    }
  }
})
