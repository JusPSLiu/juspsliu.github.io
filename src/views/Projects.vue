<template>
  <div class="ProjectsPage">
    <!--FILTER REGION-->
    <div style="display:flex;justify-content: center;align-items: center;user-select: none">
      <div class="filtercontainer closed">
        <h3 style="margin:0 10px;margin-right:30%;text-shadow:2px 2px #000;font: 60px 'Jersey 10', sans-serif;">Filters</h3>
        <label class="filter"><input type="checkbox" value="class_project" unchecked><span class="class_project">&nbsp;Class Project&nbsp;</span></label> <label class="filter"><input type="checkbox" value="game_jam" unchecked><span class="game_jam"><img class="imgicon" onerror="this.style.display='none'"> Game Jam</span></label> <label class="filter"><input type="checkbox" value="group" unchecked><span class="group"><img class="imgicon" onerror="this.style.display='none'"> Group Project</span></label> <label class="filter"><input type="checkbox" value="solo" unchecked><span class="solo"><img class="imgicon" onerror="this.style.display='none'"> Solo Project</span></label> <label class="filter"><input type="checkbox" value="program" unchecked><span class="program"><img class="imgicon" onerror="this.style.display='none'"> Program</span></label> <label class="filter"><input type="checkbox" value="godot" unchecked><span class="godot"><img class="imgicon" onerror="this.style.display='none'"> Godot</span></label> <label class="filter"><input type="checkbox" value="unity" unchecked><span class="unity"><img class="imgicon" onerror="this.style.display='none'"> Unity</span></label> <label class="filter"><input type="checkbox" value="python" unchecked><span class="python"><img class="imgicon" onerror="this.style.display='none'"> Python</span></label> <label class="filter"><input type="checkbox" value="cpp" unchecked><span class="cpp"><img class="imgicon" onerror="this.style.display='none'"> C++</span></label> <label class="filter"><input type="checkbox" value="cs" unchecked><span class="cs"><img class="imgicon" onerror="this.style.display='none'"> C#</span></label> <label class="filter"><input type="checkbox" value="postgres" unchecked><span class="postgres"><img class="imgicon" onerror="this.style.display='none'"> PostgreSQL</span></label> <label class="filter"><input type="checkbox" value="java" unchecked><span class="java"><img class="imgicon" onerror="this.style.display='none'"> Java</span></label> <label class="filter"><input type="checkbox" value="vue" unchecked><span class="vue"><img class="imgicon" onerror="this.style.display='none'"> Vue.js</span></label> <label class="filter"><input type="checkbox" value="nim" unchecked><span class="nim"><img class="imgicon" onerror="this.style.display='none'"> Nim</span></label> <label class="filter"><input type="checkbox" value="vhdl" unchecked><span class="vhdl"><img class="imgicon" onerror="this.style.display='none'"> VHDL</span></label>
      </div>
    </div>
    <div><button id="filteropener">v</button></div>

    <!--LIST OF PROJECTS; to be filled by javascript loading the json-->
    <div id="projectlist"></div>
  </div>
</template>

<script>
import DOMPurify from "dompurify";

export default {
  name: 'Projects',
  mounted() {
    function img_url(string) { return "files/screenshots/"+string; }
    
    import("@/assets/projectlist.json").then((data) => {
      let tagslist = data.tagslist;
      // VERIFY THE TAGS LIST IS SANITIZED
      for (let i=0;i<tagslist.length;i++) {
        tagslist[i][0] = DOMPurify.sanitize(tagslist[i][0], { USE_PROFILES: { } });
        tagslist[i][1] = DOMPurify.sanitize(tagslist[i][1], { USE_PROFILES: { } });
        tagslist[i][2] = (tagslist[i][2] === true)
      }

      // LOAD THE CONTENTS
      let projectlist = document.querySelector("#projectlist");
      if (projectlist == null) return

      for (let i=0;i<data["size"];i++) {
        // SANITIZE
        let newline = DOMPurify.sanitize(data[i.toString()], { USE_PROFILES: { } });
        // SPLIT
        let newdata = newline.split("\n");

        let newDiv = document.createElement('div');
        // add title and img
        let stringstream = `<div class="img_container" style="background-image:url('`+img_url(newdata[4])+`')"></div>
        <div class="txt_container">
          <strong><span class="title">`+newdata[0]+`</span></strong>`
        
        stringstream += '<div class="details" style="margin-top:5px;">'
        // Parse the tags
        let newtags = newdata[3].split(" ")
        let tagnames = []
        for (let i=0;i<newtags.length;i++) {
          let tag_int = parseInt(newtags[i]);
          // verify valid
          if (isNaN(tag_int) || tag_int < 0 || tag_int >= tagslist.length)
          {console.log("Could not parse tag \""+newtags[i]+"\"");continue}
          // add tag
          stringstream += ' <span class="iconblock '+tagslist[tag_int][0]+'">'
          // add icon if exists
          if (tagslist[tag_int][2]) stringstream += '<img class="imgicon" onerror="this.style.display=\'none\'"> '
          stringstream += tagslist[tag_int][1]+'</span>'
          tagnames += " "+tagslist[tag_int][0]
        }
        // the div needs tag names too for easier filtering
        newDiv.setAttribute('class', 'module'+tagnames);

        // links
        stringstream += `</div>
        <div class="links">`
        if (newdata[1])
          stringstream += `<p><a class='github' href="`+newdata[1]+`"><img class="imgicon" onerror="this.style.display='none'"> Source Code</a></p>`
        if (newdata[2])
          stringstream += `<p><a class='game_jam' href="`+newdata[2]+`"><img class="imgicon" onerror="this.style.display='none'"> Runnable Version</a></p>`

        // bottomtext
        newDiv.innerHTML += stringstream+`</div>
          <p class="bottomtext">`+newdata[5]+`</p>
        </div>`;
        projectlist.appendChild(newDiv);
      }

      // SET THE FILTERS
      let filters = document.querySelectorAll("label.filter input[type='checkbox']");
      filters.forEach(element => {
        element.addEventListener('change', filterContents);
      });

      filterContents();

      // SET THE FILTER OPENER BUTTON
      let opener = document.querySelector("button#filteropener");
      opener.addEventListener('click', openFilters);

      // RESET THE BACKGROUND NOW
      this.$root.resetBackground()
    })

    function filterContents() {
      // get current filter
      let filter_checkboxes = document.querySelectorAll("label.filter input");
      let filter_list = []
      filter_checkboxes.forEach(checkbox => {
        if (checkbox.checked) {filter_list.push(checkbox.value)}
      });

      // if filter length is zero, deactivate filter
      let deactivate = (filter_list.length == 0);

      // filter things
      let projectlist = document.querySelector("#projectlist").children;
      projectlist = Array.from(projectlist);
      projectlist.forEach(element => {
        let kept = false;
        if (deactivate) {kept = true}
        else filter_list.forEach(filter => {
          if (element.classList.contains(filter)) {
            kept = true;
          }
        });
        // if this ones not kept, then set
        if (kept) {element.classList.remove("hidden")}
        else {element.classList.add("hidden")}
      });
    }

    function openFilters() {
      let filter = document.querySelector(".filtercontainer")
      let showbutton = document.querySelector("button#filteropener")
      if (filter.classList.contains("closed")) {
        document.documentElement.style.setProperty('--filter-scrollheight', (filter.scrollHeight-10) + 'px');
        filter.classList.remove("closed")
        showbutton.textContent = "^";
      } else {
        filter.classList.add("closed")
        showbutton.textContent = "v";
      }
    }
  }
}
</script>