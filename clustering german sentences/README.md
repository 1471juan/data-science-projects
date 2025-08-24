# Clustering German Sentences with K-Means

The objective is to apply unsupervised learning to a dataset of German sentences and explore whether meaningful clusters can be visualized.

## Methodology
- I gather the data from my own German studying sessions, the sentences are sorted  with the older sentences presented first.
- I preprocessed said sentences into vectors. The vector counts the times a word appears in a sentence.
- I Applied K-means clustering with 5 clusters
- Then Evaluated clustering quality using the silhouette score
- Finally, I used PCA(Principal component analysis) for dimensionality reduction and visualization of the clusters.

## Results

The Silhouette score 0.026, which indicates weak clustering.

PCA explained variance: PC1 = 3.4% PC2 = 2.8%
Each principal component(PC) is a direction in the data that captures as much variance information as possible. The strongest direction in the dataset explains 3.4% (PC1), and the second strongest explains 2.8% (PC2) of the variance. This means that the first two components together capture about 6% of the overall variation in my German sentences dataset. These values are small, but we can still partially visualize the separation of clusters in 2d. PC1 and PC2 likely represent contrasts in sentence structure of frequent and infrequent vocabulary.

<u>PCA plot:</u>
<img width="1920" height="975" alt="Figure" src="https://github.com/user-attachments/assets/b749b41e-da04-4a6c-b8a3-7eb88671c33d" />

The visualization shows partial separation between clusters, but the low silhouette score (0.026) indicates weak clustering structure.

<u>Top 50 most frequent words for each cluster</u>
> Note: nan cells indicate that a cluster has fewer than 50 frequent words.
<img width="950" height="1040" alt="cluster_words_table" src="https://github.com/user-attachments/assets/b18fa86d-49dc-4dd0-8176-0b0569997ccf" />
