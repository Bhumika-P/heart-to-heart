import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source=readFileSync(new URL('../assets/js/contact.js',import.meta.url),'utf8');
function setup({enabled=false,allowLocalSending=false,fail=false}={}){
 const handlers={},status={textContent:''},button={disabled:false},note={textContent:''};let payload,reset=false;
 const values={'_u591433381397433013[first]':'Test','_u591433381397433013[last]':'Visitor','_u333905647996242475':'test@example.com','_u323937929538945427[number]':'','_u252407693101516036':'Question','_u344758540638003138':'Synthetic test','website':''};
 const choices={'.contact-time-preferences input':[{id:'am',value:'A.M.',checked:true},{id:'pm',value:'P.M.',checked:true}],'.contact-interest-options input':[{id:'interest',value:'1',checked:true}]};
 const labels={am:'A.M.',pm:'P.M.',interest:'Support Group'};
 const form={elements:{namedItem:name=>({value:values[name]})},querySelector:s=>s==='[role="status"]'?status:s==='button[type="submit"]'?button:s==='[data-contact-service-note]'?note:{textContent:labels[s.match(/for="([^"]+)"/)?.[1]]},querySelectorAll:s=>choices[s],addEventListener:(name,fn)=>handlers[name]=fn,reportValidity:()=>true,setAttribute(){},removeAttribute(){},reset(){reset=true;},dispatchEvent(){}};
 const context={document:{querySelector:()=>form},window:{heartToHeartContact:{enabled,endpoint:'https://example.cloudfunctions.net/submitMainContact',allowLocalSending}},location:{hostname:'127.0.0.1'},crypto:{randomUUID:()=> 'test-uuid'},Event:class{},fetch:async(url,options)=>{payload=JSON.parse(options.body);if(fail)throw Error('Connection failed');return {ok:true,json:async()=>({result:{ok:true,message:'Received'}})};}};
 vm.runInNewContext(source,context);
 return {button,status,send:()=>handlers.submit({preventDefault(){}}),get payload(){return payload},get reset(){return reset}};
}
test('unconfigured and ordinary local previews never submit',async()=>{for(const options of [{},{enabled:true}]){const form=setup(options);assert.equal(form.button.disabled,true);await form.send();assert.equal(form.payload,undefined);}});
test('configured authorized local test sends both time choices and visible interest name',async()=>{const form=setup({enabled:true,allowLocalSending:true});await form.send();assert.deepEqual(JSON.parse(JSON.stringify(form.payload.data.bestTimes)),['A.M.','P.M.']);assert.equal(form.payload.data.interests[0],'Support Group');assert.equal(form.reset,true);assert.equal(form.status.textContent,'Received');});
test('network failure preserves entries and re-enables SEND',async()=>{const form=setup({enabled:true,allowLocalSending:true,fail:true});await form.send();assert.equal(form.reset,false);assert.equal(form.button.disabled,false);assert.equal(form.status.textContent,'Connection failed');});
