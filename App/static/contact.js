/* contact page form logic */

async function submitForm() {
  const fname    = document.getElementById('fname')?.value.trim();
  const lname    = document.getElementById('lname')?.value.trim();
  const email    = document.getElementById('email')?.value.trim();
  const org      = document.getElementById('org')?.value.trim();
  const enquiry  = document.getElementById('enquiry')?.value;
  const message  = document.getElementById('message')?.value.trim();

  if (!fname || !lname || !email || !message) {
    alert('Please fill in your name, email, and message before sending.');
    return;
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    alert('Please enter a valid email address.');
    return;
  }

  const btn = document.querySelector('#contact-form .btn-primary');
  if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

  try {
    const formData = new FormData();
    formData.append('fname',   fname);
    formData.append('lname',   lname);
    formData.append('name',    fname + ' ' + lname);
    formData.append('email',   email);
    formData.append('org',     org || '');
    formData.append('enquiry', enquiry || '');
    formData.append('message', message);

    const res = await fetch('/contact/submit', {
      method: 'POST',
      body: formData
    });

    if (res.ok || res.redirected) {
      const form    = document.getElementById('contact-form');
      const success = document.getElementById('form-success');
      if (form && success) {
        form.style.display    = 'none';
        success.style.display = 'block';
      }
    } else {
      alert('Something went wrong. Please try again or email us directly.');
      if (btn) { btn.disabled = false; btn.textContent = 'Send Message'; }
    }
  } catch (err) {
    alert('Something went wrong. Please try again or email us directly.');
    if (btn) { btn.disabled = false; btn.textContent = 'Send Message'; }
  }
}