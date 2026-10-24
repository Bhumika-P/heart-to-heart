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
