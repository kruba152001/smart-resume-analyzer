





from nlp_extractor import extract_skills_from_text


def precision(extracted:set, expected:set) -> float:
    if not extracted:
        return 0.0
    return len(extracted & expected) / len(extracted)
def recall(extracted:set, expected:set) -> float:
    if not expected:
        return 0.0
    return len(extracted & expected) / len(expected)
def f1_score(p:float, r:float) -> float:
    if p + r == 0:
        return 0.0
    return 2 * (p * r) / (p + r)
def evaluate_single(text:str,expected_skills:set) -> dict:
    extracted = extract_skills_from_text(text)
    p = precision(extracted, expected_skills)
    r = recall(extracted, expected_skills)
    f1 = f1_score(p, r)
    return {
        "precision": round(p, 4),
        "recall": round(r, 4),
        "f1_score": round(f1, 4),
        "extracted": extracted,
        "expected": expected_skills,
        "true_positives" : extracted & expected_skills,   # found AND correct
        "false_positives": extracted - expected_skills,   # found BUT wrong (noise)
        "false_negatives": expected_skills - extracted,   # existed BUT missed
    }
def evaluate_all(data: list) -> dict:
    if not data:
        return {}

    results = []
    total_precision = 0.0
    total_recall    = 0.0
    total_f1        = 0.0

    for item in data:
        result          = evaluate_single(item["text"], item["expected"])
        result["label"] = item["label"]
        results.append(result)

        total_precision += result["precision"]
        total_recall    += result["recall"]
        total_f1        += result["f1_score"]

    n = len(data)
    return {
        "results"          : results,
        "average_precision": round(total_precision / n, 4),
        "average_recall"   : round(total_recall    / n, 4),
        "average_f1_score" : round(total_f1        / n, 4),
    }
TEST_CASES = [
    {
        "label"   : "Backend Developer Resume",
        "text"    : """
            Experienced backend developer with Python and Django.
            Worked with PostgreSQL and Redis.
            Deployed using Docker and AWS.
            Familiar with Git and CI/CD pipelines.
        """,
        "expected": {
            "python", "django", "postgresql", "redis",
            "docker", "amazon web services", "git", "ci/cd"
        }
    },
    {
        "label"   : "Alias Test",
        "text"    : """
            Strong knowledge of JS and k8s.
            Experience with AWS and GCP.
            Used sklearn and tf for model building.
        """,
        "expected": {
            "javascript", "kubernetes",
            "amazon web services", "google cloud platform",
            "scikit-learn", "tensorflow"
        }
    },
    {
    "label"   : "Tricky Alias Test",
    "text"    : """
        Built REST APIs using Node and Postgres.
        Deployed on Azure cloud with Terraform.
        Used Mongo for NoSQL storage.
        Wrote unit tests with py.test
    """,
    "expected": {
        "rest api", "node.js", "postgresql",
        "microsoft azure", "terraform",
        "mongodb", "pytest"
    }
},
{
    "label"   : "Noise Test",
    "text"    : """
        Strong experience and excellent knowledge of
        working with teams. Good understanding of
        development processes and strong ability to learn.
        Some Python experience.
    """,
    "expected": {"python"}   # everything else is noise
},
]
def print_evaluation_report(report: dict):
    print("\nDetailed Results:")
    for result in report["results"]:
        print(f"\nLabel: {result['label']}")
        print(f"Extracted Skills: {result['extracted']}")
        print(f"Expected Skills : {result['expected']}")
        print(f"True Positives  : {result['true_positives']}")
        print(f"False Positives : {result['false_positives']}")
        print(f"False Negatives : {result['false_negatives']}")
        print(f"Precision       : {result['precision']}")
        print(f"Recall          : {result['recall']}")
        print(f"F1 Score        : {result['f1_score']}")

    # averages at the bottom — overall summary after details
    print("\n" + "="*40)
    print(f"Average Precision: {report['average_precision']}")
    print(f"Average Recall   : {report['average_recall']}")
    print(f"Average F1 Score : {report['average_f1_score']}")

if __name__ == "__main__":
    report = evaluate_all(TEST_CASES)
    print_evaluation_report(report)