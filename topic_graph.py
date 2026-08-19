"""
topic_graph.py

Hand-built knowledge graph of topics required to go from zero to
"build and deploy an ML model". Each topic lists its prerequisites.

This is the core differentiator of the project: instead of asking an LLM
to guess a valid topic order (which can hallucinate incorrect prerequisite
relationships), we encode the prerequisite structure explicitly and use a
topological sort to GUARANTEE a valid learning order.
"""

from graphlib import TopologicalSorter, CycleError

# ---------------------------------------------------------------------------
# 1. THE GRAPH
# Each key is a topic_id. "title" is the human-readable name.
# "prereqs" lists topic_ids that must be learned first.
# ---------------------------------------------------------------------------

TOPIC_GRAPH = {
    "python_basics": {
        "title": "Python Basics",
        "prereqs": [],
    },
    "numpy_pandas": {
        "title": "NumPy & Pandas",
        "prereqs": ["python_basics"],
    },
    "statistics_basics": {
        "title": "Statistics Fundamentals",
        "prereqs": ["python_basics"],
    },
    "linear_algebra": {
        "title": "Linear Algebra for ML",
        "prereqs": ["python_basics"],
    },
    "probability": {
        "title": "Probability Theory",
        "prereqs": ["statistics_basics"],
    },
    "data_visualization": {
        "title": "Data Visualization",
        "prereqs": ["numpy_pandas"],
    },
    "data_cleaning": {
        "title": "Data Cleaning & Preprocessing",
        "prereqs": ["numpy_pandas"],
    },
    "supervised_learning": {
        "title": "Supervised Learning (Regression & Classification)",
        "prereqs": ["statistics_basics", "linear_algebra", "data_cleaning"],
    },
    "unsupervised_learning": {
        "title": "Unsupervised Learning (Clustering, PCA)",
        "prereqs": ["supervised_learning"],
    },
    "model_evaluation": {
        "title": "Model Evaluation & Metrics",
        "prereqs": ["supervised_learning"],
    },
    "feature_engineering": {
        "title": "Feature Engineering",
        "prereqs": ["supervised_learning", "data_visualization"],
    },
    "cross_validation": {
        "title": "Cross-Validation & Hyperparameter Tuning",
        "prereqs": ["model_evaluation"],
    },
    "ensemble_methods": {
        "title": "Ensemble Methods (Random Forest, XGBoost)",
        "prereqs": ["cross_validation", "feature_engineering"],
    },
    "neural_networks_basics": {
        "title": "Neural Network Fundamentals",
        "prereqs": ["probability", "cross_validation"],
    },
    "deep_learning_frameworks": {
        "title": "Deep Learning Frameworks (PyTorch/TensorFlow)",
        "prereqs": ["neural_networks_basics"],
    },
    "model_deployment": {
        "title": "Model Deployment (API/Streamlit/Docker)",
        "prereqs": ["ensemble_methods"],
    },
    "mlops_basics": {
        "title": "MLOps Basics (Versioning, Monitoring)",
        "prereqs": ["model_deployment"],
    },
}


# ---------------------------------------------------------------------------
# 2. TOPOLOGICAL SORT
# Produces a valid learning order that always respects prerequisites,
# regardless of dictionary insertion order.
# ---------------------------------------------------------------------------

def get_full_topological_order():
    """Returns ALL topics in a valid prerequisite-respecting order."""
    ts = TopologicalSorter()
    for topic_id, data in TOPIC_GRAPH.items():
        ts.add(topic_id, *data["prereqs"])
    try:
        return list(ts.static_order())
    except CycleError as e:
        raise ValueError(f"Cycle detected in topic graph: {e}")


def get_personalized_path(known_topics: set):
    """
    Given a set of topic_ids the learner already knows (from the quiz),
    return the ordered list of topic_ids they still need to learn.

    Also expands 'known_topics' to include any topic whose prerequisites
    are ALL already known but wasn't explicitly marked known — optional,
    currently left explicit (only removes what was directly marked known).
    """
    full_order = get_full_topological_order()
    remaining = [t for t in full_order if t not in known_topics]
    return remaining


def get_topic_title(topic_id: str) -> str:
    return TOPIC_GRAPH.get(topic_id, {}).get("title", topic_id)


def validate_graph():
    """Sanity check: every prereq referenced must exist as a topic key."""
    all_ids = set(TOPIC_GRAPH.keys())
    for topic_id, data in TOPIC_GRAPH.items():
        for p in data["prereqs"]:
            if p not in all_ids:
                raise ValueError(f"Unknown prereq '{p}' referenced by '{topic_id}'")
    # Will raise CycleError if there's a cycle
    get_full_topological_order()
    return True


if __name__ == "__main__":
    validate_graph()
    print("Graph valid. Full learning order:\n")
    for i, t in enumerate(get_full_topological_order(), 1):
        print(f"{i:2d}. {get_topic_title(t)}")
