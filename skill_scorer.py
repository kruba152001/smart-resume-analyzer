import re
import csv

# ─────────────────────────────────────────
#  CATEGORY WEIGHTS
#  Only these stay hardcoded — and that's fine.
#  These are business rules, not data.
#  "how important is each category" is a
#  design decision, not a skill definition.
# ─────────────────────────────────────────
CATEGORY_WEIGHTS = {
    "core_language" : 1.5,
    "framework"     : 1.3,
    "ai_ml"         : 1.4,
    "cloud"         : 1.3,
    "devops"        : 1.2,
    "database"      : 1.1,
    "testing"       : 1.1,
    "fundamentals"  : 1.1,
    "tool"          : 1.0,
    "soft_process"  : 0.8,
}


def load_skill_categories(path="Data/data.csv") -> dict:
    """
    Read skills.csv and return a dict of:
    { "python": "core_language", "docker": "devops", ... }

    Single source of truth — adding a skill to skills.csv
    automatically gives it a category here. No code changes needed.
    """
    skill_categories = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            skill    = row["skill"].strip().lower()
            category = row["category"].strip().lower()
            if skill and category:
                skill_categories[skill] = category
    return skill_categories


# Built once at module load — same pattern as PhraseMatcher
SKILL_CATEGORIES = load_skill_categories()


def get_category_multiplier(skill: str) -> float:
    """
    Look up category from CSV-loaded dict.
    Falls back to 'tool' weight if skill not found.
    """
    category = SKILL_CATEGORIES.get(skill.lower(), "tool")
    return CATEGORY_WEIGHTS.get(category, 1.0)


# ── Rest of functions unchanged ──────────

def compute_frequency_score(skill: str, jd_text: str) -> float:
    pattern = r'\b' + re.escape(skill) + r'\b'
    count = len(re.findall(pattern, jd_text, flags=re.IGNORECASE))
    return min(float(max(count, 1)), 5.0)


def compute_position_score(skill: str, jd_text: str) -> float:
    position = jd_text.lower().find(skill.lower())
    if position == -1:
        return 1.0
    relative_pos = position / max(len(jd_text), 1)
    if relative_pos <= 0.33:
        return 1.2
    elif relative_pos <= 0.66:
        return 1.0
    else:
        return 0.8


def compute_skill_weights(jd_text: str, job_skills: set) -> dict:
    weights = {}
    for skill in job_skills:
        freq  = compute_frequency_score(skill, jd_text)
        pos   = compute_position_score(skill, jd_text)
        cat   = get_category_multiplier(skill)
        weights[skill] = round(freq * pos * cat, 2)
    return weights


def compute_weighted_score(matched_skills: set, skill_weights: dict) -> dict:
    total_possible = sum(skill_weights.values())
    matched_weight = sum(skill_weights.get(s, 1.0) for s in matched_skills)

    weighted_pct = round((matched_weight / total_possible) * 100, 2) \
        if total_possible > 0 else 0.0

    raw_pct = round(
        (len(matched_skills) / len(skill_weights)) * 100, 2
    ) if skill_weights else 0.0

    missing_skills = set(skill_weights.keys()) - matched_skills
    top_missing = sorted(
        missing_skills,
        key=lambda s: skill_weights.get(s, 0),
        reverse=True
    )

    return {
        "weighted_pct" : weighted_pct,
        "raw_pct"      : raw_pct,
        "weights"      : skill_weights,
        "top_missing"  : top_missing,
    }

## 🔑 Key Design Lesson Here

