import Vue from 'vue'
import Router from 'vue-router'
import LoggedIn from '@/components/LoggedIn'
import { authGuard } from '@/services/AuthGuard'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'LoggedIn',
      component: LoggedIn,
      beforeEnter: authGuard
    }
  ]
})
