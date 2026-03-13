/* showwise master .js*/

/* nav shadow */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 10);
  });
}

/* navbar togle (hambutger) */
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', isOpen);
  });

  // close menu when a nav link is clicked
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('open');
      hamburger.setAttribute('aria-expanded', false);
    });
  });
}

/* contact form submit */
function submitForm() {
  const fname   = document.getElementById('fname')?.value.trim();
  const lname   = document.getElementById('lname')?.value.trim();
  const email   = document.getElementById('email')?.value.trim();
  const message = document.getElementById('message')?.value.trim();

  if (!fname || !lname || !email || !message) {
    alert('Please fill in your name, email, and message before sending.');
    return;
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }

  const form    = document.getElementById('contact-form');
  const success = document.getElementById('form-success');
  if (form && success) {
    form.style.display    = 'none';
    success.style.display = 'block';
  }
}

/* faq togle */
function toggleFaq(btn) {
  const answer = btn.nextElementSibling;
  const icon   = btn.querySelector('span');
  const isOpen = answer.classList.toggle('open');
  if (icon) icon.textContent = isOpen ? '−' : '+';
}