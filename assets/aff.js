(function(){
  function variant(){return window.WS_AB?WS_AB.variant():'A';}
  function base36Hash(str){var h=0;for(var i=0;i<str.length;i++){h=((h<<5)-h)+str.charCodeAt(i);h|=0;}return (h>>>0).toString(36).slice(0,8);}
  function rand6(){return Math.floor(Math.random()*0xffffffff).toString(36).slice(0,6);}
  function clickidFor(url){var u=new URL(url,location.origin);var cid=u.searchParams.get('subId')||u.searchParams.get('clickref');if(cid)return cid;var d=new Date();var pad=n=>String(n).padStart(2,'0');var ts=d.getFullYear()+pad(d.getMonth()+1)+pad(d.getDate())+pad(d.getHours())+pad(d.getMinutes())+pad(d.getSeconds());var lang=(navigator.language||'').slice(0,2).toUpperCase()||'ZZ';cid=ts+'-'+rand6()+'-'+lang+'-'+variant()+'-'+base36Hash(location.pathname+location.search);return cid;}
  function decorate(el){var url;if(typeof el==='string'){url=new URL(el,location.origin);}else if(el instanceof HTMLAnchorElement){url=new URL(el.getAttribute('href'),location.origin);}else{return el;}
    var params=new URLSearchParams(location.search);
    params.forEach(function(v,k){if(k.startsWith('utm_')&&!url.searchParams.has(k))url.searchParams.set(k,v);});
    if(!url.searchParams.has('ref'))url.searchParams.set('ref',location.hostname);
    if(!url.searchParams.has('page'))url.searchParams.set('page',encodeURIComponent(location.pathname+location.search));
    if(params.get('llm')==='1'&&!url.searchParams.has('llm'))url.searchParams.set('llm','1');
    var cid=clickidFor(url);
    if(!url.searchParams.has('subId'))url.searchParams.set('subId',cid);
    if(!url.searchParams.has('clickref'))url.searchParams.set('clickref',cid);
    if(typeof el==='string')return url.toString();
    el.href=url.pathname+url.search;
    el.rel='sponsored noopener nofollow';
    el.referrerPolicy='origin-when-cross-origin';
    el.addEventListener('click',function(){if(window.WS_METRICS){var utm={};params.forEach(function(v,k){if(k.startsWith('utm_'))utm[k]=v;});WS_METRICS.record({ts:new Date().toISOString(),alias:url.pathname.split('/').pop().replace(/\.html$/,''),clickid:cid,variant:variant(),lang:(navigator.language||'').slice(0,2).toUpperCase()||'ZZ',page:location.pathname+location.search,utm:utm});}}, {once:true});
    return el;}
  function decorateAll(){document.querySelectorAll('a[href^="/go/"]').forEach(decorate);}
  document.addEventListener('DOMContentLoaded',decorateAll);
  new MutationObserver(decorateAll).observe(document.body,{childList:true,subtree:true});
  window.WS_AFF={decorate:decorate,clickidFor:clickidFor};
})();
