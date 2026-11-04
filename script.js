const menuToggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
const themeToggle = document.querySelector('.theme-toggle');

menuToggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('.main-nav a').forEach((link) => link.addEventListener('click', () => nav.classList.remove('open')));

const savedTheme = localStorage.getItem('taurus-theme');
if (savedTheme === 'night') document.body.classList.add('night');
themeToggle?.addEventListener('click', () => {
  document.body.classList.toggle('night');
  localStorage.setItem('taurus-theme', document.body.classList.contains('night') ? 'night' : 'light');
});

document.getElementById('read-more')?.addEventListener('click', (event) => {
  const text = document.getElementById('more-text');
  const hidden = text.hasAttribute('hidden');
  text.toggleAttribute('hidden');
  event.currentTarget.innerHTML = hidden ? 'Приховати інформацію <span>−</span>' : 'Дізнатися більше <span>＋</span>';
});

const reviews = [
  { name: 'Олександр', text: 'Чудова автошкола — здав з першого разу! Інструктор справжній професіонал.' },
  { name: 'Марія', text: 'Нові машини, спокійні пояснення та дуже зручний графік. Рекомендую всім!' }
];
const reviewList = document.getElementById('reviews-list');
function escapeHtml(value) {
  return value.replace(/[&<>\'\"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
}
function renderReviews() {
  if (!reviewList) return;
  reviewList.innerHTML = reviews.map((review, index) => `<article class="review-card"><strong>${escapeHtml(review.name)}</strong><p>“${escapeHtml(review.text)}”</p><button class="review-delete" type="button" data-index="${index}">Видалити</button></article>`).join('');
  reviewList.querySelectorAll('.review-delete').forEach((button) => button.addEventListener('click', () => { reviews.splice(Number(button.dataset.index), 1); renderReviews(); }));
}
renderReviews();

document.getElementById('review-form')?.addEventListener('submit', (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  reviews.push({ name: form.elements[0].value.trim(), text: form.elements[1].value.trim() });
  renderReviews();
  form.reset();
});

document.getElementById('contact-form')?.addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const status = document.getElementById('form-status');
  if (!form.checkValidity()) { form.reportValidity(); return; }
  const payload = Object.fromEntries(new FormData(form));
  status.textContent = 'Надсилання...';
  try {
    const response = await fetch('/api/messages', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Не вдалося зберегти заявку.');
    status.textContent = data.success;
    form.reset();
  } catch (error) {
    if (window.location.protocol === 'file:') {
      status.textContent = `Дякуємо, ${payload.name}! Деморежим: для збереження в БД запустіть app.py.`;
      form.reset();
    } else status.textContent = error.message;
  }
});
