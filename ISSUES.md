# Issues & TODO

## Spell Categorization Issues

### Issue: Summoning/Conjuration Spells Incorrectly Categorized as "Heal"

**Problem:**
Spells that summon or conjure creatures (e.g., "Find Steed", "Conjure Animals") are being incorrectly categorized as "heal" because their stat blocks contain HP references and creature features that mention healing.

**Examples:**
- "Find Steed" has "Life Bond" and "Healing Touch" features in the summoned creature's stat block
- These features allow the summoned creature to heal, but this is not the spell itself providing healing
- The spell should not be categorized as "heal" - the healing is a feature of the summoned creature, not the spell

**Current Status:**
- Automatic categorization still detects "heal" for summoning spells
- Manual fixes have been attempted but the issue persists
- Need to improve the categorization logic to exclude:
  1. Stat block HP references (e.g., "HP 5 + 10 per spell level")
  2. Creature features that mention healing (e.g., "Life Bond", "Healing Touch")
  3. Patterns like "the steed/creature regains hit points" in stat block contexts

**Solution Needed:**
Improve the `categorize_spell()` function to better detect summoning/conjuration contexts and exclude creature feature healing from heal detection.

**Priority:** Medium
**Status:** Open
