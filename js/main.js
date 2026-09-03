/* ==========================================================================
   Rowan IEEE — Shared Script
   Handles: mobile nav toggle, active nav link, EmailJS contact form, footer year.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  /* Mobile nav toggle */
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (toggle && header) {
    toggle.addEventListener("click", function () {
      header.classList.toggle("nav-open");
      var expanded = header.classList.contains("nav-open");
      toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
    });
    document.querySelectorAll(".nav-links a").forEach(function (link) {
      link.addEventListener("click", function () {
        header.classList.remove("nav-open");
      });
    });
  }

  /* Highlight the current page in the nav */
  var here = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav-links a").forEach(function (link) {
    var target = link.getAttribute("href");
    if (target === here || (here === "" && target === "index.html")) {
      link.classList.add("active");
    }
  });

  /* Contact form via EmailJS (same service/template as the previous React site) */
  var form = document.getElementById("contact-form");
  var status = document.getElementById("form-status");
  if (form && status) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var submitBtn = form.querySelector('button[type="submit"]');
      var name = form.name.value.trim();
      var email = form.email.value.trim();
      var message = form.message.value.trim();

      if (!name || !email || !message) {
        status.textContent = "Please fill out all fields.";
        status.classList.add("show");
        return;
      }

      if (typeof emailjs === "undefined") {
        status.textContent =
          "Could not load the mail service. Please email us using the addresses on the Team page.";
        status.classList.add("show");
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Sending...";
      }
      status.textContent = "";
      status.classList.remove("show");

      emailjs
        .send("service_0op7bv8", "template_0b1f86r", {
          name: name,
          email: email,
          message: message,
        })
        .then(function () {
          status.textContent = "Message sent — thanks! We'll get back to you soon.";
          status.classList.add("show");
          form.reset();
        })
        .catch(function () {
          status.textContent =
            "Failed to send. Please try again later, or email us using the addresses on the Team page.";
          status.classList.add("show");
        })
        .finally(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = "Send";
          }
        });
    });
  }

  /* Footer year */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();
});
