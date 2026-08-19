"""
quiz.py

A short diagnostic quiz. Each question is tagged with the topic_id it tests.
If the user answers correctly, we mark that topic as "known" and remove it
(and it alone -- we don't assume prerequisite topics are known too, to stay
safe/conservative) from the generated path.

This directly maps quiz performance to graph nodes, so scoring feeds
straight into topic_graph.get_personalized_path().
"""

QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "topic_id": "python_basics",
        "question": "What does the following return? len([1, 2, 3])",
        "options": ["2", "3", "Error", "[1, 2, 3]"],
        "answer": "3",
    },
    {
        "id": "q2",
        "topic_id": "numpy_pandas",
        "question": "Which library is primarily used for tabular data manipulation in Python?",
        "options": ["Matplotlib", "Pandas", "Flask", "Requests"],
        "answer": "Pandas",
    },
    {
        "id": "q3",
        "topic_id": "statistics_basics",
        "question": "What does 'standard deviation' measure?",
        "options": [
            "The average value",
            "The spread of data around the mean",
            "The most frequent value",
            "The total sum of values",
        ],
        "answer": "The spread of data around the mean",
    },
    {
        "id": "q4",
        "topic_id": "linear_algebra",
        "question": "In machine learning, what is a 'dot product' typically used for?",
        "options": [
            "Sorting arrays",
            "Combining weighted inputs (e.g., in a neuron)",
            "Reading files",
            "String formatting",
        ],
        "answer": "Combining weighted inputs (e.g., in a neuron)",
    },
    {
        "id": "q5",
        "topic_id": "supervised_learning",
        "question": "What distinguishes supervised learning from unsupervised learning?",
        "options": [
            "Supervised learning uses labeled data; unsupervised does not",
            "Supervised learning is always faster",
            "Unsupervised learning requires more labeled data",
            "There is no difference",
        ],
        "answer": "Supervised learning uses labeled data; unsupervised does not",
    },
    {
        "id": "q6",
        "topic_id": "model_evaluation",
        "question": "Which metric is commonly used to evaluate a classification model?",
        "options": ["R-squared", "F1 Score", "Mean Squared Error", "Silhouette Score"],
        "answer": "F1 Score",
    },
    {
        "id": "q7",
        "topic_id": "neural_networks_basics",
        "question": "What is the role of an 'activation function' in a neural network?",
        "options": [
            "It stores training data",
            "It introduces non-linearity into the model",
            "It splits data into train/test sets",
            "It compresses the dataset",
        ],
        "answer": "It introduces non-linearity into the model",
    },
    {
        "id": "q8",
        "topic_id": "model_deployment",
        "question": "What is the purpose of deploying a model behind an API?",
        "options": [
            "To make it accessible for other applications to send requests to",
            "To train it faster",
            "To visualize the data",
            "To clean the dataset",
        ],
        "answer": "To make it accessible for other applications to send requests to",
    },
]


def score_quiz(user_answers: dict) -> set:
    """
    user_answers: dict of {question_id: selected_option}
    Returns: set of topic_ids the user answered correctly (i.e. "known" topics)
    """
    known_topics = set()
    for q in QUIZ_QUESTIONS:
        selected = user_answers.get(q["id"])
        if selected == q["answer"]:
            known_topics.add(q["topic_id"])
    return known_topics
