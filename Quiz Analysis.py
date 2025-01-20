import pandas as pd

# Step 1: Load the Data (replace with actual data sources)
# Assuming the datasets are in CSV format
current_quiz_data = pd.read_csv("current_quiz_data.csv")
historical_quiz_data = pd.read_csv("historical_quiz_data.csv")

# Step 2: Data Exploration and Schema Understanding
def explore_data():
    print("Current Quiz Data Overview:")
    print(current_quiz_data.info())
    print(current_quiz_data.head())

    print("\nHistorical Quiz Data Overview:")
    print(historical_quiz_data.info())
    print(historical_quiz_data.head())

# Step 3: Analyze Patterns in Student Performance
def analyze_performance():
    # Topic-Level Analysis
    topic_accuracy = historical_quiz_data.groupby('topic')[['is_correct']].mean().rename(columns={"is_correct": "accuracy"})

    # Difficulty-Level Analysis
    difficulty_accuracy = historical_quiz_data.groupby('difficulty_level')[['is_correct']].mean().rename(columns={"is_correct": "accuracy"})

    # Current Quiz Performance
    current_performance = current_quiz_data.groupby(['topic', 'difficulty_level'])["is_correct"].mean()

    print("Topic-Level Accuracy:")
    print(topic_accuracy)

    print("\nDifficulty-Level Accuracy:")
    print(difficulty_accuracy)

    print("\nCurrent Quiz Performance:")
    print(current_performance)

    return topic_accuracy, difficulty_accuracy, current_performance

# Step 4: Generate Insights
def generate_insights(topic_accuracy, difficulty_accuracy, current_performance):
    insights = {}

    # Weak Areas
    weak_topics = topic_accuracy[topic_accuracy['accuracy'] < 0.5].index.tolist()
    weak_difficulty = difficulty_accuracy[difficulty_accuracy['accuracy'] < 0.5].index.tolist()

    # Improvement Trends
    trends = historical_quiz_data.groupby(['quiz_id', 'topic'])['is_correct'].mean().unstack()
    trends_diff = trends.diff(axis=0).mean(axis=0)

    # Performance Gaps
    performance_gaps = current_performance[current_performance < 0.5]

    insights['weak_topics'] = weak_topics
    insights['weak_difficulty'] = weak_difficulty
    insights['improvement_trends'] = trends_diff
    insights['performance_gaps'] = performance_gaps

    return insights

# Step 5: Create Recommendations
def generate_recommendations(insights):
    recommendations = []

    # Focus on weak topics
    for topic in insights['weak_topics']:
        recommendations.append(f"Focus on improving performance in the topic: {topic}.")

    # Address weak difficulty levels
    for difficulty in insights['weak_difficulty']:
        recommendations.append(f"Practice questions at {difficulty} level to build confidence.")

    # Time management tips if applicable
    recommendations.append("Review time spent per question and allocate more time for harder topics.")

    return recommendations

# Main Execution
if __name__ == "__main__":
    explore_data()

    # Analyze performance
    topic_accuracy, difficulty_accuracy, current_performance = analyze_performance()

    # Generate insights
    insights = generate_insights(topic_accuracy, difficulty_accuracy, current_performance)

    # Generate recommendations
    recommendations = generate_recommendations(insights)

    # Display insights and recommendations
    print("\nInsights:")
    for key, value in insights.items():
        print(f"{key}: {value}")

    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec}")
