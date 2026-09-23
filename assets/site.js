(function(){
  function slug(s){
    return s.toLowerCase().trim().replace(/&/g,'and').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
  }
  
  // Prevent scroll jump: add IDs before browser tries to scroll to hash
  function initTOC(){
    const main = document.querySelector('main');
    if(!main) return;

    // Collapsible class/lineage pages handle their own hash navigation.
    if(main.querySelector('.lineages-container')) return;
    
    // Add IDs to headings FIRST (before any scroll happens)
    const headings = Array.from(main.querySelectorAll('h2, h3'))
      .filter(h => !h.closest('.toc') && !h.closest('[data-toc-skip]'));
    headings.forEach(h=>{ if(!h.id) h.id = slug(h.textContent); });
    
    // Build TOC
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
    
    // Handle hash navigation AFTER IDs are set
    // This prevents the jump because the target element now exists
    if(window.location.hash){
      requestAnimationFrame(()=>{
        const target = document.querySelector(window.location.hash);
        if(target){
          // Use scrollIntoView with smooth behavior
          target.scrollIntoView({behavior:'smooth',block:'start'});
        }
      });
    }
  }
  
  // Compact "On this page" accordion on phone/tablet; sidebar stays open on desktop.
  function enhanceCollapsibleTocs(){
    const mq = window.matchMedia('(min-width: 1164px)');

    function syncOpen(details){
      if(mq.matches){
        details.open = true;
        details.dataset.forceOpen = '1';
      } else if(details.dataset.forceOpen === '1'){
        details.open = false;
        delete details.dataset.forceOpen;
      }
    }

    document.querySelectorAll('.toc').forEach(toc => {
      if(toc.querySelector(':scope > .toc-details')) return;

      const heading = toc.querySelector(':scope > h2');
      const label = (heading && heading.textContent.trim()) || 'On this page';
      const details = document.createElement('details');
      details.className = 'toc-details';
      const summary = document.createElement('summary');
      summary.className = 'toc-summary';
      summary.textContent = label;
      if(heading && heading.id) summary.id = heading.id;

      const panel = document.createElement('div');
      panel.className = 'toc-panel';

      Array.from(toc.childNodes).forEach(node => {
        if(node === heading) return;
        panel.appendChild(node);
      });
      if(heading) heading.remove();

      details.appendChild(summary);
      details.appendChild(panel);
      toc.appendChild(details);
      toc.classList.add('toc--collapsible');

      panel.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', () => {
          if(!mq.matches) details.open = false;
        });
      });

      syncOpen(details);
    });

    const onBreakpoint = () => {
      document.querySelectorAll('.toc-details').forEach(syncOpen);
    };
    if(typeof mq.addEventListener === 'function') mq.addEventListener('change', onBreakpoint);
    else if(typeof mq.addListener === 'function') mq.addListener(onBreakpoint);
  }

  // Glossary term hover/focus tips: copy <dd> text onto a.term[href^="#g-"]
  function initTermTooltips(){
    document.querySelectorAll('a.term[href^="#g-"]').forEach(a => {
      if(a.getAttribute('data-tip')) return;
      const id = a.getAttribute('href').slice(1);
      if(!id) return;
      const dt = document.getElementById(id);
      const dd = dt && dt.nextElementSibling;
      if(!dd || dd.tagName !== 'DD') return;
      const tip = dd.textContent.replace(/\s+/g, ' ').trim();
      if(!tip) return;
      a.setAttribute('data-tip', tip);
    });
  }

  // Run as early as possible to set IDs before browser scrolls
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', () => {
      initTOC();
      enhanceCollapsibleTocs();
      initTermTooltips();
    });
  } else {
    // DOM already ready, run immediately
    initTOC();
    enhanceCollapsibleTocs();
    initTermTooltips();
  }
  
  // Tab functionality for gear page
  function initGearTabs(){
    const tabButtons = document.querySelectorAll('.gear-tabs .tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    if(tabButtons.length === 0) return;
    
    tabButtons.forEach(button => {
      button.addEventListener('click', () => {
        const targetTab = button.getAttribute('data-tab');
        
        // Remove active class from all buttons and contents
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        const targetContent = document.getElementById(targetTab + '-tab');
        if(targetContent){
          targetContent.classList.add('active');
        }
      });
    });
  }
  
  // Initialize gear tabs
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initGearTabs);
  } else {
    initGearTabs();
  }
})();