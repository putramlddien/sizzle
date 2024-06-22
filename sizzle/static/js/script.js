document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");
  const headBanner = document.querySelector("section.head-banner");
  const navbar = document.querySelector(".navbar");
  const hamburger = document.querySelector(".navbar-toggler");
  let isHeaderColored = false;

  window.addEventListener("scroll", () => {
    const scrollPosition = window.scrollY;

    if (scrollPosition > 50 && !isHeaderColored) {
      header.style.backgroundColor = "#198CD6";
      headBanner.style.display = "none";
      headBanner.classList.add("hidden");
      isHeaderColored = true;
    } else if (scrollPosition <= 50 && isHeaderColored) {
      console.log("scroll <= 50");
      header.style.backgroundColor = "transparent";
      headBanner.style.display = "flex";
      headBanner.classList.remove("hidden");
      navbar.style.backgroundColor = "transparent";
      isHeaderColored = false;
    }
  });

  if (hamburger) {
    hamburger.addEventListener("click", () => {
      if (!isHeaderColored) {
        header.style.backgroundColor = "#198CD6";
        navbar.style.backgroundColor = "#198CD6";
        headBanner.style.display = "none";
        isHeaderColored = true;
      } else {
        header.style.backgroundColor = "transparent";
        navbar.style.backgroundColor = "transparent";
        headBanner.style.display = "flex";
        isHeaderColored = false;
      }
    });
  }
});

function getDynamicPageUrl() {
  console.log(window.location.href);
  return window.location.href;
}

(function () {
  var d = document,
    s = d.createElement("script");
  s.src = "https://sizzle-2.disqus.com/embed.js";
  s.setAttribute("data-timestamp", +new Date());
  (d.head || d.body).appendChild(s);
})();
