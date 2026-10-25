import test from 'node:test';
import assert from 'node:assert/strict';
import {validateContact,notificationText} from '../functions/contact-validation.js';
const valid=()=>({firstName:'Test',lastName:'Visitor',email:'TEST@example.com',phone:'',subject:'Question',message:'Synthetic contact test.',bestTimes:['A.M.','P.M.','Weekdays are best'],interests:['Support Group','Emotional Abuse Recovery Coaching'],website:'',requestId:'synthetic-123'});
test('preserves all selected time preferences and interests for email',()=>{const data=validateContact(valid());assert.equal(data.email,'test@example.com');assert.equal(data.bestTimes.length,3);const mail=notificationText(data);assert.match(mail,/A\.M\., P\.M\., Weekdays are best/);assert.match(mail,/Support Group, Emotional Abuse Recovery Coaching/);assert.match(mail,/Synthetic contact test/);});
test('rejects spam honeypot and header injection',()=>{assert.throws(()=>validateContact({...valid(),website:'spam'}));assert.throws(()=>validateContact({...valid(),email:'test@example.com\r\nBcc: other@example.com'}));assert.throws(()=>validateContact({...valid(),subject:'Question\nInjected'}));});
test('rejects unknown choices, missing required input and oversized comments',()=>{for(const changes of [{bestTimes:[]},{interests:['Unapproved']},{firstName:''},{message:''},{message:'x'.repeat(5001)},{requestId:'../../x'}])assert.throws(()=>validateContact({...valid(),...changes}));});
test('normalizes repeated selections without losing distinct choices',()=>{assert.deepEqual(validateContact({...valid(),bestTimes:['A.M.','A.M.','P.M.']}).bestTimes,['A.M.','P.M.']);});

test('accepts every visible interest label from the published form',()=>{for(const interest of ['Open-Heart Coaching for Emotional Healing','Marriage/Family/Relationship Restoration Coaching','Emotional Abuse Recovery Coaching','Support Group','Other'])assert.equal(validateContact({...valid(),interests:[interest]}).interests[0],interest);});
