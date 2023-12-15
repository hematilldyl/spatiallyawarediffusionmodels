import os
import pandas as pd
import matplotlib.pyplot as plt

filepath = 'data_and_visuals_k/all_vsr_validated_data.jsonl'
dataset = pd.read_json(path_or_buf=filepath, lines=True, orient='records')


data = dataset[['image', 'image_link', 'caption', 'label', 'relation']]
true_data = dataset[dataset['label'] == 1][['image', 'image_link', 'caption', 'relation']]
false_data = dataset[dataset['label'] == 0][['image', 'image_link', 'caption', 'relation']]


# have list of labels, count label appearances in true
x = data['relation'].value_counts()
y = true_data['relation'].value_counts()
y = y[y > 50]
# print(x.index)
# print(x[y.index])

a = "deepskyblue"
c = "mediumblue"

hist = plt.figure(figsize=(12, 6))
plt.bar(y.index, x[y.index], align='center', color=a)
plt.bar(y.index, y, align='center', color=c)
plt.xticks(rotation=90)
plt.title("VSR Data")
plt.legend(['All data points', 'True cases only'])
plt.tight_layout()
plt.savefig('data_and_visuals_k/vsr_all_hist.png')
plt.show()

y = y[y > 50]
#print(sum(y))  # 4920

hist = plt.figure(figsize=(12, 6))
plt.bar(y.index, y, align='center', color=c)
plt.xticks(rotation=90)
plt.title("VSR Data (Relations > 50 samples)")
plt.legend(['True cases only'])
plt.tight_layout()
plt.savefig('data_and_visuals_k/vsr_50_hist.png')
plt.show()








