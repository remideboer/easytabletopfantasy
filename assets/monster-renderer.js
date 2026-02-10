/**
 * Monster Stat Block Renderer
 * Renders monster data from structured JSON using templates
 */

// Render ability scores table
function renderAbilityScores(abilities, isYMIAT) {
  if (!abilities || Object.keys(abilities).length === 0) {
    return '';
  }

  const headers = Object.keys(abilities);
  const values = Object.values(abilities);

  let html = '<figure class="wp-block-table monster-ability-scores is-style-stripes"><table><thead><tr>';

  headers.forEach(header => {
    html += `<th class="has-text-align-center" data-align="center">${escapeHtml(header)}</th>`;
  });

  html += '</tr></thead><tbody><tr>';

  values.forEach(value => {
    const sign = value >= 0 ? '+' : '';
    html += `<td class="has-text-align-center" data-align="center">${sign}${value}</td>`;
  });

  html += '</tr></tbody></table></figure>';

  return html;
}

// Render traits or actions section
function renderTraitsOrActions(items, sectionTitle) {
  if (!items || items.length === 0) {
    return '';
  }

  let html = '';

  if (sectionTitle) {
    html += `<h3 class="wp-block-heading">${escapeHtml(sectionTitle)}</h3>`;
  }

  items.forEach(item => {
    html += `<p><strong>${escapeHtml(item.name)}</strong>. ${escapeHtml(item.description)}</p>`;
  });

  return html;
}

// Render full stat block from data
function renderStatBlock(monsterData, useYMIAT) {
  const version = useYMIAT ? monsterData.ymiat : monsterData.original;
  const template = document.getElementById('monster-stat-block-template');

  if (!template) {
    console.error('Monster template not found');
    return document.createElement('div');
  }

  const clone = template.content.cloneNode(true);
  const container = document.createElement('div');
  container.appendChild(clone);

  // Set CR/Level label
  const crLevelLabel = container.querySelector('.cr-level-label');
  if (crLevelLabel) {
    if (useYMIAT) {
      crLevelLabel.textContent = `Level ${monsterData.level}`;
    } else {
      crLevelLabel.textContent = `CR ${formatCR(monsterData.cr)}`;
    }
  }

  // Set size and type
  const sizeType = container.querySelector('.size-type');
  if (sizeType) {
    sizeType.textContent = `${monsterData.size} ${monsterData.type}`;
  }

  // Set basic stats
  const ac = container.querySelector('.ac');
  if (ac) {
    ac.textContent = version.ac_notes ? `${version.ac} (${version.ac_notes})` : version.ac;
  }

  const hp = container.querySelector('.hp');
  if (hp) hp.textContent = version.hp;

  const speed = container.querySelector('.speed');
  if (speed) speed.textContent = version.speed || '—';

  const perception = container.querySelector('.perception');
  if (perception) perception.textContent = version.perception || 10;

  const stealth = container.querySelector('.stealth');
  if (stealth) stealth.textContent = version.stealth || 10;

  // Set resistances and immunities
  const resistancesBlock = container.querySelector('.resistances-block');
  if (resistancesBlock && version.resistances) {
    resistancesBlock.innerHTML = `<strong>Resistant</strong> ${escapeHtml(version.resistances)}<br/>`;
  }

  const immunitiesBlock = container.querySelector('.immunities-block');
  if (immunitiesBlock && version.immunities) {
    immunitiesBlock.innerHTML = `<strong>Immune</strong> ${escapeHtml(version.immunities)}<br/>`;
  }

  const senses = container.querySelector('.senses');
  if (senses) senses.textContent = version.senses || '—';

  const languages = container.querySelector('.languages');
  if (languages) languages.textContent = version.languages || '—';

  // Render ability scores table
  const abilityTable = container.querySelector('.ability-scores-table');
  if (abilityTable) {
    abilityTable.innerHTML = renderAbilityScores(version.abilities, useYMIAT);
  }

  // Render traits
  const traitsSection = container.querySelector('.traits-section');
  if (traitsSection) {
    traitsSection.innerHTML = renderTraitsOrActions(version.traits, null);
  }

  // Render actions
  const actionsSection = container.querySelector('.actions-section');
  if (actionsSection) {
    const actionTitle = useYMIAT ? 'Moments' : 'Actions';
    actionsSection.innerHTML = renderTraitsOrActions(version.actions, actionTitle);
  }

  // Render bonus actions
  const bonusActionsSection = container.querySelector('.bonus-actions-section');
  if (bonusActionsSection) {
    bonusActionsSection.innerHTML = renderTraitsOrActions(version.bonus_actions, 'Bonus Actions');
  }

  // Render reactions
  const reactionsSection = container.querySelector('.reactions-section');
  if (reactionsSection) {
    reactionsSection.innerHTML = renderTraitsOrActions(version.reactions, 'Reactions');
  }

  // Render legendary actions
  const legendaryActionsSection = container.querySelector('.legendary-actions-section');
  if (legendaryActionsSection) {
    const legendaryTitle = useYMIAT ? 'Legendary Moments' : 'Legendary Actions';
    legendaryActionsSection.innerHTML = renderTraitsOrActions(version.legendary_actions, legendaryTitle);
  }

  return container;
}

// Format CR for display
function formatCR(cr) {
  if (cr === 0) return '0';
  if (cr === 0.125) return '1/8';
  if (cr === 0.25) return '1/4';
  if (cr === 0.5) return '1/2';
  return cr.toString();
}

// Escape HTML
function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
