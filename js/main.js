/* ==========================================================================
   Rowan IEEE — Shared Script
   Handles: page transitions, mobile nav, active nav link, EmailJS, footer year.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Restore page if browser restores from bfcache after a leave transition */
  window.addEventListener("pageshow", function (event) {
    if (event.persisted) {
      document.body.classList.remove("is-leaving");
    }
  });

  /* Smooth exit when navigating between internal pages */
  function isInternalNav(anchor) {
    if (!anchor || !anchor.href) return false;
    if (anchor.target && anchor.target !== "_self") return false;
    if (anchor.hasAttribute("download")) return false;
    var url;
    try {
      url = new URL(anchor.href, window.location.href);
    } catch (err) {
      return false;
    }
    if (url.origin !== window.location.origin) return false;
    if (url.pathname === window.location.pathname && url.hash) return false;
    var next = url.pathname + url.search + url.hash;
    var here = window.location.pathname + window.location.search + window.location.hash;
    return next !== here;
  }

  if (!reduceMotion) {
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) {
        return;
      }
      var anchor = e.target.closest("a");
      if (!isInternalNav(anchor)) return;

      e.preventDefault();
      document.body.classList.add("is-leaving");
      setTimeout(function () {
        window.location.href = anchor.href;
      }, 220);
    });
  }

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
        toggle.setAttribute("aria-expanded", "false");
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
