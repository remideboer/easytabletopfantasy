(function(){
  function slug(s){
    return s.toLowerCase().trim().replace(/&/g,'and').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
  }
  const main = document.querySelector('main');
  if(!main) return;
  const headings = Array.from(main.querySelectorAll('h2, h3'));
  headings.forEach(h=>{ if(!h.id) h.id = slug(h.textContent); });
  const tocHost = document.querySelector('[data-toc]');
  if(tocHost && headings.length){
    const ul = document.createElement('ul');
    headings.forEach(h=>{
      const li = document.createElement('li');
      li.className = 'toc-' + h.tagName.toLowerCase();
      const a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      li.appendChild(a);
      ul.appendChild(li);
    });
    tocHost.textContent = '';
    tocHost.appendChild(ul);
  }
})();