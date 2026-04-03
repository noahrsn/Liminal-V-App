'use strict';

/* ============================================================
   LIMINAL V – main.js
   ============================================================ */

// ---- Nav: scroll behaviour ---------------------------------
const header   = document.getElementById('header');
const SCROLL_THRESHOLD = 40;

// ---- Nav: mobile burger ------------------------------------
const burger   = document.getElementById('navBurger');
const navList  = document.getElementById('navList');
const backdrop = document.getElementById('navBackdrop');

function closeNav() {
  navList.classList.remove('is-open');
  burger.classList.remove('is-active');
  burger.setAttribute('aria-expanded', 'false');
  backdrop.classList.remove('is-visible');
  document.body.style.overflow = '';
}

burger.addEventListener('click', () => {
  const isOpen = navList.classList.toggle('is-open');
  burger.classList.toggle('is-active', isOpen);
  burger.setAttribute('aria-expanded', String(isOpen));
  backdrop.classList.toggle('is-visible', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

// Close on nav link click
navList.addEventListener('click', (e) => {
  if (e.target.closest('.nav__link')) closeNav();
});

// Close on backdrop click
backdrop.addEventListener('click', closeNav);

// ---- Hero: logo + content fade on scroll -------------------
const heroEl      = document.querySelector('.hero');
const heroLogo    = document.querySelector('.hero__logo');
const heroContent = document.querySelector('.hero__content');
const heroBgEl    = document.querySelector('.hero__bg');

function onHeroScroll() {
  const scrollY = window.scrollY;

  // Nav background
  header.classList.toggle('header--scrolled', scrollY > SCROLL_THRESHOLD);

  if (!heroEl) return;

  // Logo & content fade out — logo exits faster than the rest
  const heroH    = heroEl.offsetHeight;
  const progress = Math.min(scrollY / (heroH * 0.45), 1);

  if (heroLogo) {
    heroLogo.style.opacity   = Math.max(1 - progress * 2.2, 0);
    heroLogo.style.transform = `translateY(${scrollY * 0.45}px)`;
  }
  if (heroContent) {
    heroContent.style.opacity   = Math.max(1 - progress * 1.4, 0);
    heroContent.style.transform = `translateY(${scrollY * 0.12}px)`;
  }

  // Hero background parallax
  if (heroBgEl) {
    heroBgEl.style.transform = `translateY(${scrollY * 0.3}px)`;
  }
}

window.addEventListener('scroll', onHeroScroll, { passive: true });
onHeroScroll(); // run once

// ---- Nav: active link on scroll ----------------------------
const sections = Array.from(document.querySelectorAll('section[id]'));
const navLinks = Array.from(document.querySelectorAll('.nav__link[href^="#"]'));

function updateActiveLink() {
  const scrollY = window.scrollY + 120;
  let current = '';
  sections.forEach((sec) => {
    if (scrollY >= sec.offsetTop) current = sec.id;
  });
  navLinks.forEach((link) => {
    link.classList.toggle('nav__link--active', link.getAttribute('href') === `#${current}`);
  });
}
window.addEventListener('scroll', updateActiveLink, { passive: true });

// ---- Gallery: placeholder fallback -------------------------
document.querySelectorAll('.gallery__item img').forEach((img) => {
  img.addEventListener('error', () => {
    img.closest('.gallery__item').classList.add('gallery__item--placeholder');
  });
});

// ---- Contact form ------------------------------------------
const form        = document.getElementById('contactForm');
const submitBtn   = document.getElementById('submitBtn');
const feedback    = document.getElementById('formFeedback');

function showFeedback(msg, type) {
  feedback.textContent = msg;
  feedback.className = `form__feedback form__feedback--${type}`;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  feedback.textContent = '';
  feedback.className = 'form__feedback';

  const name    = form.name.value.trim();
  const email   = form.email.value.trim();
  const message = form.message.value.trim();

  if (!name || !email || !message) {
    showFeedback('Bitte fülle alle Pflichtfelder aus.', 'error');
    return;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showFeedback('Bitte gib eine gültige E-Mail-Adresse ein.', 'error');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = 'Wird gesendet …';

  const payload = {
    name,
    email,
    event_type: form.event_type.value,
    date:        form.date.value,
    message,
  };

  try {
    const res = await fetch('/api/contact', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });
    const data = await res.json();

    if (data.success) {
      showFeedback('Deine Anfrage ist angekommen – wir melden uns bald! 🎸', 'success');
      form.reset();
    } else {
      showFeedback(data.error || 'Ein Fehler ist aufgetreten. Bitte versuche es erneut.', 'error');
    }
  } catch {
    showFeedback('Verbindungsfehler. Bitte prüfe deine Internetverbindung.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Anfrage absenden';
  }
});
