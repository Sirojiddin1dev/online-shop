const filter = document.querySelector(".main_filter_div");
const filterBox = document.querySelector(".main_inner_filter");
const cards = document.querySelectorAll(".card");
const itemLi = document.querySelectorAll(".main_inner_item_li");
let t = false;

if (filter && filterBox) {
  filter.addEventListener("click", () => {
    t = !t;
    filterBox.style.display = t ? "block" : "none";
    cards.forEach(card => {
      card.style.width = t ? "250px" : "385px";
    });
    itemLi.forEach(card => {
      card.style.height = t ? "400px" : "auto";
    });
  });
} else {
  console.error("Element not found");
}
