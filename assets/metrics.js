(function(){
  const dbName='ws_metrics',store='clicks';
  let db=null,useLocal=false;
  function init(){return new Promise((res,rej)=>{if(!('indexedDB'in window))return rej();const open=indexedDB.open(dbName,1);open.onupgradeneeded=()=>open.result.createObjectStore(store,{autoIncrement:true});open.onsuccess=()=>res(open.result);open.onerror=()=>rej(open.error);});}
  async function ensure(){if(db||useLocal)return db;try{db=await init();return db;}catch(e){useLocal=true;}}
  async function record(ev){if(!db&&!useLocal)await ensure();if(useLocal){const arr=JSON.parse(localStorage.getItem('ws_clicks')||'[]');arr.push(ev);localStorage.setItem('ws_clicks',JSON.stringify(arr));return;}const tx=db.transaction(store,'readwrite');tx.objectStore(store).add(ev);}
  async function getAll(){if(!db&&!useLocal)await ensure();if(useLocal){return JSON.parse(localStorage.getItem('ws_clicks')||'[]');}return new Promise(res=>{const tx=db.transaction(store,'readonly');const rq=tx.objectStore(store).getAll();rq.onsuccess=()=>res(rq.result||[]);rq.onerror=()=>res([]);});}
  document.addEventListener('DOMContentLoaded',function(){if(new URLSearchParams(location.search).get('dev')==='1'){const link=document.createElement('a');link.href='/dashboard/';link.textContent='Metrics';link.style.position='fixed';link.style.bottom='8px';link.style.right='8px';link.style.fontSize='12px';link.style.opacity='0.6';document.body.append(link);}});
  window.WS_METRICS={record, getAll};
})();
