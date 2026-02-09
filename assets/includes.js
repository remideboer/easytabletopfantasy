// HTML Templates - Single source of truth for navigation and footer
// Edit these templates to update across all pages
// NOTE: Use {{ROOT}} placeholder which gets replaced with correct path

// Configuration: BASE_PATH for web deployment
// - For GitHub Pages (user/repo): Set to '/repo-name' (e.g., '/easytabletopfantasy')
// - For root domain deployment: Set to ''
// - For local development: Will automatically use relative paths regardless of this setting
const BASE_PATH = '/easytabletopfantasy';

const HTML_INCLUDES = {
  nav: `<nav><a href="{{ROOT}}index.html" class="logo-link"><img src="{{ROOT}}assets/You-Meet-In-A-Tavern.png" alt="You-Meet-In-A-Tavern (YMIAT)" class="nav-logo" /></a><div class="nav-dropdown"><a href="{{ROOT}}rules/core.html">Rules</a><div class="nav-dropdown-menu"><a href="{{ROOT}}rules/core.html#core-game-loop">Core Game Loop</a><a href="{{ROOT}}rules/core.html#modes-of-play">Modes of Play</a><a href="{{ROOT}}rules/core.html#dice-and-tests">Dice and Tests</a><a href="{{ROOT}}rules/core.html#ability-scores">Abilities and Properties</a><a href="{{ROOT}}rules/core.html#determining-ability-modifiers">Determining Ability Modifiers</a><a href="{{ROOT}}rules/core.html#proficiency-and-advantage">Proficiency and Advantage</a><a href="{{ROOT}}rules/core.html#skills-and-ability-checks">Skills and Ability Checks</a><a href="{{ROOT}}rules/core.html#talents">Talents</a><a href="{{ROOT}}rules/core.html#hit-points-and-scale">Hit Points and Scale</a><a href="{{ROOT}}rules/core.html#level-advancement">Level Advancement</a><a href="{{ROOT}}rules/core.html#attacks-and-defense">Attacks and Defense</a><a href="{{ROOT}}rules/core.html#weapon-attacks">Weapon Attacks</a><a href="{{ROOT}}rules/core.html#weapon-mastery">Weapon Mastery</a><a href="{{ROOT}}rules/core.html#actions-and-time-encounter-mode">Actions and Time</a><a href="{{ROOT}}rules/core.html#magic-and-spell-resources">Magic and Spell Resources</a><a href="{{ROOT}}rules/core.html#resolve">Resolve</a><a href="{{ROOT}}rules/core.html#recovery-points-and-rest">Recovery Points and Rest</a><a href="{{ROOT}}rules/core.html#spell-school-expertise">Spell School Expertise</a></div></div><div class="nav-dropdown"><a href="{{ROOT}}rules/characters.html">Characters</a><div class="nav-dropdown-menu"><a href="{{ROOT}}rules/characters.html">Character Creation</a><a href="{{ROOT}}rules/lineages.html">Lineages</a><a href="{{ROOT}}rules/backgrounds.html">Backgrounds</a><a href="{{ROOT}}rules/talents.html">Talents</a></div></div><a href="{{ROOT}}convert.html">Converter</a><a href="{{ROOT}}rules/conversion.html">Conversion Guide</a><a href="{{ROOT}}rules/combat.html">Combat</a><a href="{{ROOT}}rules/magic.html">Magic</a><a href="{{ROOT}}rules/gear.html">Gear</a><a href="{{ROOT}}rules/monsters.html">Monsters</a><a href="{{ROOT}}faq.html">FAQ</a><a href="{{ROOT}}legal.html">Legal</a></nav>`,

  footer: `<p>© <strong>You-Meet-In-A-Tavern</strong> (YMIAT).</p>
<p>This work is licensed under the <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License (CC BY 4.0)</a>.</p>
<p>Portions of this work are derived from the <em>5.1 System Reference Document (SRD 5.1)</em> and are used under the Creative Commons Attribution 4.0 International License.</p>
<p><strong>You-Meet-In-A-Tavern</strong> (YMIAT) is a fan-made D&D 5e homebrew and is not affiliated with, sponsored by, or endorsed by Wizards of the Coast, Kobold Press, Paizo, or any other publisher.</p>
<p><em>Dungeons &amp; Dragons</em> and <em>D&amp;D</em> are trademarks of Wizards of the Coast. <em>Tales of the Valiant</em> is a trademark of Kobold Press. <em>Pathfinder</em> is a trademark of Paizo Inc.</p>`
};

// Load includes into page - works with file:// protocol and web deployments
(function(){
  // Calculate the root path for navigation links
  function getRootPath(){
    const protocol = window.location.protocol;
    const path = window.location.pathname;

    // For file:// protocol (local development), use relative paths
    if(protocol === 'file:'){
      // Count directory depth by checking slashes
      const parts = path.replace(/^\//, '').split('/').filter(p => p);
      const depth = parts.length - 1; // -1 because last part is the filename

      // Return appropriate number of '../' based on depth
      if(depth === 0) return '';
      if(depth === 1) return '../';
      if(depth === 2) return '../../';
      return '../'.repeat(depth);
    }

    // For http(s):// protocol (web deployment), use absolute paths from BASE_PATH
    if(BASE_PATH){
      // Ensure BASE_PATH ends with '/' for consistency
      return BASE_PATH.endsWith('/') ? BASE_PATH : BASE_PATH + '/';
    }

    // No BASE_PATH set, use relative paths
    const parts = path.replace(/^\//, '').split('/').filter(p => p);
    const depth = parts.length - 1;

    if(depth === 0) return '';
    if(depth === 1) return '../';
    if(depth === 2) return '../../';
    return '../'.repeat(depth);
  }

  function loadIncludes(){
    const rootPath = getRootPath();

    // Load navigation with correct path
    const navPlaceholder = document.querySelector('[data-include="nav"]');
    if(navPlaceholder){
      navPlaceholder.innerHTML = HTML_INCLUDES.nav.replace(/\{\{ROOT\}\}/g, rootPath);
      updateActiveNav();
    }

    // Load footer
    const footerPlaceholder = document.querySelector('[data-include="footer"]');
    if(footerPlaceholder){
      footerPlaceholder.innerHTML = HTML_INCLUDES.footer;
    }
  }

  // Set aria-current="page" on the current page's nav link
  function updateActiveNav(){
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');

    navLinks.forEach(link => {
      const href = link.getAttribute('href');
      if(!href) return;

      // Normalize paths for comparison
      const linkPath = href.startsWith('/') ? href : '/' + href;
      const normalized = currentPath.endsWith('/') ? currentPath + 'index.html' : currentPath;

      if(linkPath === normalized || linkPath === currentPath){
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  // Load includes immediately
  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', loadIncludes);
  } else {
    loadIncludes();
  }
})();
