// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App'
import router from './router'
import Mgr from './services/AuthService'

Vue.config.productionTip = false

let mgr = new Mgr()
Vue.use(VueRouter)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  if (requiresAuth) {
    mgr.getSignedIn().then(
      signedIn => {
        if (signedIn) {
          next()
        } else {
          next('/accessdenied')
        }
      },
      err => {
        console.log(err)
      }
    )
  } else {
    next()
  }
})
