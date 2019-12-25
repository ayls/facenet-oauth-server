<template>
    <div id="app">
        <div><video ref="video" id="video" width="640" height="480" autoplay></video></div>
        <div><button id="snap" v-on:click="play()">Play</button></div>
        <div><button id="snap" v-on:click="capture()">Capture</button></div>
        <canvas ref="canvas" id="canvas" width="640" height="480"></canvas>
    </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      video: {},
      canvas: {}
    }
  },
  mounted () {
    this.video = this.$refs.video
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(stream => {
        this.video.srcObject = stream
      })
    }
  },
  methods: {
    play () {
      this.video.play()
    },
    capture () {
      this.canvas = this.$refs.canvas
      this.canvas.getContext('2d').drawImage(this.video, 0, 0, 640, 480)
    }
  }
}
</script>

<style>
    body {
        background-color: #F0F0F0;
    }
    #app {
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
    #video {
        background-color: #000000;
    }
</style>
