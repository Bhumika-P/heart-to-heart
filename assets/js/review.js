// Local-only forms: do not transmit or persist client information.
for (const form of document.querySelectorAll('[data-local-form]')) {
  const button = form.querySelector('[data-preview-submit]');
  const status = form.querySelector('[role="status"]');
  for (const group of form.querySelectorAll('[data-checkbox-required]')) {
    const boxes = [...group.querySelectorAll('input[type="checkbox"]')];
    const update = () => boxes[0].setCustomValidity(boxes.some(box => box.checked) ? '' : 'Choose at least one option.');
    group.addEventListener('change', update);
    update();
  }
  for (const select of form.querySelectorAll('select[required]')) {
    const update = () => select.setCustomValidity(select.value === '----' || select.value === '--' ? 'Choose an option.' : '');
    select.addEventListener('change', update);
    update();
  }
  button.type = 'submit';
  form.addEventListener('submit', event => {
    event.preventDefault();
    status.textContent = 'This is a local review. Your information has not been sent or saved. The private submission service will be connected before launch.';
  });
}
