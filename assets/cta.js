(function(){
  function load(){
    var slot=document.getElementById('cta-slot');
    if(slot){
      var v=window.WS_AB?WS_AB.variant():'A';
      fetch('partials/cta_'+v+'.html').then(r=>r.text()).then(html=>{
        slot.innerHTML=html;
        if(window.WS_AFF) slot.querySelectorAll('a[href^="/go/"]').forEach(a=>WS_AFF.decorate(a));
      });
    }
    fetch('partials/schema.html').then(r=>r.text()).then(html=>{
      var div=document.createElement('div');div.innerHTML=html;document.head.appendChild(div.firstElementChild);
    });
  }
  document.addEventListener('DOMContentLoaded',load);
})();
