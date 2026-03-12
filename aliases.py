import re

SKILL_ALIASES = {
    # JavaScript
    "js"                    : "javascript",
    "es6"                   : "javascript",
    "es2015"                : "javascript",
    "vanilla js"            : "javascript",
    "ecmascript"            : "javascript",

    # TypeScript
    "ts"                    : "typescript",

    # Python
    "py"                    : "python",

    # React
    "reactjs"               : "react",
    "react.js"              : "react",
    "react js"              : "react",

    # Node.js
    "node"                  : "node.js",
    "nodejs"                : "node.js",
    "node js"               : "node.js",
    "node"                  : "node.js",

    # Next.js
    "nextjs"                : "next.js",
    "next js"               : "next.js",

    # Vue.js
    "vuejs"                 : "vue.js",
    "vue js"                : "vue.js",

    # Angular
    "angularjs"             : "angular",

    # AWS
    "aws"                   : "amazon web services",
    "amazon aws"            : "amazon web services",

    # GCP
    "gcp"                   : "google cloud platform",
    "google cloud"          : "google cloud platform",

    # Azure
    "azure"                 : "microsoft azure",
    "ms azure"              : "microsoft azure",
    "azure cloud"           : "microsoft azure",

    # Kubernetes
    "k8s"                   : "kubernetes",
    "kube"                  : "kubernetes",

    # Docker
    "containerization"      : "docker",
    "containers"            : "docker",

    # CI/CD
    "cicd"                  : "ci/cd",
    "ci cd"                 : "ci/cd",
    "continuous integration": "ci/cd",
    "continuous deployment" : "ci/cd",
    "continuous delivery"   : "ci/cd",

    # Git
    "github"                : "git",
    "gitlab"                : "git",
    "version control"       : "git",
    "vcs"                   : "git",
    "bitbucket"             : "git",

    # Databases
    "postgres"              : "postgresql",
    "psql"                  : "postgresql",
    "mongo"                 : "mongodb",

    # SQL variants — map to sql (generic)
    "t-sql"                 : "sql",
    "pl/sql"                : "sql",
    "mysql"                 : "sql",
    "sqlite"                : "sql",

    # REST API
    "rest"                  : "rest api",
    "restful"               : "rest api",
    "restful api"           : "rest api",
    "rest apis"             : "rest api",

    # GraphQL
    "gql"                   : "graphql",

    # Linux / Shell
    "unix"                  : "linux",
    "shell scripting"       : "linux",
    "shell script"          : "linux",

    # Machine Learning
    "ml"                    : "machine learning",
    "ai/ml"                 : "machine learning",

    # Deep Learning
    "dl"                    : "deep learning",

    # NLP
    "nlp"                   : "natural language processing",

    # Computer Vision
    "cv"                    : "computer vision",

    # LLMs
    "llm"                   : "large language models",
    "llms"                  : "large language models",
    "generative ai"         : "large language models",
    "gen ai"                : "large language models",

    # Scikit-learn
    "sklearn"               : "scikit-learn",
    "scikit learn"          : "scikit-learn",

    # TensorFlow
    "tf"                    : "tensorflow",

    # OOP
    "object oriented"       : "object oriented programming",
    "oops"                  : "object oriented programming",

    # Power BI
    "powerbi"               : "power bi",

    # Spring Boot
    "spring"                : "spring boot",

    # Tailwind
    "tailwind"              : "tailwind css",

    # Agile/Scrum
    "agile methodology"     : "agile",
    "scrum methodology"     : "scrum",
    
    #test
    "py.test"   : "pytest",     
    "pyest"     : "pytest",
}


def normalize_with_aliases(text: str) -> str:
    """
    Replace alias terms in text with their canonical skill names.
    Runs BEFORE clean_text() so punctuation is still intact.
    Longer aliases are matched first to avoid partial replacements.
    """
    for alias, canonical in sorted(SKILL_ALIASES.items(), key=lambda x: -len(x[0])):
        pattern = r'\b' + re.escape(alias) + r'\b'
        text = re.sub(pattern, canonical, text, flags=re.IGNORECASE)
    return text