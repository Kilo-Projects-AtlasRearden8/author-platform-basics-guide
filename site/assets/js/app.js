// Author Platform Basics — site interactivity
// Created by Asdale Dynamics, LLC. Copyright (c) 2026 Asdale Dynamics, LLC.

(function () {
  'use strict';

  // Highlight the current page in the nav.
  var links = document.querySelectorAll('nav a');
  var path = window.location.pathname.split('/').pop() || 'index.html';
  links.forEach(function (link) {
    var href = link.getAttribute('href');
    if (href === path || (path === 'index.html' && href === 'index.html')) {
      link.classList.add('active');
      link.setAttribute('aria-current', 'page');
    }
  });

  // Smooth, accessible reveal for template blocks (keyboard-friendly).
  var toggles = document.querySelectorAll('[data-toggle]');
  toggles.forEach(function (toggle) {
    toggle.addEventListener('click', function (event) {
      event.preventDefault();
      var targetId = toggle.getAttribute('data-toggle');
      var target = document.getElementById(targetId);
      if (!target) return;
      var hidden = target.getAttribute('hidden') !== null;
      if (hidden) {
        target.removeAttribute('hidden');
        toggle.textContent = 'Hide template';
        target.focus();
      } else {
        target.setAttribute('hidden', '');
        toggle.textContent = 'Show template';
      }
    });
  });
})();