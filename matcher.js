// matcher.js — port of matcher.py
const SKILL_ALIASES = {
  "js": "javascript", "es6": "javascript", "es2015": "javascript", "ecmascript": "javascript",
  "ts": "typescript",
  "py": "python",
  "node": "nodejs", "node.js": "nodejs",
  "react": "reactjs", "react.js": "reactjs",
  "vue": "vuejs", "vue.js": "vuejs",
  "next": "nextjs", "next.js": "nextjs",
  "postgres": "postgresql", "psql": "postgresql",
  "mongo": "mongodb",
  "express": "expressjs", "express.js": "expressjs",
  "go": "golang",
  "dotnet": ".net", "asp.net": ".net",
  "cplusplus": "c++", "csharp": "c#",
  "restful": "rest api", "rest": "rest api", "rest apis": "rest api",
  "ml": "machine learning",
  "ai": "artificial intelligence",
  "sklearn": "scikit-learn",
  "k8s": "kubernetes",
  "ci cd": "ci/cd", "cicd": "ci/cd",
  "version control": "git",
  "oop": "object oriented programming", "object-oriented": "object oriented programming",
  "nlp": "natural language processing",
  "ui ux": "ui/ux", "ux": "ux design", "ui": "ui design",
  "tdd": "test driven development",
  "dsa": "data structures",
  "llms": "llm", "large language models": "llm",
};

function normalize(skill) {
  const s = skill.trim().toLowerCase();
  return SKILL_ALIASES[s] || s;
}

function getMatchLabel(percentage) {
  if (percentage >= 80) return "Excellent Match 🌟";
  if (percentage >= 60) return "Good Match ✅";
  if (percentage >= 40) return "Partial Match ⚠️";
  if (percentage >= 20) return "Weak Match ❌";
  return "Poor Match 💔";
}

function calculateMatch(resumeSkills, jobSkills) {
  const jobNormMap = {};
  for (const s of jobSkills) {
    jobNormMap[normalize(s)] = s;
  }

  const resumeNormSet = new Set(resumeSkills.map(normalize));

  const matched = [];
  const missing = [];

  for (const [normKey, displayForm] of Object.entries(jobNormMap)) {
    if (resumeNormSet.has(normKey)) {
      matched.push(displayForm);
    } else {
      missing.push(displayForm);
    }
  }

  matched.sort();
  missing.sort();

  const totalJob = Object.keys(jobNormMap).length;
  const matchPercentage = totalJob === 0 ? 0 : Math.round((matched.length / totalJob) * 10000) / 100;

  return {
    resume_skills: [...resumeSkills].sort(),
    job_skills: [...jobSkills].sort(),
    matched_skills: matched,
    missing_skills: missing,
    match_percentage: matchPercentage,
    match_label: getMatchLabel(matchPercentage),
    total_job_skills: totalJob,
    total_matched: matched.length,
  };
}

module.exports = { calculateMatch };