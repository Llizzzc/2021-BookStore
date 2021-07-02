import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import(/* webpackChunkName: "Home" */ '../views/home/Home')
  },
  {
    path: '/Admin',
    name: 'Admin',
    component: () => import(/* webpackChunkName: "Admin" */ '../views/admin/Admin'),
    beforeEnter: (to, from, next) => {
      const { isLogin } = localStorage
      isLogin ? next({ name: 'AdminHome' }) : next()
    }
  },
  {
    path: '/AdminHome',
    name: 'AdminHome',
    component: () => import(/* webpackChunkName: "AdminHome" */ '../views/admin/AdminHome')
  },
  {
    path: '/AllShop',
    name: 'AllShop',
    component: () => import(/* webpackChunkName: "AllShop" */ '../views/admin/AllShop')
  },
  {
    path: '/AllBook',
    name: 'AllBook',
    component: () => import(/* webpackChunkName: "AllBook" */ '../views/admin/AllBook')
  },
  {
    path: '/EditShop/:id',
    name: 'EditShop',
    component: () => import(/* webpackChunkName: "EditShop" */ '../views/admin/EditShop')
  },
  {
    path: '/DeleteShop/:id',
    name: 'DeleteShop',
    component: () => import(/* webpackChunkName: "DeleteShop" */ '../views/admin/DeleteShop')
  },
  {
    path: '/AddShop',
    name: 'AddShop',
    component: () => import(/* webpackChunkName: "AddShop" */ '../views/admin/AddShop')
  },
  {
    path: '/TheShop/:id',
    name: 'TheShop',
    component: () => import(/* webpackChunkName: "TheShop" */ '../views/admin/TheShop')
  },
  {
    path: '/AddShopBook/:id',
    name: 'AddShopBook',
    component: () => import(/* webpackChunkName: "AddShopBook" */ '../views/admin/AddShopBook')
  },
  {
    path: '/AddBook',
    name: 'AddBook',
    component: () => import(/* webpackChunkName: "AddBook" */ '../views/admin/AddBook')
  },
  {
    path: '/EditShopBook/:id/:bookId?',
    name: 'EditShopBook',
    component: () => import(/* webpackChunkName: "EditShopBook" */ '../views/admin/EditShopBook')
  },
  {
    path: '/EditBook/:id',
    name: 'EditBook',
    component: () => import(/* webpackChunkName: "EditBook" */ '../views/admin/EditBook')
  },
  {
    path: '/DeleteShopBook/:id/:bookId?',
    name: 'DeleteShopBook',
    component: () => import(/* webpackChunkName: "DeleteShopBook" */ '../views/admin/DeleteShopBook')
  },
  {
    path: '/DeleteBook/:id',
    name: 'DeleteBook',
    component: () => import(/* webpackChunkName: "DeleteBook" */ '../views/admin/DeleteBook')
  },
  {
    path: '/CartList',
    name: 'CartList',
    component: () => import(/* webpackChunkName: "CartList" */ '../views/cartList/CartList')
  },
  {
    path: '/DeleteUser',
    name: 'DeleteUser',
    component: () => import(/* webpackChunkName: "DeleteUser" */ '../views/deleteUser/DeleteUser')
  },
  {
    path: '/OrderList',
    name: 'OrderList',
    component: () => import(/* webpackChunkName: "OrderList" */ '../views/orderList/OrderList')
  },
  {
    path: '/PersonalInfo',
    name: 'PersonalInfo',
    component: () => import(/* webpackChunkName: "PersonalInfo" */ '../views/personalInfo/PersonalInfo')
  },
  {
    path: '/MyAddressList',
    name: 'MyAddressList',
    component: () => import(/* webpackChunkName: "MyAddressList" */ '../views/myAddressList/MyAddressList')
  },
  {
    path: '/AddAddress',
    name: 'AddAddress',
    component: () => import(/* webpackChunkName: "AddAddress" */ '../views/addAddress/AddAddress')
  },
  {
    path: '/UpdateAddress/:id',
    name: 'UpdateAddress',
    component: () => import(/* webpackChunkName: "UpdateAddress" */ '../views/updateAddress/UpdateAddress')
  },
  {
    path: '/ChooseAddressList/:id',
    name: 'ChooseAddressList',
    component: () => import(/* webpackChunkName: "ChooseAddressList" */ '../views/chooseAddressList/ChooseAddressList')
  },
  {
    path: '/OrderConfirmation/:id/:addressId?',
    name: 'OrderConfirmation',
    component: () => import(/* webpackChunkName: "OrderConfirmation" */ '../views/orderConfirmation/OrderConfirmation')
  },
  {
    path: '/Shop/:id',
    name: 'Shop',
    component: () => import(/* webpackChunkName: "Shop" */ '../views/shop/Shop')
  },
  {
    path: '/PswChange',
    name: 'PswChange',
    component: () => import(/* webpackChunkName: "PswChange" */ '../views/pswChange/PswChange')
  },
  {
    path: '/UsernameChange',
    name: 'UsernameChange',
    component: () => import(/* webpackChunkName: "UsernameChange" */ '../views/usernameChange/UsernameChange')
  },
  {
    path: '/Register',
    name: 'Register',
    component: () => import(/* webpackChunkName: "Register" */ '../views/register/Register'),
    // 访问注册页面就会判断
    beforeEnter: (to, from, next) => {
      const { isLogin } = localStorage
      isLogin ? next({ name: 'Home' }) : next()
    }
  },
  {
    path: '/Login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "Login" */ '../views/login/Login'),
    // 访问登录页面就会判断
    beforeEnter: (to, from, next) => {
      const { isLogin } = localStorage
      isLogin ? next({ name: 'Home' }) : next()
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 每次路由跳转都会执行
router.beforeEach((to, from, next) => {
  const { isLogin } = localStorage
  const { name } = to
  const isLoginOrRegister = (name === 'Login' || name === 'Register' || name === 'Admin');
  (isLogin || isLoginOrRegister) ? next() : next({ name: 'Login' })
})

export default router
