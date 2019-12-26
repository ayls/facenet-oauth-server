import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import AccessDenied from '@/components/AccessDenied'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/accessdenied',
      name: 'AccessDenied',
      component: AccessDenied,
      meta: {
        requiresAuth: false
      }
    }
  ]
})
