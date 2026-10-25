const contactForm = document.querySelector('[data-main-contact]');
if (contactForm) {
  const config = window.heartToHeartContact || {};
  const feedback = contactForm.querySelector('[role="status"]');
  const sendButton = contactForm.querySelector('button[type="submit"]');
  const local = ['localhost','127.0.0.1'].includes(location.hostname);
  const active = config.enabled && (!local || config.allowLocalSending);
  const value = name => contactForm.elements.namedItem(name)?.value?.trim() || '';
  let requestId = crypto.randomUUID();
  let pendingPayload = null;
  const note = contactForm.querySelector('[data-contact-service-note]');
  if (note) note.textContent = active ? 'Please share only the information needed for us to respond. Your message will be sent to Heart to Heart.' : 'Email sending is not connected in this preview. Please call 224-225-9494 for assistance.';
  sendButton.disabled = !active;
  contactForm.addEventListener('input', () => { pendingPayload = null; requestId = crypto.randomUUID(); });
  contactForm.addEventListener('submit', async event => {
    event.preventDefault();
    if (!active || sendButton.disabled) return;
    if (!contactForm.reportValidity()) return;
    const selected = selector => [...contactForm.querySelectorAll(selector)].filter(el=>el.checked).map(el=>contactForm.querySelector(`label[for="${el.id}"]`)?.textContent.trim() || el.value);
    const payload = pendingPayload || {
      firstName:value('_u591433381397433013[first]'),lastName:value('_u591433381397433013[last]'),
      email:value('_u333905647996242475'),phone:value('_u323937929538945427[number]'),
      subject:value('_u252407693101516036'),message:value('_u344758540638003138'),
      bestTimes:selected('.contact-time-preferences input'),interests:selected('.contact-interest-options input'),website:value('website'),requestId
    };
    pendingPayload = payload;
    sendButton.disabled = true;contactForm.setAttribute('aria-busy','true');feedback.textContent='Sending your message…';
    try {
      if (!/^https:\/\//.test(config.endpoint)) throw Error('Online messages are not configured. Please call us.');
      const response = await fetch(config.endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({data:payload})});
      const result = await response.json();
      if (!response.ok || !result.result?.ok) throw Error(result.error?.message || 'We could not send your message. Please try again or call us.');
      feedback.textContent=result.result.message;
      contactForm.reset();requestId=crypto.randomUUID();pendingPayload=null;
      contactForm.dispatchEvent(new Event('change',{bubbles:true}));
    } catch(error) {feedback.textContent=error.message || 'Unable to send. Your entries are still here; please try again.';}
    finally {sendButton.disabled=false;contactForm.removeAttribute('aria-busy');}
  });
}
