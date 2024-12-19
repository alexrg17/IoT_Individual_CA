// Handle "Details" button to toggle dropdown visibility
document.querySelectorAll(".details-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const dropdown = button.nextElementSibling;
    dropdown.classList.toggle("d-none"); // Bootstrap class to hide/show
  });
});
