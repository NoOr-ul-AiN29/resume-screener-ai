# skills.py
# ---------------------------------------------------------------------------
# PURPOSE:
#   Contains a large predefined list of skills organized by category.
#   Both the resume text and job description text are scanned against
#   this list to extract relevant skills.
#
#   No API needed — this is pure Python. Completely free.
# ---------------------------------------------------------------------------

# Master list of all known skills (lowercase for case-insensitive matching)
SKILLS_LIST = [
    # -----------------------------------------------------------------------
    # Programming Languages
    # -----------------------------------------------------------------------
    "python", "javascript", "typescript", "java", "c++", "c#", "c",
    "ruby", "php", "swift", "kotlin", "go", "golang", "rust", "scala",
    "r", "matlab", "perl", "bash", "shell", "powershell", "dart",
    "objective-c", "lua", "haskell", "elixir", "clojure", "groovy",

    # -----------------------------------------------------------------------
    # Web Frontend
    # -----------------------------------------------------------------------
    "html", "css", "html5", "css3", "sass", "scss", "less",
    "react", "reactjs", "react.js", "angular", "angularjs", "vue",
    "vuejs", "vue.js", "nextjs", "next.js", "nuxtjs", "nuxt.js",
    "svelte", "jquery", "bootstrap", "tailwind", "tailwindcss",
    "material ui", "chakra ui", "webpack", "vite", "babel",

    # -----------------------------------------------------------------------
    # Web Backend
    # -----------------------------------------------------------------------
    "node", "nodejs", "node.js", "express", "expressjs", "express.js",
    "fastapi", "flask", "django", "spring", "spring boot", "laravel",
    "rails", "ruby on rails", "asp.net", "dotnet", ".net", "nestjs",
    "graphql", "rest", "rest api", "restful", "soap", "grpc",
    "fastify", "hapi",

    # -----------------------------------------------------------------------
    # Databases
    # -----------------------------------------------------------------------
    "sql", "mysql", "postgresql", "postgres", "sqlite", "oracle",
    "mongodb", "mongoose", "redis", "elasticsearch", "cassandra",
    "dynamodb", "firebase", "supabase", "mariadb", "mssql",
    "sql server", "nosql", "neo4j", "couchdb", "influxdb",

    # -----------------------------------------------------------------------
    # Cloud & DevOps
    # -----------------------------------------------------------------------
    "aws", "azure", "gcp", "google cloud", "heroku", "vercel",
    "netlify", "digitalocean", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "jenkins", "github actions", "gitlab ci",
    "circleci", "travis ci", "nginx", "apache", "linux", "ubuntu",
    "ci/cd", "devops", "serverless", "lambda",

    # -----------------------------------------------------------------------
    # Data Science & AI/ML
    # -----------------------------------------------------------------------
    "machine learning", "deep learning", "artificial intelligence",
    "data science", "data analysis", "data engineering",
    "natural language processing", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "jupyter", "opencv", "huggingface", "transformers",
    "reinforcement learning", "neural network", "llm",
    "large language model", "generative ai",

    # -----------------------------------------------------------------------
    # Mobile Development
    # -----------------------------------------------------------------------
    "android", "ios", "react native", "flutter", "xamarin",
    "ionic", "swift", "kotlin", "mobile development",

    # -----------------------------------------------------------------------
    # Version Control & Collaboration
    # -----------------------------------------------------------------------
    "git", "github", "gitlab", "bitbucket", "svn",
    "jira", "confluence", "trello", "notion", "slack",

    # -----------------------------------------------------------------------
    # Testing
    # -----------------------------------------------------------------------
    "unit testing", "integration testing", "pytest", "jest",
    "mocha", "chai", "selenium", "cypress", "playwright",
    "test driven development", "tdd", "bdd", "postman",

    # -----------------------------------------------------------------------
    # Security
    # -----------------------------------------------------------------------
    "cybersecurity", "penetration testing", "ethical hacking",
    "owasp", "ssl", "tls", "oauth", "jwt", "encryption",
    "network security", "firewalls",

    # -----------------------------------------------------------------------
    # Design & UX
    # -----------------------------------------------------------------------
    "figma", "adobe xd", "sketch", "photoshop", "illustrator",
    "ui/ux", "ux design", "ui design", "wireframing", "prototyping",
    "user research", "canva",

    # -----------------------------------------------------------------------
    # Project Management & Methodologies
    # -----------------------------------------------------------------------
    "agile", "scrum", "kanban", "waterfall", "product management",
    "project management", "pmp", "six sigma", "lean",

    # -----------------------------------------------------------------------
    # Soft Skills
    # -----------------------------------------------------------------------
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "adaptability",
    "creativity", "collaboration", "presentation", "mentoring",
    "analytical", "attention to detail", "multitasking",

    # -----------------------------------------------------------------------
    # Other Technical
    # -----------------------------------------------------------------------
    "microservices", "api development", "system design",
    "object oriented programming", "oop", "functional programming",
    "data structures", "algorithms", "linux administration",
    "websocket", "message queue", "rabbitmq", "kafka",
    "celery", "redis queue", "etl", "data pipeline",
    "blockchain", "web3", "solidity", "excel", "tableau", "power bi",
]


def get_skills_list() -> list[str]:
    """
    Return the full master skills list.
    All skills are stored in lowercase for case-insensitive matching.

    Returns:
        List of skill strings.
    """
    return SKILLS_LIST