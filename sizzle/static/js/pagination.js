$(document).ready(function () {
    var boxesPerPage = 6;
  
    function showBoxes(pageNumber) {
      var startIndex = (pageNumber - 1) * boxesPerPage;
      var endIndex = startIndex + boxesPerPage;
  
      $("#box-container .col-6").hide();
      $("#box-container .col-6").slice(startIndex, endIndex).show();
  
      if (pageNumber === 1) {
        $("html, body").animate({ scrollTop: 0 }, 500);
      } else {
        $("html, body").animate(
          { scrollTop: $("#box-container .col-6").first().offset().top },
          500
        );
      }
    }
  
    var totalBoxes = $("#box-container .col-6").length;
  
    var totalPages = Math.ceil(totalBoxes / boxesPerPage);
  
    // Number btn in pagination
    $(".page-link.text-body-emphasis").on("click", function () {
      $(".page-link.active").removeClass("active");
  
      $(this).addClass("active");
  
      var pageNumber = parseInt($(this).text());
  
      showBoxes(pageNumber);
      console.log(pageNumber);
  
      return false;
    });
  
    //   Prev btn
    $(".prev").on("click", function () {
      var currentPage = parseInt(
        $(".page-link.text-body-emphasis.active").text()
      );
      console.log(currentPage);
      if (!isNaN(currentPage) && currentPage > 1) {
        $(".page-link.text-body-emphasis").removeClass("active");
        $(".page-link.text-body-emphasis").each(function (i, e) {
          var teks = $(this).text().trim();
  
          if (teks === `${currentPage - 1}`) {
            $(this).addClass("active");
  
            return false;
          }
        });
        showBoxes(currentPage - 1);
      } else {
        showBoxes(1);
      }
  
      return false;
    });
  
    // Next btn
    $(".next").on("click", function () {
      var currentPage = parseInt(
        $(".page-link.text-body-emphasis.active").text()
      );
      if (!isNaN(currentPage) && currentPage < 3) {
        $(".page-link.text-body-emphasis").removeClass("active");
        $(".page-link.text-body-emphasis").each(function (i, e) {
          var teks = $(this).text().trim();
  
          if (teks === `${currentPage + 1}`) {
            $(this).addClass("active");
  
            return false;
          }
        });
        showBoxes(currentPage + 1);
      } else {
        showBoxes(3);
      }
  
      return false;
    });
  
    showBoxes(1);
  });
  