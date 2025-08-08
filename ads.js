(function(){
  if(location.pathname.startsWith('/go/')||location.pathname.startsWith('/track/')) return;

  const AD_VARIANT = "A"; // change to "B" for alt copy/color
  const NOW = Date.now(), TTL = 7*24*60*60*1000;
  const redirect = {gemini:'/go/gemini', ledger:'/go/ledger', nord:'/go/nord'};

  const config = {
    'walletstarter.com':{
      bar:{text:'Learn crypto with Gemini and earn a bonus',btn:{A:'Open Gemini',B:'Claim Gemini Bonus'},aff:'gemini'},
      footer:{text:{A:'Open Gemini – fast signup bonus',B:'Claim Gemini Bonus'},aff:'gemini'},
      card:{headline:'Ledger – take control of your crypto',bullets:['Secure offline storage','Easy backups','Supports 5,500+ coins'],btn:{A:'Get Ledger',B:'Shop Ledger Now'},aff:'ledger'},
      sidebar:{text:'Secure your coins offline',btn:{A:'Get Ledger',B:'Shop Ledger Now'},aff:'ledger'}
    },
    'vpnworldwallet.com':{
      bar:{text:'Stay private online with NordVPN',btn:{A:'Get NordVPN',B:'Unlock NordVPN Deal'},aff:'nord'},
      footer:{text:{A:'Get NordVPN – pay with crypto',B:'Unlock NordVPN Deal'},aff:'nord'},
      card:{headline:'NordVPN – privacy for every device',bullets:['No-log policy','Pay anonymously with crypto','Fast servers worldwide'],btn:{A:'Get NordVPN',B:'Claim NordVPN Offer'},aff:'nord'},
      sidebar:{text:'NordVPN: secure your connection',btn:{A:'Get NordVPN',B:'Claim Offer'},aff:'nord'}
    }
  };

  const host = location.hostname.replace(/^www\./,'');
  const cfg = config[host];
  if(!cfg) return;
  if(AD_VARIANT==="B") document.body.classList.add('ad-variant-b');

  const params = new URLSearchParams(location.search);
  const subId = params.get('subId');

  function processAff(){
    document.querySelectorAll('a[data-aff]').forEach(a=>{
      const base = redirect[a.dataset.aff];
      if(!base) return;
      a.href = base + (subId ? '?subId=' + encodeURIComponent(subId) : '');
      a.rel = 'sponsored nofollow';
      a.referrerPolicy = 'origin';
    });
  }

  // Top promo bar
  const barKey = host + '-promoDismissed';
  const last = +localStorage.getItem(barKey)||0;
  if(NOW-last>TTL){
    const bar = document.createElement('div');
    bar.className = 'promo-bar';
    bar.setAttribute('role','region');
    bar.setAttribute('aria-label','promotion');
    const span = document.createElement('span');
    span.textContent = cfg.bar.text;
    const btn = document.createElement('a');
    btn.className='btn'; btn.dataset.aff=cfg.bar.aff;
    btn.textContent = cfg.bar.btn[AD_VARIANT];
    btn.setAttribute('aria-label',cfg.bar.btn[AD_VARIANT]);
    const close=document.createElement('button');
    close.className='close'; close.textContent='×';
    close.setAttribute('aria-label','Dismiss');
    close.onclick=()=>{bar.remove();localStorage.setItem(barKey,NOW);document.body.classList.remove('has-promo-bar');};
    bar.append(span,btn,close);
    document.body.prepend(bar);
    document.body.classList.add('has-promo-bar');
  }

  // Mobile footer CTA
  const foot=document.createElement('div');
  foot.className='mobile-cta';
  foot.setAttribute('role','region');
  foot.setAttribute('aria-label','call to action');
  const fbtn=document.createElement('a');
  fbtn.className='btn'; fbtn.dataset.aff=cfg.footer.aff;
  fbtn.textContent=cfg.footer.text[AD_VARIANT];
  fbtn.setAttribute('aria-label',cfg.footer.text[AD_VARIANT]);
  foot.append(fbtn);
  document.body.append(foot);
  if(window.matchMedia('(max-width:768px)').matches){
    document.body.classList.add('has-mobile-cta');
  }

  // In-article product card
  const firstH2=document.querySelector('h2');
  if(firstH2){
    const card=document.createElement('div');
    card.className='aff-card';
    const h3=document.createElement('h3'); h3.textContent=cfg.card.headline;
    const ul=document.createElement('ul');
    cfg.card.bullets.forEach(b=>{const li=document.createElement('li');li.textContent=b;ul.append(li);});
    const btn=document.createElement('a');
    btn.className='btn'; btn.dataset.aff=cfg.card.aff;
    btn.textContent=cfg.card.btn[AD_VARIANT];
    btn.setAttribute('aria-label',cfg.card.btn[AD_VARIANT]);
    card.append(h3,ul,btn);
    firstH2.parentNode.insertBefore(card,firstH2.nextSibling);
  }

  // Sidebar card
  const sidebar=document.querySelector('.sidebar');
  if(sidebar){
    const sc=document.createElement('div');
    sc.className='aff-card';
    const p=document.createElement('p'); p.textContent=cfg.sidebar.text;
    const btn=document.createElement('a');
    btn.className='btn'; btn.dataset.aff=cfg.sidebar.aff;
    btn.textContent=cfg.sidebar.btn[AD_VARIANT];
    btn.setAttribute('aria-label',cfg.sidebar.btn[AD_VARIANT]);
    sc.append(p,btn);
    sidebar.append(sc);
  }

  processAff();
})();
