<template>
  <div class="position">
    <span class="iconfont position__icon">&#xe620;</span>
    时间:{{ nowDate }}
    <span class="iconfont position__bell">&#xe70b;</span>
  </div>
  <div class="slogan">最是书香能致远,腹有诗书气自华</div>
  <div class="banner">
    <img
      class="banner__img"
      src="../../img/others/1.jpg"
    />
  </div>
  <div class="icons">
    <div
      class="icons__item"
      v-for="(item, index) in iconList"
      :key="index"
    >
      <img
        class="icons__item__img"
        :src="item.imgUrl"
      />
      <p class="icons__item__desc">{{ item.desc }}</p>
    </div>
  </div>
  <div class="gap"></div>
</template>

<script>
export default {
  name: 'StaticPart',
  data () {
    return {
      nowDate: '' // 当前日期
    }
  },
  methods: {
    currentTime () {
      setInterval(this.formatDate, 500)
    },
    formatDate () {
      // eslint-disable-next-line prefer-const
      let date = new Date()
      // eslint-disable-next-line prefer-const
      let year = date.getFullYear() // 年
      // eslint-disable-next-line prefer-const
      let month = date.getMonth() + 1 // 月
      // eslint-disable-next-line prefer-const
      let day = date.getDate() // 日
      // eslint-disable-next-line prefer-const
      let week = date.getDay() // 星期
      // eslint-disable-next-line prefer-const
      let weekArr = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
      let hour = date.getHours() // 时
      hour = hour < 10 ? '0' + hour : hour // 如果只有一位，则前面补零
      let minute = date.getMinutes() // 分
      minute = minute < 10 ? '0' + minute : minute // 如果只有一位，则前面补零
      let second = date.getSeconds() // 秒
      second = second < 10 ? '0' + second : second // 如果只有一位，则前面补零
      this.nowDate = `${year}/${month}/${day} ${hour}:${minute}:${second} ${weekArr[week]}`
    }
  },
  mounted () {
    this.currentTime()
  },
  // 销毁定时器
  beforeUnmount () {
    if (this.formatDate) {
      clearInterval(this.formatDate) // 在Vue实例销毁前，清除时间定时器
    }
  },
  setup () {
    const iconList = [
      {
        desc: '漫画',
        tab: 'cartoon',
        imgUrl: require('../../img/icons/1.jpg')
      },
      {
        desc: '科幻',
        tab: 'sci-fi',
        imgUrl: require('../../img/icons/2.jpg')
      },
      {
        desc: '美食',
        tab: 'food',
        imgUrl: require('../../img/icons/3.jpg')
      },
      {
        desc: '教育',
        tab: 'education',
        imgUrl: require('../../img/icons/4.jpg')
      },
      {
        desc: '儿童',
        tab: 'children',
        imgUrl: require('../../img/icons/5.jpg')
      },
      {
        desc: '法律',
        tab: 'law',
        imgUrl: require('../../img/icons/6.jpg')
      },
      {
        desc: '历史',
        tab: 'history',
        imgUrl: require('../../img/icons/7.jpg')
      },
      {
        desc: '经济',
        tab: 'financial',
        imgUrl: require('../../img/icons/8.jpeg')
      },
      {
        desc: '娱乐',
        tab: 'amusing',
        imgUrl: require('../../img/icons/9.jpg')
      },
      {
        desc: '旅游',
        tab: 'travel',
        imgUrl: require('../../img/icons/10.jpg')
      }
    ]
    return { iconList }
  }
}
</script>

<style lang="scss" scoped>
.position {
  position: relative;
  overflow: hidden;
  padding: 0.16rem 0.24rem 0.16rem;
  line-height: 0.22rem;
  font-size: 0.16rem;
  white-space: nowrap;
  text-overflow: ellipsis;
  .position__icon {
    position: relative;
    font-size: 0.2rem;
    color: red;
  }
  .position__bell {
    position: absolute;
    right: 0;
    top: 0.17rem;
    font-size: 0.2rem;
    color: gold;
  }
}

.slogan {
  line-height: 0.32rem;
  background: #f5f5f5;
  color: #b7b7b7;
  border-radius: 0.19rem;
  font-size: 0.14rem;
  float: right;
  color: black;
  font-weight: bold;
}

.banner {
  &__img {
    width: 100%;
  }
}

.icons {
  display: flex;
  flex-wrap: wrap;
  background: #fff;
  &__item {
    width: 20%;
    margin-top: 0.1rem;
  }
  &__item__img {
    display: block;
    width: 0.4rem;
    height: 0.4rem;
    margin: 0 auto;
    border-radius: 0.3rem;
  }
  &__item__desc {
    text-align: center;
    margin: 0.16rem 0 0.16rem 0;
  }
}

.gap {
  height: 0.1rem;
  background: #b7b7b7;
}
</style>
