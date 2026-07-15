"""
Build assets/talents-data.json by scraping the talent entries on
rules/talents.html - the site's authoritative talent text - so the
character sheet's talent detail popup can show the real description
instead of just a name.

Re-run this whenever rules/talents.html's talent list changes.
"""
import json
import re
from bs4 import BeautifulSoup

ROOT = r"d:\projecten\dndlite"
SOURCE = f"{ROOT}\\rules\\talents.html"
DEST = f"{ROOT}\\assets\\talents-data.json"


def clean_text(text):
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def main():
    with open(SOURCE, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    out = []
    for item in soup.select(".lineage-item"):
        title_el = item.select_one(".lineage-title")
        content = item.select_one(".lineage-content")
        if not title_el or not content:
            continue
        name = title_el.get_text(strip=True)

        prerequisite = ""
        paragraphs = []
        for child in content.find_all(["p", "ul"], recursive=False):
            if child.name == "p":
                strong = child.find("strong")
                if strong and strong.get_text(strip=True).rstrip(":") == "Prerequisite":
                    prerequisite = clean_text(child.get_text(" ")[len(strong.get_text(strip=True)):])
                    continue
                text = clean_text(child.get_text(" "))
                if text:
                    paragraphs.append(text)
            elif child.name == "ul":
                bullets = [clean_text(li.get_text(" ")) for li in child.find_all("li", recursive=False)]
                paragraphs.append("\n".join(f"• {b}" for b in bullets if b))

        out.append({
            "id": item.get("id", ""),
            "name": name,
            "prerequisite": prerequisite,
            "description": "\n\n".join(p for p in paragraphs if p),
        })

    with open(DEST, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(out)} talents to {DEST}")


if __name__ == "__main__":
    main()
