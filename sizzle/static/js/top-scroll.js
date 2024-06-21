window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("scrollToTopBtn").style.display = "block";
  } else {
    document.getElementById("scrollToTopBtn").style.display = "none";
  }
}

function scrollToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

const nav = document.querySelector('header');

    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        nav.classList.add('header');
      } else {
        nav.classList.remove('header');
      }
    });