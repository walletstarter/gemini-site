(async function(){
  const events=await (window.WS_METRICS?WS_METRICS.getAll():[]);
  const stats={};
  events.forEach(e=>{stats[e.alias]=(stats[e.alias]||0)+1;});
  const container=document.getElementById('stats');
  Object.keys(stats).forEach(k=>{var p=document.createElement('p');p.textContent=k+': '+stats[k];container.appendChild(p);});
  document.getElementById('export').addEventListener('click',function(){
    const header=['ts','alias','clickid','variant','lang','page'];
    const rows=events.map(e=>header.map(h=>JSON.stringify(e[h]||'')).join(','));
    const csv=[header.join(',')].concat(rows).join('\n');
    const blob=new Blob([csv],{type:'text/csv'});
    const a=document.createElement('a');
    const d=new Date();
    a.download='ws_clicks_'+d.toISOString().slice(0,10).replace(/-/g,'')+'.csv';
    a.href=URL.createObjectURL(blob);
    a.click();
  });
})();
