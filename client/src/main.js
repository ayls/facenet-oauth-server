// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import { OidcClientPlugin } from './services/AuthService'

Vue.config.productionTip = false

Vue.use(OidcClientPlugin, {
  authority: 'http://127.0.0.1:5001',
  client_id: 'sample-client',
  response_type: 'id_token',
  scope: 'openid',
  metadata: {
    issuer: 'sample-auth-server',
    authorization_endpoint: 'http://127.0.0.1:5001/auth',
    end_session_endpoint: 'http://127.0.0.1:5001/signout',
    jwks_uri: 'http://127.0.0.1:5001/jwks'
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
