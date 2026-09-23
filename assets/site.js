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

  function dialogText(value){
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // In-page confirm or notice. Omit confirmLabel for a single Close button.
  // Cancel, ×, Escape, and the overlay leave the action undone.
  window.ymiatDialog = function(opts){
    opts = opts || {};
    var nl = document.documentElement.lang === 'nl';
    var title = opts.title || '';
    var message = opts.message || '';
    var notice = !opts.confirmLabel;
    var cancelLabel = opts.cancelLabel || (notice ? (nl ? 'Sluiten' : 'Close') : (nl ? 'Annuleren' : 'Cancel'));
    var closeAria = nl ? 'Sluiten' : 'Close';
    var heading = title || message;
    var body = title && message ? message : '';

    return new Promise(function(resolve){
      var settled = false;
      var overlay = document.createElement('div');
      overlay.className = 'cs-modal-overlay';
      overlay.innerHTML =
        '<div class="cs-modal cs-modal--confirm" role="dialog" aria-modal="true" aria-labelledby="ymiat-dialog-title">' +
          '<div class="cs-modal-header">' +
            '<h2 id="ymiat-dialog-title">' + dialogText(heading) + '</h2>' +
            '<button type="button" class="cs-modal-close" data-ymiat-dialog-dismiss aria-label="' + dialogText(closeAria) + '">×</button>' +
          '</div>' +
          (body ? '<p class="cs-portrait-clear-message">' + dialogText(body) + '</p>' : '') +
          '<div class="cls-ability-modal-footer">' +
            '<button type="button" class="btn cs-btn-secondary" data-ymiat-dialog-dismiss>' + dialogText(cancelLabel) + '</button>' +
            (notice ? '' : '<button type="button" class="btn' + (opts.danger === false ? '' : ' cs-btn-danger') + '" data-ymiat-dialog-confirm>' + dialogText(opts.confirmLabel) + '</button>') +
          '</div>' +
        '</div>';

      function finish(ok){
        if(settled) return;
        settled = true;
        document.removeEventListener('keydown', onKey, true);
        if(overlay.parentNode) overlay.parentNode.removeChild(overlay);
        resolve(!!ok);
      }

      function onKey(e){
        if(e.key !== 'Escape') return;
        e.preventDefault();
        e.stopPropagation();
        finish(false);
      }

      overlay.addEventListener('click', function(e){
        if(e.target === overlay || e.target.closest('[data-ymiat-dialog-dismiss]')) finish(false);
        else if(e.target.closest('[data-ymiat-dialog-confirm]')) finish(true);
      });
      document.body.appendChild(overlay);
      document.addEventListener('keydown', onKey, true);
      var focusEl = overlay.querySelector('[data-ymiat-dialog-dismiss]');
      if(focusEl) focusEl.focus();
    });
  };
})();