import Vue from 'vue'
import Oidc from 'oidc-client'

/** Define a default action to perform after authentication */
const DEFAULT_REDIRECT_CALLBACK = () =>
  window.history.replaceState({}, document.title, window.location.pathname)

let instance

/** Returns the current instance of the SDK */
export const getInstance = () => instance

/** Creates an instance of the OIDC client. If one has already been created, it returns that instance */
export const useOidcClient = ({
  onRedirectCallback = DEFAULT_REDIRECT_CALLBACK,
  redirectUri = window.location.origin,
  ...options
}) => {
  if (instance) return instance

  // The 'instance' is simply a Vue object
  instance = new Vue({
    data () {
      return {
        loading: true,
        isAuthenticated: false,
        user: {},
        oidcClient: null,
        error: null
      }
    },
    methods: {
      /** Handles the callback when logging in using a redirect */
      async handleRedirectCallback () {
        this.loading = true
        try {
          this.user = await this.oidcClient.signinRedirectCallback()
          this.isAuthenticated = true
        } catch (e) {
          this.isAuthenticated = false
          this.error = e
        } finally {
          this.loading = false
        }
      },
      /** Authenticates the user using the redirect method */
      loginWithRedirect () {
        return this.oidcClient.signinRedirect()
      },
      /** Logs the user out and removes their session on the authorization server */
      async logout () {
        await this.oidcClient.signoutRedirect()
        this.user = null
        this.isAuthenticated = false
      }
    },
    /** Use this lifecycle method to instantiate the OIDC client */
    async created () {
      // Create a new instance of OIDC client using members of the given options object
      this.oidcClient = new Oidc.UserManager({
        userStore: new Oidc.WebStorageStateStore(),
        authority: options.authority,
        client_id: options.client_id,
        redirect_uri: redirectUri,
        response_type: options.response_type,
        scope: options.scope
      })

      try {
        // If the user is returning to the app after authentication..
        if (
          window.location.hash.includes('id_token=') &&
          window.location.hash.includes('state=') &&
          window.location.hash.includes('expires_in=')
        ) {
          // handle the redirect
          await this.handleRedirectCallback()
          onRedirectCallback()
        }
      } catch (e) {
        this.error = e
      } finally {
        // Initialize our internal authentication state
        this.user = await this.oidcClient.getUser()
        this.isAuthenticated = this.user != null
        this.loading = false
      }
    }
  })

  return instance
}

// Create a simple Vue plugin to expose the wrapper object throughout the application
export const OidcClientPlugin = {
  install (Vue, options) {
    Vue.prototype.$auth = useOidcClient(options)
  }
}
