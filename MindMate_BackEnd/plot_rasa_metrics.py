import json
import matplotlib.pyplot as plt
import numpy as np

# Load Rasa test report
with open('intent_report.json', 'r') as f:
    report = json.load(f)

# Extract metrics
intent_report = report['report']['intent_report']
metrics = intent_report
overall_precision = metrics['precision']
overall_recall = metrics['recall'] 
overall_f1 = metrics['f1-score']

# Create chart
labels = ['Precision', 'Recall', 'F1-Score']
values = [overall_precision, overall_recall, overall_f1]
colors = ['#2E86AB', '#A23B72', '#F18F01']

plt.figure(figsize=(10, 6))
bars = plt.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
plt.title('Rasa NLU Model Performance\n(Precision, Recall, F1-Score)', fontsize=16, fontweight='bold')
plt.ylabel('Score', fontsize=12)
plt.ylim(0, 1)
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, value in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{value:.3f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('rasa_performance_metrics.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"✅ Metrics Chart saved as 'rasa_performance_metrics.png'")
print(f"📊 Precision: {overall_precision:.3f}")
print(f"📊 Recall:   {overall_recall:.3f}")
print(f"📊 F1-Score: {overall_f1:.3f}")