<template>
  <header>
    <h1>Jus Liu</h1>
    <a class='github' href="https://github.com/JusPSLiu">
      <img class="imgicon"> GitHub
    </a>
    <a class='lnkdn' href="https://www.linkedin.com/in/jus-liu-77b032291">
      <img class="imgicon"> LinkedIn
    </a>
    <nav>
      <h2>
        <router-link class="navlink" to="/">About</router-link>
        -
        <router-link class="navlink" to="/projects">Projects</router-link>
      </h2>
    </nav>
  </header>
  <div class="container">
    <router-view v-slot="{Component}">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
  <footer>
    <p>Jus Liu</p>
  </footer>
  
</template>


<script>
export default {
  name: 'Projects',
  mounted() {/*
    let navlinks = document.querySelectorAll(".navlink");
    navlinks.forEach(element => {
      element.addEventListener("click", disabley())
    });

    function disabley() {
      let active_navlink = document.querySelector(".router-link-active");
      active_navlink.nextElementSibling.removeClass("hidden")
    }*/
  },
  methods: {
    resetBackground() {resetBack()}
  }
}


// BACKGROUND SCRIPT
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
const scroll_scales = [0.7, 0.2, 0.1, 0.08, 0.05, 0.02]
const stars = []

function resize() {
  ctx.canvas.width = window.innerWidth;
  ctx.canvas.height = window.innerHeight;

  redraw()
}
function resetBack() {
  ctx.canvas.width  = window.innerWidth;
  ctx.canvas.height = window.innerHeight;

  let canvas_width = window.innerWidth;
  let canvas_height = document.documentElement.scrollHeight;
  let screen_height = window.innerHeight - 5;

  stars.length = 0

  let layer = 0;
  for (let i=0;i<59;i++) {
    if (i % 10 == 9) layer += 1
    let x = Math.random() * canvas_width;
    let y = Math.random() * ((canvas_height-screen_height)*scroll_scales[layer]+screen_height);
    stars.push(new star(x, y, layer));
  }

  resize()
}

var starTimeout = null;
function redraw(reset = false) {
  let scrollTop = document.documentElement.scrollTop;
  checkScrollSpeed(performance.now());
  let tempoportion = deltaTime*0.01
  inertia = (inertia*(2-tempoportion)+speed*tempoportion)/2

  let reds = []
  let grens = []
  let blues = []

  for (let i=0;i<scroll_scales.length;i++) {
    let localnertia = inertia*scroll_scales[i]
    let colordiff = Math.round(Math.min(Math.abs(localnertia*6), 200));
    let subtracted = (255-colordiff).toString(16);
    let halfsubtracted = (255-Math.round(colordiff*0.8)).toString(16);

    reds.push(("#ff"+subtracted+subtracted));
    grens.push(("#"+halfsubtracted+"ff"+halfsubtracted));
    blues.push(("#"+subtracted+subtracted+"ff"));
  }

  // CLEAR
  ctx.clearRect(0,0, window.innerWidth, window.innerHeight)
  ctx.reset()

  stars.forEach((element) => {
    let oldPos = element.y-(scrollTop-inertia)*scroll_scales[element.layer];
    let newPos = element.y-scrollTop*scroll_scales[element.layer];
    let width = 3-(element.layer*0.25);
    let red=reds[element.layer], blue=blues[element.layer], relgren=grens[element.layer]
    let green = ctx.createLinearGradient(0, oldPos, 0, newPos);
    green.addColorStop(0.1, red);green.addColorStop(0.5,relgren);green.addColorStop(0.9, blue);
    // LINE BETWEEN
    ctx.fillStyle = green;
    ctx.fillRect(element.x-width, newPos, width*2, oldPos-newPos);

    // PAST POSITION
    ctx.fillStyle = red;
    let circle = new Path2D();
    circle.arc(element.x, oldPos, width, 0, 2 * Math.PI);
    ctx.fill(circle);

    // NEW POSITION
    ctx.fillStyle = blue;
    let circle2 = new Path2D();
    circle2.arc(element.x, newPos, width, 0, 2 * Math.PI);
    ctx.fill(circle2);
  });

  // TOP COVERER FOR NON-CHROMIUM USERS
  if (scrollTop < 10) {
    ctx.fillStyle = '#111'
    ctx.fillRect(0, 0, ctx.canvas.width, 200);
  }

  if (reset && Math.abs(inertia) > 0.1) {
    requestAnimationFrame(redraw, true);
  }
}

addEventListener("DOMContentLoaded", () => {
  resetBack()
})
addEventListener("scroll", () => {
  if (starTimeout != null) clearTimeout(starTimeout);
  starTimeout = setTimeout(redraw, 66, true)
  redraw()
})
class star {
  x = 0;y = 0;layer=0
  constructor(x, y, layer){
    this.x=x;this.y=y;this.layer=layer;
  }
}

var lastPos, lastTime, speed=0, inertia=0, deltaTime=0;
function checkScrollSpeed(timestamp){
  // repeat failsafe
  if (timestamp-lastTime < 8) return speed;
  
  let currPos = window.scrollY;
  
  // reset failsafe
  if (timestamp-lastTime > 40) {
    lastPos = currPos;
    lastTime = timestamp;
    return 0;
  }

  let delta = 0;
  if (lastPos != null){
    deltaTime = timestamp - lastTime;
    delta *= deltaTime;
    delta = currPos - lastPos;
  }
  lastTime = timestamp;
  lastPos = currPos;
  speed = delta*3;
}
</script>