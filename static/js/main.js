// Handle "Details" button to toggle dropdown visibility
document.querySelectorAll(".details-btn").forEach((button) => {
  button.addEventListener("click", () => {
    const dropdown = button.nextElementSibling;
    dropdown.classList.toggle("d-none"); // Toggle visibility
  });
});

// Handle main room toggle to activate/deactivate sensors
document.querySelectorAll(".room-toggle").forEach((toggle) => {
  toggle.addEventListener("change", () => {
    const card = toggle.closest(".room-card");
    const statusDot = card.querySelector(".status-dot");

    if (toggle.checked) {
      // Sensor activated
      card.dataset.active = "true";
      statusDot.classList.remove("bg-danger");
      statusDot.classList.add("bg-success");
    } else {
      // Sensor deactivated
      card.dataset.active = "false";
      statusDot.classList.remove("bg-success");
      statusDot.classList.add("bg-danger");
    }
  });
});
