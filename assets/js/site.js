// Normalize explicitly entered index.html addresses to their directory URL.
if (location.pathname.endsWith('/index.html')) location.replace(location.pathname.slice(0,-10)+location.search+location.hash);
const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function setMenu(open) {
  toggle?.setAttribute('aria-expanded', String(open));
  toggle?.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  navigation?.classList.toggle('open', open);
}
toggle?.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && navigation?.classList.contains('open')) {
    setMenu(false);
    toggle.focus();
  }
});
document.querySelectorAll('[data-year]').forEach(element => element.textContent = new Date().getFullYear());

// Align the homepage support link beneath the header discovery button.
const heroSupport = document.querySelector('.hero-support');
const discoveryButton = document.querySelector('.header-join');
function alignSupportButton() {
  if (!heroSupport || !discoveryButton) return;
  if (window.innerWidth <= 640) { heroSupport.style.removeProperty('right'); return; }
  const headerBounds = discoveryButton.getBoundingClientRect();
  const heroBounds = heroSupport.closest('.main-hero').getBoundingClientRect();
  heroSupport.style.right = `${heroBounds.right - (headerBounds.left + headerBounds.width / 2) - heroSupport.offsetWidth / 2}px`;
}
alignSupportButton();
window.addEventListener('resize', alignSupportButton);
document.fonts?.ready.then(alignSupportButton);
