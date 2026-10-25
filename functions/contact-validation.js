const interests = new Set(['Open-Heart Coaching for Emotional Healing','Marriage/Family/Relationship Coaching','Emotional Abuse Recovery Coaching','Support Group','Other']);
const times = new Set(['A.M.','P.M.','Weekdays are best','Weekends are best','Anytime is okay']);
function text(value, label, max, required = true) {
  if (typeof value !== 'string') throw Error(`${label} is invalid.`);
  const result = value.trim();
  if ((required && !result) || result.length > max || /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/u.test(result)) throw Error(`${label} is invalid.`);
  return result;
}
function choices(value, allowed, label) {
  if (!Array.isArray(value) || !value.length || value.length > allowed.size || value.some(item => !allowed.has(item))) throw Error(`Choose ${label}.`);
  return [...new Set(value)];
}
export function validateContact(data) {
  if (!data || typeof data !== 'object' || data.website) throw Error('Unable to submit this form.');
  const firstName = text(data.firstName,'First name',120), lastName = text(data.lastName,'Last name',120);
  const email = text(data.email,'Email address',254).toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw Error('Enter a valid email address.');
  const phone = text(data.phone,'Phone number',60,false);
  const subject = text(data.subject,'Subject',160);
  if (subject === '----' || /[\r\n]/.test(subject)) throw Error('Choose a subject.');
  const requestId = text(data.requestId,'Request',80);
  if (!/^[a-zA-Z0-9_-]+$/.test(requestId)) throw Error('Invalid request.');
  return {firstName,lastName,email,phone,subject,requestId,message:text(data.message,'Comment',5000),bestTimes:choices(data.bestTimes,times,'a preferred call time'),interests:choices(data.interests,interests,'an area of interest')};
}
export function notificationText(record) {
  return `Main website contact\n\nName: ${record.firstName} ${record.lastName}\nEmail: ${record.email}\nPhone: ${record.phone || 'Not provided'}\nSubject: ${record.subject}\nBest time to call: ${record.bestTimes.join(', ')}\nInterested in: ${record.interests.join(', ')}\n\nComment:\n${record.message}`;
}
