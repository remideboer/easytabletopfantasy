(function(){
  function slug(s){
    return s.toLowerCase().trim().replace(/&/g,'and').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
  }
  
  // Prevent scroll jump: add IDs before browser tries to scroll to hash
  function initTOC(){
    const main = document.querySelector('main');
    if(!main) return;
    
    // Add IDs to headings FIRST (before any scroll happens)
    const headings = Array.from(main.querySelectorAll('h2, h3'));
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
  
  // Run as early as possible to set IDs before browser scrolls
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initTOC);
  } else {
    // DOM already ready, run immediately
    initTOC();
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