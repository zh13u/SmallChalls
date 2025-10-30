document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("pingForm");
  const btnPing = document.getElementById("btnPing");
  const btnContent = btnPing.querySelector(".btn-content");
  const btnLoader = btnPing.querySelector(".btn-loader");
  const output = document.getElementById("output");
  const resultsSection = document.getElementById("resultsSection");
  const input = document.getElementById("target");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    // Show loading state
    btnContent.classList.add("d-none");
    btnLoader.classList.remove("d-none");
    btnPing.disabled = true;
    
    // Hide results section
    resultsSection.classList.add("d-none");
    output.textContent = "";

    const formData = new FormData(form);
    
    try {
      const response = await fetch("/ping", {
        method: "POST",
        body: formData,
      });
      
      const data = await response.json();
      
      // Display output
      output.textContent = data.output || "No response.";
      
      // Show results section with animation
      resultsSection.classList.remove("d-none");
      
      // Scroll to results
      resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      
    } catch (err) {
      output.textContent = "Error: " + err.message;
      resultsSection.classList.remove("d-none");
    } finally {
      // Reset button state
      btnContent.classList.remove("d-none");
      btnLoader.classList.add("d-none");
      btnPing.disabled = false;
    }
  });

  // Add Enter key support
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      form.dispatchEvent(new Event("submit"));
    }
  });

  // Add focus animation
  input.addEventListener("focus", () => {
    input.parentElement.style.transform = "scale(1.02)";
  });

  input.addEventListener("blur", () => {
    input.parentElement.style.transform = "scale(1)";
  });

  // Add smooth scroll for history items
  const historyItems = document.querySelectorAll(".history-item");
  historyItems.forEach(item => {
    item.addEventListener("click", () => {
      item.style.transform = "scale(0.98)";
      setTimeout(() => {
        item.style.transform = "scale(1)";
      }, 100);
    });
  });
});
