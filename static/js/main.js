'use strict';

/* ============================================================
   NAVBAR: Scroll-Schatten + aktiver Link
   ============================================================ */
const navbar   = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

function onScroll() {
  // Scrolled-Klasse für Hintergrund
  navbar.classList.toggle('scrolled', window.scrollY > 60);

  // Aktiver Menüpunkt
  let current = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
  });
  navLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === '#' + current);
  });
}

window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ============================================================
   HAMBURGER-MENÜ
   ============================================================ */
const navToggle   = document.getElementById('navToggle');
const navLinksEl  = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
  const isOpen = navLinksEl.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

// Menü schließen bei Klick auf einen Link
navLinksEl.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    navLinksEl.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  });
});

// Menü schließen bei Klick außerhalb
document.addEventListener('click', e => {
  if (!navbar.contains(e.target) && navLinksEl.classList.contains('open')) {
    navLinksEl.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
});

/* ============================================================
   GALERIE-LIGHTBOX
   ============================================================ */
const lightbox      = document.getElementById('lightbox');
const lightboxImg   = document.getElementById('lightboxImg');
const lightboxClose = document.getElementById('lightboxClose');

document.getElementById('galleryGrid').addEventListener('click', e => {
  const item = e.target.closest('.gallery-item');
  if (!item) return;

  const img = item.querySelector('img');
  if (!img) return; // Platzhalter haben kein <img>

  lightboxImg.src = img.src;
  lightboxImg.alt = img.alt;
  lightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
});

function closeLightbox() {
  lightbox.classList.remove('active');
  lightboxImg.src = '';
  document.body.style.overflow = '';
}

lightboxClose.addEventListener('click', closeLightbox);

lightbox.addEventListener('click', e => {
  if (e.target === lightbox) closeLightbox();
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && lightbox.classList.contains('active')) closeLightbox();
});

/* ============================================================
   KONTAKTFORMULAR
   ============================================================ */
const form       = document.getElementById('contactForm');
const feedback   = document.getElementById('formFeedback');
const submitBtn  = document.getElementById('submitBtn');

form.addEventListener('submit', async e => {
  e.preventDefault();

  feedback.className    = 'form-feedback';
  feedback.textContent  = '';

  const data = {
    name:       form.name.value.trim(),
    email:      form.email.value.trim(),
    phone:      form.phone.value.trim(),
    event_date: form.event_date.value,
    location:   form.location.value.trim(),
    message:    form.message.value.trim(),
  };

  // Client-seitige Grundvalidierung
  if (!data.name || !data.email || !data.message) {
    showFeedback('error', 'Bitte füll alle Pflichtfelder (*) aus.');
    return;
  }

  submitBtn.classList.add('loading');
  submitBtn.disabled = true;

  try {
    const res = await fetch('/contact', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(data),
    });

    const json = await res.json();

    if (json.success) {
      showFeedback('success', json.message);
      form.reset();
    } else {
      showFeedback('error', json.error || 'Ein unbekannter Fehler ist aufgetreten.');
    }
  } catch {
    showFeedback('error', 'Netzwerkfehler – bitte prüf deine Verbindung und versuch es erneut.');
  } finally {
    submitBtn.classList.remove('loading');
    submitBtn.disabled = false;
  }
});

function showFeedback(type, text) {
  feedback.className   = `form-feedback ${type}`;
  feedback.textContent = text;
  feedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
