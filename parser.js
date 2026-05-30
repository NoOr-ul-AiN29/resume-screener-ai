// parser.js — port of parser.py
const { SKILLS_LIST } = require('./skills');

const PROTECTED_SKILLS = [
  "JavaScript", "TypeScript", "FastAPI", "GitHub", "GitLab",
  "MySQL", "MongoDB", "PostgreSQL", "MariaDB", "SQLite", "NoSQL",
  "PyCharm", "GraphQL", "TailwindCSS", "NumPy", "SciPy",
  "TensorFlow", "PyTorch", "HuggingFace", "IntelliJ",
  "VSCode", "VS Code",
  "Next.js", "Node.js", "React.js", "Vue.js", "Nuxt.js",
  "Express.js", "Angular.js",
];

function normalizeText(text) {
  // Step 1: protect compound skill names with placeholders
  const placeholders = {};
  PROTECTED_SKILLS.forEach((term, i) => {
    const ph = `ZZP${i}ZZ`;
    const regex = new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    if (regex.test(text)) {
      placeholders[ph] = term.toLowerCase();
      text = text.replace(new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), ph);
    }
  });

  // Step 2: camelCase split
  text = text.replace(/([a-z]{2,})([A-Z])/g, '$1 $2');

  // Step 3: lowercase
  text = text.toLowerCase();

  // Step 4: restore placeholders
  for (const [ph, val] of Object.entries(placeholders)) {
    text = text.split(ph.toLowerCase()).join(val);
  }

  // Step 5: normalize whitespace
  text = text.replace(/[\r\n\t]+/g, ' ').replace(/ {2,}/g, ' ').trim();

  return text;
}

function buildSkillPattern(skill) {
  const escaped = skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(?:(?:^)|(?<=[^a-zA-Z0-9]))${escaped}(?=[^a-zA-Z0-9]|$)`, 'i');
}

function extractSkillsFromText(text) {
  if (!text || !text.trim()) return [];

  const normalized = normalizeText(text);
  const skillsSorted = [...SKILLS_LIST].sort((a, b) => b.length - a.length);
  const found = new Set();

  for (const skill of skillsSorted) {
    try {
      const pattern = buildSkillPattern(skill);
      if (pattern.test(normalized)) {
        found.add(skill);
      }
    } catch (e) {
      // skip bad patterns
    }
  }

  return [...found].sort();
}

function extractSkillsFromJobDescription(jobDescription) {
  if (!jobDescription || !jobDescription.trim()) {
    throw new Error('Job description cannot be empty.');
  }
  return extractSkillsFromText(jobDescription);
}

module.exports = { extractSkillsFromText, extractSkillsFromJobDescription };