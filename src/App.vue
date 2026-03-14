<template>
  <h1>Jus Liu</h1>
  <a class='github' href="https://github.com/JusPSLiu">
    <img class="imgicon"> GitHub
  </a>
  <a class='lnkdn' href="https://www.linkedin.com/in/jus-liu-77b032291">
    <img class="imgicon"> LinkedIn
  </a>
  <nav>
    <h2>
      <router-link to="/">About</router-link>
      -
      <router-link to="/projects">Projects</router-link>
    </h2>
  </nav>
  <div class="container">
    <router-view />
  </div>
  <footer style="display: flex; outline-color: white">
    <p>Jus Liu</p>
  </footer>
</template>
