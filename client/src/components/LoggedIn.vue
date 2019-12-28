<template>
  <div>
    <h1>{{ msg }}</h1>
    <button v-if="$auth.isAuthenticated" @click="logout">Log out</button>
  </div>
</template>

<script>
export default {
  name: 'LoggedIn',
  data () {
    return {
      msg: null
    }
  },
  mounted () {
    this.msg = `Hi ${this.$auth.user.profile.name}`
  },
  methods: {
    logout () {
      this.$auth.logout()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  font-weight: normal;
}
button {
  background-color: #41B883;
  border: none;
  color: white;
  margin: 10px auto 10px auto;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: block;
  font-size: 16px;
}
</style>
