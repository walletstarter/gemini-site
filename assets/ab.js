(function(){
  function hash(str){var h=0;for(var i=0;i<str.length;i++){h=((h<<5)-h)+str.charCodeAt(i);h|=0;}return h;}
  function pick(){
    var m=document.cookie.match(/(?:^|; )ab_ws=([^;]+)/);
    if(m) return m[1];
    var first=localStorage.getItem('ws_firstSeen');
    if(!first){first=Date.now().toString();localStorage.setItem('ws_firstSeen',first);}
    var seed=navigator.userAgent+screen.width+screen.height+(new Date).getTimezoneOffset()+first;
    var variant=Math.abs(hash(seed))%2===0?'A':'B';
    document.cookie='ab_ws='+variant+'; Max-Age=2592000; Path=/';
    return variant;
  }
  var v=pick();
  window.WS_AB={variant:function(){return v;}};
})();
