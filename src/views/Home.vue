<template>
  <div class="Homepage">
    <div class="description">
      <h3>Hello</h3>
      <p>My name is Jus, I'm a currently a Computer Science Graduate student at UNCC, proficient in C++, C, Java, and Python. I've maintained a 4.0 GPA throughout college, so I've been on the Chancellor's List for every semester attended.</p>
    </div>
    <div style="margin-top:100px;" class="module">
      <div class="img_container" style="background-image:url('files/docs/cs-bs.jpg');filter:brightness(80%);"></div>
      <div class="txt_container">
        <strong><span class="title">Bachelor of Science Degree</span></strong>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  mounted() {
    // RESET THE BACKGROUND NOW
    this.$root.resetBackground()
  }
}
</script>