const filter = document.getElementById("filter");
const allItems = Array.from(document.querySelectorAll("#box-container .col-6"));



filter.addEventListener("input", (e) => filterData(e.target.value));

function filterData(search) {
    allItems.forEach((item) => {
        const h5 = item.querySelector("h5");
        if (h5.innerText.toLowerCase().includes(search.toLowerCase())) {
            item.classList.remove('d-none');
        } else {
            item.classList.add("d-none");
        }
    });
}


