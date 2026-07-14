// HTML Templates - Single source of truth for navigation and footer
// Edit these templates to update across all pages
// NOTE: Use {{ROOT}} placeholder which gets replaced with correct path

// Configuration: BASE_PATH for web deployment
// - For GitHub Pages (user/repo): Set to '/repo-name' (e.g., '/easytabletopfantasy')
// - For root domain deployment: Set to ''
// - For local development: Will automatically use relative paths regardless of this setting
const BASE_PATH = '/easytabletopfantasy';

// BEGIN GENERATED CHARACTERS NAV
const GENERATED_CHARACTERS_NAV = `<div class="nav-dropdown"><a href="{{ROOT}}rules/characters.html">Characters</a><div class="nav-dropdown-menu nav-dropdown-menu-nested"><a href="{{ROOT}}rules/characters.html">Character Creation</a><div class="nav-submenu nav-submenu--branch"><span class="nav-submenu-label">Classes</span><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel-inner--intro"><a href="{{ROOT}}rules/classes.html">All classes</a><a href="{{ROOT}}rules/class-abilities/index.html">Class abilities index</a></div><div class="nav-submenu-panel-inner nav-submenu-panel-inner--branch-list"><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#artificer" class="nav-submenu-link">Artificer</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/artificer.html#armorer">Armorer</a><a href="{{ROOT}}rules/class-abilities/artificer.html#alchemist">Alchemist</a><a href="{{ROOT}}rules/class-abilities/artificer.html#artillerist">Artillerist</a><a href="{{ROOT}}rules/class-abilities/artificer.html#battle-smith">Battle Smith</a><a href="{{ROOT}}rules/class-abilities/artificer.html#cog-augur">Cog Augur</a><a href="{{ROOT}}rules/class-abilities/artificer.html#grenadier">Grenadier</a><a href="{{ROOT}}rules/class-abilities/artificer.html#toymaker">Toymaker</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#barbarian" class="nav-submenu-link">Barbarian</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/barbarian.html#berserker">Berserker</a><a href="{{ROOT}}rules/class-abilities/barbarian.html#wild-fury">Wild Fury</a><a href="{{ROOT}}rules/class-abilities/barbarian.html#chaos">Chaos</a><a href="{{ROOT}}rules/class-abilities/barbarian.html#four-winds">Four Winds</a><a href="{{ROOT}}rules/class-abilities/barbarian.html#kraken">Kraken</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#bard" class="nav-submenu-link">Bard</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/bard.html#lore">Lore</a><a href="{{ROOT}}rules/class-abilities/bard.html#victory">Victory</a><a href="{{ROOT}}rules/class-abilities/bard.html#allure">Allure</a><a href="{{ROOT}}rules/class-abilities/bard.html#mockery">Mockery</a><a href="{{ROOT}}rules/class-abilities/bard.html#sound">Sound</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#cleric" class="nav-submenu-link">Cleric</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/cleric.html#life">Life</a><a href="{{ROOT}}rules/class-abilities/cleric.html#light">Light</a><a href="{{ROOT}}rules/class-abilities/cleric.html#war">War</a><a href="{{ROOT}}rules/class-abilities/cleric.html#death">Death</a><a href="{{ROOT}}rules/class-abilities/cleric.html#nature">Nature</a><a href="{{ROOT}}rules/class-abilities/cleric.html#tempest">Tempest</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#druid" class="nav-submenu-link">Druid</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/druid.html#leaf">Leaf</a><a href="{{ROOT}}rules/class-abilities/druid.html#shifter">Shifter</a><a href="{{ROOT}}rules/class-abilities/druid.html#elementalist">Elementalist</a><a href="{{ROOT}}rules/class-abilities/druid.html#fey">Fey</a><a href="{{ROOT}}rules/class-abilities/druid.html#stoneheart">Stoneheart</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#fighter" class="nav-submenu-link">Fighter</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/fighter.html#spell-blade">Spell Blade</a><a href="{{ROOT}}rules/class-abilities/fighter.html#weapon-master">Weapon Master</a><a href="{{ROOT}}rules/class-abilities/fighter.html#scrapper">Scrapper</a><a href="{{ROOT}}rules/class-abilities/fighter.html#stunt-archer">Stunt Archer</a><a href="{{ROOT}}rules/class-abilities/fighter.html#twinblade">Twinblade</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#monk" class="nav-submenu-link">Monk</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/monk.html#flickering-dark">Flickering Dark</a><a href="{{ROOT}}rules/class-abilities/monk.html#open-hand">Open Hand</a><a href="{{ROOT}}rules/class-abilities/monk.html#affliction-eater">Affliction Eater</a><a href="{{ROOT}}rules/class-abilities/monk.html#elemental-voice">Elemental Voice</a><a href="{{ROOT}}rules/class-abilities/monk.html#seal-guardian">Seal Guardian</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#paladin" class="nav-submenu-link">Paladin</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/paladin.html#devotion">Devotion</a><a href="{{ROOT}}rules/class-abilities/paladin.html#justice">Justice</a><a href="{{ROOT}}rules/class-abilities/paladin.html#anathema">Anathema</a><a href="{{ROOT}}rules/class-abilities/paladin.html#safekeeping">Safekeeping</a><a href="{{ROOT}}rules/class-abilities/paladin.html#unbound">Unbound</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#ranger" class="nav-submenu-link">Ranger</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/ranger.html#hunter">Hunter</a><a href="{{ROOT}}rules/class-abilities/ranger.html#pack-master">Pack Master</a><a href="{{ROOT}}rules/class-abilities/ranger.html#arrow-binder">Arrow Binder</a><a href="{{ROOT}}rules/class-abilities/ranger.html#shadow">Shadow</a><a href="{{ROOT}}rules/class-abilities/ranger.html#trailblazer">Trailblazer</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#rogue" class="nav-submenu-link">Rogue</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/rogue.html#enforcer">Enforcer</a><a href="{{ROOT}}rules/class-abilities/rogue.html#thief">Thief</a><a href="{{ROOT}}rules/class-abilities/rogue.html#con-arcanist">Con Arcanist</a><a href="{{ROOT}}rules/class-abilities/rogue.html#nightblade">Nightblade</a><a href="{{ROOT}}rules/class-abilities/rogue.html#trapsmith">Trapsmith</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#sorcerer" class="nav-submenu-link">Sorcerer</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/sorcerer.html#chaos">Chaos</a><a href="{{ROOT}}rules/class-abilities/sorcerer.html#draconic">Draconic</a><a href="{{ROOT}}rules/class-abilities/sorcerer.html#abominable">Abominable</a><a href="{{ROOT}}rules/class-abilities/sorcerer.html#cyclonic">Cyclonic</a><a href="{{ROOT}}rules/class-abilities/sorcerer.html#sacred">Sacred</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#theurge" class="nav-submenu-link">Theurge</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/theurge.html#conduit">Conduit</a><a href="{{ROOT}}rules/class-abilities/theurge.html#illuminary">Illuminary</a><a href="{{ROOT}}rules/class-abilities/theurge.html#source-spinner">Source Spinner</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#vanguard" class="nav-submenu-link">Vanguard</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/vanguard.html#bulwark">Bulwark</a><a href="{{ROOT}}rules/class-abilities/vanguard.html#herald">Herald</a><a href="{{ROOT}}rules/class-abilities/vanguard.html#marshal">Marshal</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#warlock" class="nav-submenu-link">Warlock</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/warlock.html#archfey">Archfey</a><a href="{{ROOT}}rules/class-abilities/warlock.html#fiend">Fiend</a><a href="{{ROOT}}rules/class-abilities/warlock.html#great-old-one">Great Old One</a><a href="{{ROOT}}rules/class-abilities/warlock.html#archon">Archon</a><a href="{{ROOT}}rules/class-abilities/warlock.html#elemental-regent">Elemental Regent</a><a href="{{ROOT}}rules/class-abilities/warlock.html#fey-noble">Fey Noble</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#witch" class="nav-submenu-link">Witch</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/witch.html#crimson-cord">Crimson Cord</a><a href="{{ROOT}}rules/class-abilities/witch.html#night-song">Night Song</a><a href="{{ROOT}}rules/class-abilities/witch.html#twilight-soul">Twilight Soul</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/classes.html#wizard" class="nav-submenu-link">Wizard</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner"><a href="{{ROOT}}rules/class-abilities/wizard.html#battle-mage">Battle Mage</a><a href="{{ROOT}}rules/class-abilities/wizard.html#cantrip-adept">Cantrip Adept</a><a href="{{ROOT}}rules/class-abilities/wizard.html#arcanist">Arcanist</a><a href="{{ROOT}}rules/class-abilities/wizard.html#necromancer">Necromancer</a><a href="{{ROOT}}rules/class-abilities/wizard.html#summoner">Summoner</a></div></div></div></div></div></div><div class="nav-submenu nav-submenu--branch"><span class="nav-submenu-label">Lineages</span><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel--columns nav-submenu-panel-inner--scroll"><a href="{{ROOT}}rules/lineages.html">All lineages</a><a href="{{ROOT}}rules/lineages.html#beastkin">Beastkin</a><a href="{{ROOT}}rules/lineages.html#dhampir">Dhampir</a><a href="{{ROOT}}rules/lineages.html#dragonborn">Dragonborn</a><a href="{{ROOT}}rules/lineages.html#drow">Drow</a><a href="{{ROOT}}rules/lineages.html#duergar">Duergar</a><a href="{{ROOT}}rules/lineages.html#dwarf">Dwarf</a><a href="{{ROOT}}rules/lineages.html#elemental-scion">Elemental Scion</a><a href="{{ROOT}}rules/lineages.html#elf">Elf</a><a href="{{ROOT}}rules/lineages.html#gearforged">Gearforged</a><a href="{{ROOT}}rules/lineages.html#goblin">Goblin</a><a href="{{ROOT}}rules/lineages.html#gnoll">Gnoll</a><a href="{{ROOT}}rules/lineages.html#human">Human</a><a href="{{ROOT}}rules/lineages.html#kobold">Kobold</a><a href="{{ROOT}}rules/lineages.html#orc">Orc</a><a href="{{ROOT}}rules/lineages.html#rachisan">Rachisan</a><a href="{{ROOT}}rules/lineages.html#sapopova">Sapopova</a><a href="{{ROOT}}rules/lineages.html#sea-elf">Sea Elf</a><a href="{{ROOT}}rules/lineages.html#shade">Shade</a><a href="{{ROOT}}rules/lineages.html#smallfolk">Smallfolk</a><a href="{{ROOT}}rules/lineages.html#syderean">Syderean</a><a href="{{ROOT}}rules/lineages.html#tiefling">Tiefling</a><a href="{{ROOT}}rules/lineages.html#tosculi">Tosculi</a><a href="{{ROOT}}rules/lineages.html#eonic-human">Eonic Human</a></div></div></div><div class="nav-submenu nav-submenu--branch"><span class="nav-submenu-label">Heritages</span><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel--columns nav-submenu-panel-inner--scroll"><a href="{{ROOT}}rules/heritages.html">All heritages</a><a href="{{ROOT}}rules/heritages.html#anointed">Anointed</a><a href="{{ROOT}}rules/heritages.html#cloud">Cloud</a><a href="{{ROOT}}rules/heritages.html#cosmopolitan">Cosmopolitan</a><a href="{{ROOT}}rules/heritages.html#cottage">Cottage</a><a href="{{ROOT}}rules/heritages.html#diaspora">Diaspora</a><a href="{{ROOT}}rules/heritages.html#fireforge">Fireforge</a><a href="{{ROOT}}rules/heritages.html#grove">Grove</a><a href="{{ROOT}}rules/heritages.html#nomadic">Nomadic</a><a href="{{ROOT}}rules/heritages.html#salvager">Salvager</a><a href="{{ROOT}}rules/heritages.html#slayer">Slayer</a><a href="{{ROOT}}rules/heritages.html#stone">Stone</a><a href="{{ROOT}}rules/heritages.html#supplicant">Supplicant</a><a href="{{ROOT}}rules/heritages.html#vexed">Vexed</a><a href="{{ROOT}}rules/heritages.html#wildlands">Wildlands</a><a href="{{ROOT}}rules/heritages.html#conflicted">Conflicted</a><a href="{{ROOT}}rules/heritages.html#coterminous">Coterminous</a><a href="{{ROOT}}rules/heritages.html#covenant">Covenant</a><a href="{{ROOT}}rules/heritages.html#feysworn">Feysworn</a><a href="{{ROOT}}rules/heritages.html#hivebound">Hivebound</a><a href="{{ROOT}}rules/heritages.html#ironwrought">Ironwrought</a><a href="{{ROOT}}rules/heritages.html#islander">Islander</a><a href="{{ROOT}}rules/heritages.html#joymonger">Joymonger</a><a href="{{ROOT}}rules/heritages.html#kithren">Kithren</a><a href="{{ROOT}}rules/heritages.html#seafarer">Seafarer</a><a href="{{ROOT}}rules/heritages.html#waterside">Waterside</a></div></div></div><div class="nav-submenu nav-submenu--branch"><span class="nav-submenu-label">Backgrounds</span><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel--columns nav-submenu-panel-inner--scroll"><a href="{{ROOT}}rules/backgrounds.html">All backgrounds</a><a href="{{ROOT}}rules/backgrounds.html#adherent">Adherent</a><a href="{{ROOT}}rules/backgrounds.html#alchemist">Alchemist</a><a href="{{ROOT}}rules/backgrounds.html#artist">Artist</a><a href="{{ROOT}}rules/backgrounds.html#chronicler">Chronicler</a><a href="{{ROOT}}rules/backgrounds.html#courtier">Courtier</a><a href="{{ROOT}}rules/backgrounds.html#criminal">Criminal</a><a href="{{ROOT}}rules/backgrounds.html#gravedigger">Gravedigger</a><a href="{{ROOT}}rules/backgrounds.html#healer">Healer</a><a href="{{ROOT}}rules/backgrounds.html#homesteader">Homesteader</a><a href="{{ROOT}}rules/backgrounds.html#investigator">Investigator</a><a href="{{ROOT}}rules/backgrounds.html#maker">Maker</a><a href="{{ROOT}}rules/backgrounds.html#outcast">Outcast</a><a href="{{ROOT}}rules/backgrounds.html#rebel">Rebel</a><a href="{{ROOT}}rules/backgrounds.html#rustic">Rustic</a><a href="{{ROOT}}rules/backgrounds.html#scholar">Scholar</a><a href="{{ROOT}}rules/backgrounds.html#servant">Servant</a><a href="{{ROOT}}rules/backgrounds.html#smuggler">Smuggler</a><a href="{{ROOT}}rules/backgrounds.html#soldier">Soldier</a></div></div></div><div class="nav-submenu nav-submenu--branch"><span class="nav-submenu-label">Talents</span><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel-inner--intro"><a href="{{ROOT}}rules/talents.html">All talents</a></div><div class="nav-submenu-panel-inner nav-submenu-panel-inner--branch-list"><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/talents.html#magic-talents" class="nav-submenu-link">Magic</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel--columns nav-submenu-panel-inner--scroll"><a href="{{ROOT}}rules/talents.html#arcanist">Arcanist</a><a href="{{ROOT}}rules/talents.html#combat-casting">Combat Casting</a><a href="{{ROOT}}rules/talents.html#elemental-savant">Elemental Savant</a><a href="{{ROOT}}rules/talents.html#mental-fortitude">Mental Fortitude</a><a href="{{ROOT}}rules/talents.html#ritualist">Ritualist</a><a href="{{ROOT}}rules/talents.html#school-specialization">School Specialization</a><a href="{{ROOT}}rules/talents.html#spell-duelist">Spell Duelist</a><a href="{{ROOT}}rules/talents.html#chaos-caster">Chaos Caster</a><a href="{{ROOT}}rules/talents.html#spell-recall">Spell Recall</a><a href="{{ROOT}}rules/talents.html#magical-trickster">Magical Trickster</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/talents.html#martial-talents" class="nav-submenu-link">Martial</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel--columns nav-submenu-panel-inner--scroll"><a href="{{ROOT}}rules/talents.html#armor-expert">Armor Expert</a><a href="{{ROOT}}rules/talents.html#armor-training">Armor Training</a><a href="{{ROOT}}rules/talents.html#athletic">Athletic</a><a href="{{ROOT}}rules/talents.html#artillerist">Artillerist</a><a href="{{ROOT}}rules/talents.html#brave">Brave</a><a href="{{ROOT}}rules/talents.html#combat-conditioning">Combat Conditioning</a><a href="{{ROOT}}rules/talents.html#critical-training">Critical Training</a><a href="{{ROOT}}rules/talents.html#hand-to-hand">Hand to Hand</a><a href="{{ROOT}}rules/talents.html#opportunist">Opportunist</a><a href="{{ROOT}}rules/talents.html#physical-fortitude">Physical Fortitude</a><a href="{{ROOT}}rules/talents.html#return-fire">Return Fire</a><a href="{{ROOT}}rules/talents.html#spell-hunter">Spell Hunter</a><a href="{{ROOT}}rules/talents.html#vanguard">Vanguard</a><a href="{{ROOT}}rules/talents.html#weapon-discipline">Weapon Discipline</a></div></div></div><div class="nav-submenu nav-submenu--branch"><a href="{{ROOT}}rules/talents.html#utility-talents" class="nav-submenu-link">Utility</a><div class="nav-submenu-panel"><div class="nav-submenu-panel-inner nav-submenu-panel--columns nav-submenu-panel-inner--scroll"><a href="{{ROOT}}rules/talents.html#alchemy-adept">Alchemy Adept</a><a href="{{ROOT}}rules/talents.html#aware">Aware</a><a href="{{ROOT}}rules/talents.html#bottomless-luck">Bottomless Luck</a><a href="{{ROOT}}rules/talents.html#comrade">Comrade</a><a href="{{ROOT}}rules/talents.html#covert">Covert</a><a href="{{ROOT}}rules/talents.html#dungeoneer">Dungeoneer</a><a href="{{ROOT}}rules/talents.html#empathetic">Empathetic</a><a href="{{ROOT}}rules/talents.html#escamotage">Escamotage</a><a href="{{ROOT}}rules/talents.html#far-traveler">Far Traveler</a><a href="{{ROOT}}rules/talents.html#field-medic">Field Medic</a><a href="{{ROOT}}rules/talents.html#hardy">Hardy</a><a href="{{ROOT}}rules/talents.html#learned-researcher">Learned Researcher</a><a href="{{ROOT}}rules/talents.html#polyglot">Polyglot</a><a href="{{ROOT}}rules/talents.html#quick">Quick</a><a href="{{ROOT}}rules/talents.html#scrutinous">Scrutinous</a><a href="{{ROOT}}rules/talents.html#situational-awareness">Situational Awareness</a><a href="{{ROOT}}rules/talents.html#sleuth">Sleuth</a><a href="{{ROOT}}rules/talents.html#slippery">Slippery</a><a href="{{ROOT}}rules/talents.html#tag-team">Tag Team</a><a href="{{ROOT}}rules/talents.html#touch-of-luck">Touch of Luck</a><a href="{{ROOT}}rules/talents.html#trade-skills">Trade Skills</a><a href="{{ROOT}}rules/talents.html#trailblazer">Trailblazer</a></div></div></div></div></div></div></div></div>`;
// END GENERATED CHARACTERS NAV

const HTML_INCLUDES = {
  nav: `<nav><a href="{{ROOT}}index.html" class="logo-link"><img src="{{ROOT}}assets/You-Meet-In-A-Tavern.png" alt="You-Meet-In-A-Tavern (YMIAT)" class="nav-logo" /></a><div class="nav-dropdown"><a href="{{ROOT}}rules/core.html">Rules</a><div class="nav-dropdown-menu nav-dropdown-menu-wide"><a href="{{ROOT}}rules/core.html#core-game-loop">Core Game Loop</a><a href="{{ROOT}}rules/core.html#modes-of-play">Modes of Play</a><a href="{{ROOT}}rules/core.html#dice-and-tests">Dice and Tests</a><a href="{{ROOT}}rules/core.html#ability-scores">Abilities and Properties</a><a href="{{ROOT}}rules/core.html#determining-ability-modifiers">Determining Ability Modifiers</a><a href="{{ROOT}}rules/core.html#proficiency-and-advantage">Proficiency and Advantage</a><a href="{{ROOT}}rules/core.html#skills-and-ability-checks">Skills and Ability Checks</a><a href="{{ROOT}}rules/core.html#talents">Talents</a><a href="{{ROOT}}rules/core.html#wounds-and-scale">Wounds and Scale</a><a href="{{ROOT}}rules/core.html#level-advancement">Level Advancement</a><a href="{{ROOT}}rules/core.html#attacks-and-defense">Attacks and Defense</a><a href="{{ROOT}}rules/core.html#weapon-attacks">Weapon Attacks</a><a href="{{ROOT}}rules/core.html#weapon-mastery">Weapon Mastery</a><a href="{{ROOT}}rules/core.html#actions-and-time-encounter-mode">Actions and Time</a><a href="{{ROOT}}rules/core.html#magic-and-spell-resources">Magic and Spell Resources</a><a href="{{ROOT}}rules/core.html#resolve">Resolve</a><a href="{{ROOT}}rules/core.html#recovery-points-and-rest">Recovery Points and Rest</a><a href="{{ROOT}}rules/core.html#spell-school-expertise">Spell School Expertise</a></div></div>` + GENERATED_CHARACTERS_NAV + `<a href="{{ROOT}}character-creator.html">Character Creator</a><a href="{{ROOT}}convert.html">Converter</a><a href="{{ROOT}}rules/conversion.html">Conversion Guide</a><a href="{{ROOT}}rules/combat.html">Combat</a><a href="{{ROOT}}rules/magic.html">Magic</a><a href="{{ROOT}}rules/gear.html">Gear</a><a href="{{ROOT}}rules/monsters.html">Monsters</a><a href="{{ROOT}}faq.html">FAQ</a><a href="{{ROOT}}legal.html">Legal</a></nav>`,

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
    const hostname = window.location.hostname;
    const path = window.location.pathname;

    // For file:// protocol or localhost (local development), use relative paths
    const isLocal = protocol === 'file:' || hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '';

    if(isLocal){
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

    // No BASE_PATH set, use relative paths as fallback
    const parts = path.replace(/^\//, '').split('/').filter(p => p);
    const depth = parts.length - 1;

    if(depth === 0) return '';
    if(depth === 1) return '../';
    if(depth === 2) return '../../';
    return '../'.repeat(depth);
  }

  function needsTouchNav(){
    return window.matchMedia('(hover: none), (pointer: coarse)').matches;
  }

  function ensureNavBackdrop(){
    let backdrop = document.querySelector('.nav-dropdown-backdrop');
    if(!backdrop){
      backdrop = document.createElement('div');
      backdrop.className = 'nav-dropdown-backdrop';
      backdrop.hidden = true;
      backdrop.addEventListener('click', closeAllNavDropdowns);
      document.body.appendChild(backdrop);
    }
    return backdrop;
  }

  function closeAllNavDropdowns(){
    document.querySelectorAll('.nav-dropdown.is-open').forEach(dropdown => {
      dropdown.classList.remove('is-open');
      const trigger = dropdown.querySelector(':scope > a');
      if(trigger) trigger.setAttribute('aria-expanded', 'false');
    });
    document.querySelectorAll('.nav-submenu--branch.is-open').forEach(branch => {
      branch.classList.remove('is-open');
      clearBranchFlyoutPanel(branch);
    });
    document.body.classList.remove('nav-menu-open');
    const backdrop = document.querySelector('.nav-dropdown-backdrop');
    if(backdrop) backdrop.hidden = true;
  }

  function clearBranchFlyoutPanel(branch){
    const panel = branch.querySelector(':scope > .nav-submenu-panel');
    if(!panel) return;
    panel.classList.remove('is-placed');
    panel.style.position = '';
    panel.style.marginLeft = '';
    panel.style.left = '';
    panel.style.top = '';
    panel.style.zIndex = '';
  }

  function initNavDropdowns(){
    const backdrop = ensureNavBackdrop();

    document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
      const trigger = dropdown.querySelector(':scope > a');
      const menu = dropdown.querySelector(':scope > .nav-dropdown-menu');
      if(!trigger || !menu) return;

      trigger.setAttribute('aria-haspopup', 'true');
      trigger.setAttribute('aria-expanded', 'false');

      trigger.addEventListener('click', e => {
        if(!needsTouchNav()) return;

        const isOpen = dropdown.classList.contains('is-open');
        closeAllNavDropdowns();

        if(!isOpen){
          e.preventDefault();
          dropdown.classList.add('is-open');
          trigger.setAttribute('aria-expanded', 'true');
          document.body.classList.add('nav-menu-open');
          backdrop.hidden = false;
          requestAnimationFrame(() => {
            const first = menu.querySelector('a, [tabindex="0"]');
            if(first) first.focus({preventScroll: true});
          });
        }
      });

      menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
          if(needsTouchNav()) closeAllNavDropdowns();
        });
      });
    });

    document.addEventListener('keydown', e => {
      if(e.key === 'Escape') closeAllNavDropdowns();
    });
  }

  function initSubmenuTouchToggle(placeBranchFlyout){
    document.querySelectorAll('.nav-submenu--branch').forEach(branch => {
      const trigger = branch.querySelector(':scope > .nav-submenu-label, :scope > .nav-submenu-link');
      const panel = branch.querySelector(':scope > .nav-submenu-panel');
      if(!trigger || !panel) return;

      if(trigger.classList.contains('nav-submenu-label')){
        trigger.setAttribute('tabindex', '0');
        trigger.setAttribute('role', 'button');
        trigger.setAttribute('aria-haspopup', 'true');
        trigger.setAttribute('aria-expanded', 'false');
      }

      const inScrollList = Boolean(branch.closest('.nav-submenu-panel-inner--branch-list'));

      function setBranchOpen(open){
        branch.classList.toggle('is-open', open);
        if(trigger.getAttribute('role') === 'button'){
          trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
        }
        if(open && inScrollList){
          placeBranchFlyout(branch);
        } else if(!open){
          clearBranchFlyoutPanel(branch);
        }
      }

      function toggleBranch(e){
        if(!needsTouchNav()) return;

        const hasFlyout = Boolean(panel.querySelector('a'));
        if(!hasFlyout) return;

        e.preventDefault();
        e.stopPropagation();

        const isOpen = branch.classList.contains('is-open');
        branch.parentElement.querySelectorAll(':scope > .nav-submenu--branch.is-open').forEach(sibling => {
          if(sibling !== branch){
            sibling.classList.remove('is-open');
            const sTrigger = sibling.querySelector(':scope > .nav-submenu-label, :scope > .nav-submenu-link');
            if(sTrigger && sTrigger.getAttribute('role') === 'button'){
              sTrigger.setAttribute('aria-expanded', 'false');
            }
            clearBranchFlyoutPanel(sibling);
          }
        });
        setBranchOpen(!isOpen);
      }

      trigger.addEventListener('click', toggleBranch);
      if(trigger.classList.contains('nav-submenu-label')){
        trigger.addEventListener('keydown', e => {
          if(e.key === 'Enter' || e.key === ' '){
            e.preventDefault();
            toggleBranch(e);
          }
        });
      }
    });
  }

  function initBranchListFlyouts(){
    const OVERLAP = 8;

    /** backdrop-filter / transform on header makes fixed position relative to that ancestor */
    function fixedOrigin(el){
      let node = el.parentElement;
      while(node){
        const s = getComputedStyle(node);
        if(
          s.transform !== 'none' ||
          s.filter !== 'none' ||
          (s.backdropFilter && s.backdropFilter !== 'none') ||
          s.perspective !== 'none'
        ){
          const r = node.getBoundingClientRect();
          return {left: r.left, top: r.top};
        }
        node = node.parentElement;
      }
      return {left: 0, top: 0};
    }

    function placeBranchFlyout(branch){
      const panel = branch.querySelector(':scope > .nav-submenu-panel');
      const trigger = branch.querySelector(':scope > .nav-submenu-link');
      if(!panel || !trigger) return;

      const origin = fixedOrigin(panel);
      const rect = trigger.getBoundingClientRect();

      panel.style.position = 'fixed';
      panel.style.marginLeft = '0';
      panel.style.zIndex = '130';
      panel.classList.add('is-placed');

      let left = Math.round(rect.right - origin.left - OVERLAP);
      let top = Math.round(rect.top - origin.top);
      panel.style.left = left + 'px';
      panel.style.top = top + 'px';

      const panelRect = panel.getBoundingClientRect();
      if(panelRect.right > window.innerWidth - 8){
        left = Math.round(rect.left - origin.left - panelRect.width + OVERLAP);
        panel.style.left = left + 'px';
      }
      const adjusted = panel.getBoundingClientRect();
      if(adjusted.bottom > window.innerHeight - 8){
        top = Math.max(8 - origin.top, Math.round(window.innerHeight - adjusted.height - 8 - origin.top));
        panel.style.top = top + 'px';
      }
    }

    function clearBranchFlyout(branch){
      const panel = branch.querySelector(':scope > .nav-submenu-panel');
      if(!panel || branch.matches(':hover') || branch.classList.contains('is-open')) return;
      clearBranchFlyoutPanel(branch);
    }

    document.querySelectorAll('.nav-submenu-panel-inner--branch-list').forEach(list => {
      list.querySelectorAll('.nav-submenu--branch').forEach(branch => {
        branch.addEventListener('mouseenter', () => placeBranchFlyout(branch));
        branch.addEventListener('focusin', () => placeBranchFlyout(branch));
        branch.addEventListener('mouseleave', e => {
          if(!branch.contains(e.relatedTarget)){
            requestAnimationFrame(() => clearBranchFlyout(branch));
          }
        });
        branch.addEventListener('focusout', e => {
          if(!branch.contains(e.relatedTarget)){
            requestAnimationFrame(() => clearBranchFlyout(branch));
          }
        });
      });

      list.addEventListener('scroll', () => {
        list.querySelectorAll('.nav-submenu--branch:hover, .nav-submenu--branch.is-open').forEach(placeBranchFlyout);
      });
    });

    initSubmenuTouchToggle(placeBranchFlyout);
  }

  function loadIncludes(){
    const rootPath = getRootPath();

    // Load navigation with correct path
    const navPlaceholder = document.querySelector('[data-include="nav"]');
    if(navPlaceholder){
      navPlaceholder.innerHTML = HTML_INCLUDES.nav.replace(/\{\{ROOT\}\}/g, rootPath);
      updateActiveNav();
      initBranchListFlyouts();
      initNavDropdowns();
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
