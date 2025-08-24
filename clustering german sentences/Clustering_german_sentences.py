import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

def load_file():
    return pd.read_csv("clustering german sentences/data/data_words.csv")

def get_sample():
    df=load_file()
    return df["GERMAN"]

def process_sentences(sample):
    #words = [word.lower() for word in str(sentences).split()]
    return [sentence.lower() for sentence in sample]

def get_features(sentences):
    vocab = sorted(set(" ".join(sentences).split()))
    
    features = np.zeros((len(sentences), len(vocab)), dtype=int)
    
    for i, sentence in enumerate(sentences):
        words = sentence.split()
        for word in words:
            if word in vocab:
                j = vocab.index(word)
                features[i, j] += 1
    
    return features, vocab

def model():
    X,y=get_features(process_sentences(get_sample()))

    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans.fit(X)

    labels = kmeans.labels_

    df = pd.DataFrame({"sentence": get_sample(), "cluster": labels})
    
    return X, df, labels, kmeans, y

def pca_reduce_2d(X, df, n_components=2):
    pca = PCA(n_components=n_components, random_state=42)
    pca_result = pca.fit_transform(X)
    df["PC1"] = pca_result[:,0]
    df["PC2"] = pca_result[:,1]
    explained = pca.explained_variance_ratio_
    return df, explained

def plot_pca(df):
    plt.figure(figsize=(12,8))
    sns.scatterplot(
        data=df,
        x="PC1",
        y="PC2",
        hue="cluster",
        palette="viridis",
        legend=True
    )
    plt.title(f"PCA visualization")
    plt.show()

#get word frequencies for a single cluster
def get_freq_cluster(X, labels, id):
    #array which holds word frequencies for this cluster
    #X.shape[1] is the number of words in the vocabulary
    freq = np.zeros(X.shape[1], dtype=int)
    #loop through each sentence
    for i in range(X.shape[0]):
        if labels[i] == id:
            freq += X[i]
    return freq

def show_words(X, kmeans, vocab, n_words=20):
    n = kmeans.n_clusters
    cluster_words=[]
    for id in range(n):
        freq = get_freq_cluster(X, kmeans.labels_, id)
        #sort indices by frequency, in descending order, and keep the top n
        top_indices = np.argsort(freq)[::-1][:n_words]
        top_words = [vocab[i] for i in top_indices if freq[i] > 0]
        cluster_words.append(top_words)
    return pd.DataFrame({f"Cluster {i}": pd.Series(words) for i, words in enumerate(cluster_words)})

def main():
    X, df, labels, kmeans, y = model()

    score = silhouette_score(X, labels)
    print("score:", score)

    df,e=pca_reduce_2d(X,df)
    print("PC1", e[0]*100)
    print("PC2", e[1]*100)

    plot_pca(df)
    frequent_words_by_cluster = show_words(X,kmeans,y,50)
    print(frequent_words_by_cluster)

if __name__ == '__main__':
    main()