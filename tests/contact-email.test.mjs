import test from 'node:test';
import assert from 'node:assert/strict';
import {notificationHtml} from '../functions/contact-email.js';
const record={firstName:'Jane',lastName:'Example',email:'jane@example.com',phone:'',subject:'Coaching question',interests:['Support Group'],bestTimes:['A.M.','Weekdays are best'],message:'Hello Sherée,\nI would like to learn more.'};
test('includes source, submitted preferences, message and a reply to the visitor',()=>{
 const html=notificationHtml(record);
 for(const text of ['MAIN WEBSITE CONTACT','Jane Example','Not provided','Support Group','A.M.','Weekdays are best','Hello Sherée,<br>'])assert.ok(html.includes(text));
 assert.ok(html.includes('mailto:jane%40example.com?subject=Re%3A%20Coaching%20question'));
 assert.ok(!html.includes('Dashboard'));
});
test('escapes visitor markup and prevents attribute injection',()=>{
 const html=notificationHtml({...record,firstName:'<img src=x onerror=alert(1)>',subject:'" onclick="alert(1)',message:'<script>alert(1)</script>\nA & B',email:'"@example.com',interests:['<b>untrusted</b>']});
 assert.ok(!html.includes('<script>'));assert.ok(!html.includes('<img'));
 assert.ok(html.includes('&lt;script&gt;'));assert.ok(html.includes('A &amp; B'));
 assert.ok(html.includes('&lt;b&gt;untrusted&lt;/b&gt;'));
 assert.ok(html.includes('mailto:%22%40example.com'));
});
