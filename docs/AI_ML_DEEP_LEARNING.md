# Jakana AI, Machine Learning, and Deep Learning Ecosystem

This document provides a comprehensive guide to using Python's AI, ML, and Data Science libraries within Jakana. Jakana seamlessly transpiles to Python, allowing full access to these ecosystems.

## 1. PyTorch

### Tensor Creation & Math

**Jakana:**
```jakana
use torch

# Creation
x = torch.zeros([2, 3])
y = torch.ones([2, 3])
z = torch.randn([2, 3])
t = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

# Math
res_matmul = torch.matmul(t, t)
res_dot = torch.dot(torch.tensor([1, 2]), torch.tensor([3, 4]))
res_cross = torch.cross(torch.randn(3), torch.randn(3))
res_trans = t.transpose(0, 1)
res_reshape = t.reshape([4, 1])
```

**Python:**
```python
import torch

# Creation
x = torch.zeros([2, 3])
y = torch.ones([2, 3])
z = torch.randn([2, 3])
t = torch.tensor([[1.0, 2.0], [3.0, 4.0]])

# Math
res_matmul = torch.matmul(t, t)
res_dot = torch.dot(torch.tensor([1, 2]), torch.tensor([3, 4]))
res_cross = torch.cross(torch.randn(3), torch.randn(3))
res_trans = t.transpose(0, 1)
res_reshape = t.reshape([4, 1])
```

### Autograd & GPU

**Jakana:**
```jakana
use torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()
x.grad |> echo
```

**Python:**
```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()
z.backward()
print(x.grad)
```

### Neural Networks & Loss/Optimizers

**Jakana:**
```jakana
use torch.nn as nn
use torch.optim as optim

fn create_model() {
    return nn.Sequential(
        nn.Conv2d(1, 20, 5),
        nn.ReLU(),
        nn.Linear(20, 10),
        nn.Softmax(dim=1)
    )
}

model = create_model()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Others: nn.LSTM, nn.Transformer, optim.SGD, optim.AdamW, optim.RMSprop, nn.MSELoss, nn.BCELoss, nn.L1Loss
```

**Python:**
```python
import torch.nn as nn
import torch.optim as optim

def create_model():
    return nn.Sequential(
        nn.Conv2d(1, 20, 5),
        nn.ReLU(),
        nn.Linear(20, 10),
        nn.Softmax(dim=1)
    )

model = create_model()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Others: nn.LSTM, nn.Transformer, optim.SGD, optim.AdamW, optim.RMSprop, nn.MSELoss, nn.BCELoss, nn.L1Loss
```

### Data Loaders, Training, and Inference

**Jakana:**
```jakana
use torch
use torch.utils.data.DataLoader
use torch.utils.data.Dataset

# Assuming CustomDataset is defined
# dataloader = DataLoader(CustomDataset(), batch_size=32, shuffle=True)

fn train_step(model, optimizer, criterion, inputs, labels) {
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()
}

fn inference(model, inputs) {
    torch.no_grad()
    model.eval()
    return model(inputs)
}

# Save and load
torch.save(model.state_dict(), "model.pth")
model.load_state_dict(torch.load("model.pth"))
```

**Python:**
```python
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset

# Assuming CustomDataset is defined
# dataloader = DataLoader(CustomDataset(), batch_size=32, shuffle=True)

def train_step(model, optimizer, criterion, inputs, labels):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()

def inference(model, inputs):
    with torch.no_grad():
        model.eval()
        return model(inputs)

# Save and load
torch.save(model.state_dict(), "model.pth")
model.load_state_dict(torch.load("model.pth"))
```

## 2. TensorFlow / Keras

### Basics & Math

**Jakana:**
```jakana
use tensorflow as tf

c = tf.constant([[1.0, 2.0], [3.0, 4.0]])
v = tf.Variable([1.0, 2.0])

m = tf.matmul(c, c)
s = tf.reduce_sum(c)
r = tf.reshape(c, [4])
```

**Python:**
```python
import tensorflow as tf

c = tf.constant([[1.0, 2.0], [3.0, 4.0]])
v = tf.Variable([1.0, 2.0])

m = tf.matmul(c, c)
s = tf.reduce_sum(c)
r = tf.reshape(c, [4])
```

### Models, Training, & Data

**Jakana:**
```jakana
use tensorflow.keras as keras
use tensorflow.keras.layers as layers

# Sequential API
model = keras.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.LSTM(64),
    layers.Attention(),
    layers.Dense(10, activation="softmax")
])

# Functional API
inputs = keras.Input(shape=(32,))
outputs = layers.Dense(1)(inputs)
func_model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# callbacks = [keras.callbacks.EarlyStopping(patience=3), keras.callbacks.ModelCheckpoint("best.h5"), keras.callbacks.TensorBoard(log_dir="./logs")]
# model.fit(train_dataset, epochs=10, callbacks=callbacks)
# preds = model.predict(test_data)
# model.evaluate(test_data, test_labels)

# Dataset & TFLite
dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
```

**Python:**
```python
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

# Sequential API
model = keras.Sequential([
    layers.Dense(64, activation="relu"),
    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.LSTM(64),
    layers.Attention(),
    layers.Dense(10, activation="softmax")
])

# Functional API
inputs = keras.Input(shape=(32,))
outputs = layers.Dense(1)(inputs)
func_model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# callbacks = [keras.callbacks.EarlyStopping(patience=3), keras.callbacks.ModelCheckpoint("best.h5"), keras.callbacks.TensorBoard(log_dir="./logs")]
# model.fit(train_dataset, epochs=10, callbacks=callbacks)
# preds = model.predict(test_data)
# model.evaluate(test_data, test_labels)

# Dataset & TFLite
dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
```

## 3. Hugging Face Transformers

**Jakana:**
```jakana
use transformers.AutoModel
use transformers.AutoTokenizer
use transformers.AutoModelForCausalLM
use transformers.pipeline
use transformers.Trainer
use transformers.TrainingArguments

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

encoded = tokenizer.encode("Hello world")
decoded = tokenizer.decode(encoded)

# Pipelines
classifier = pipeline("sentiment-analysis")
res = classifier("Jakana is great!") |> echo

# Other pipelines: text-generation, translation, summarization, question-answering, zero-shot-classification, image-classification

# Fine-tuning
args = TrainingArguments(output_dir="./results", num_train_epochs=3)
# trainer = Trainer(model=model, args=args, train_dataset=dataset)
# trainer.train()

# model.push_to_hub("my-awesome-model")
```

**Python:**
```python
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
from transformers import pipeline
from transformers import Trainer
from transformers import TrainingArguments

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

encoded = tokenizer.encode("Hello world")
decoded = tokenizer.decode(encoded)

# Pipelines
classifier = pipeline("sentiment-analysis")
res = classifier("Jakana is great!")
print(res)

# Other pipelines: text-generation, translation, summarization, question-answering, zero-shot-classification, image-classification

# Fine-tuning
args = TrainingArguments(output_dir="./results", num_train_epochs=3)
# trainer = Trainer(model=model, args=args, train_dataset=dataset)
# trainer.train()

# model.push_to_hub("my-awesome-model")
```

## 4. scikit-learn

**Jakana:**
```jakana
use sklearn.linear_model.LogisticRegression
use sklearn.ensemble.RandomForestClassifier
use sklearn.cluster.KMeans
use sklearn.decomposition.PCA
use sklearn.metrics.accuracy_score
use sklearn.pipeline.make_pipeline
use sklearn.preprocessing.StandardScaler
use sklearn.model_selection.train_test_split

# Other imports: SVM, KNN, GradientBoosting, XGBoost, LinearRegression, Ridge, Lasso, ElasticNet, DBSCAN, AgglomerativeClustering, t-SNE, UMAP, f1_score, confusion_matrix, classification_report, cross_val_score, Pipeline, MinMaxScaler, LabelEncoder, OneHotEncoder

# Data prep
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Pipeline
clf = make_pipeline(StandardScaler(), RandomForestClassifier())

# clf.fit(X_train, y_train)
# preds = clf.predict(X_test)
# acc = accuracy_score(y_test, preds)

# Clustering & Dim Reduction
kmeans = KMeans(n_clusters=3)
pca = PCA(n_components=2)
```

**Python:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Other imports: SVM, KNN, GradientBoosting, XGBoost, LinearRegression, Ridge, Lasso, ElasticNet, DBSCAN, AgglomerativeClustering, t-SNE, UMAP, f1_score, confusion_matrix, classification_report, cross_val_score, Pipeline, MinMaxScaler, LabelEncoder, OneHotEncoder

# Data prep
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Pipeline
clf = make_pipeline(StandardScaler(), RandomForestClassifier())

# clf.fit(X_train, y_train)
# preds = clf.predict(X_test)
# acc = accuracy_score(y_test, preds)

# Clustering & Dim Reduction
kmeans = KMeans(n_clusters=3)
pca = PCA(n_components=2)
```

## 5. Data Libraries

**Jakana:**
```jakana
use numpy as np
use pandas as pd
use polars as pl
use scipy

# NumPy
arr = np.array([1, 2, 3])
ls = np.linspace(0, 10, 50)
ar = np.arange(10)
z = np.zeros(5)
o = np.ones(5)
r = np.random.rand(3, 3)
np.linalg.solve(np.eye(2), np.array([1, 2]))
np.linalg.eig(np.eye(2))
np.fft.fft(arr)
np.dot(arr, arr)
np.cross(arr, arr)

# Pandas
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
# pd.read_csv("data.csv")
# pd.read_excel("data.xlsx")
# df.groupby("A").mean()
# pd.merge(df1, df2)
# df.pivot_table(index="A")
# df.to_csv("out.csv")
# df.describe()
# df.fillna(0)
# df.dropna()

# Polars
# pl.read_csv("data.csv")
# df.filter(pl.col("A") > 1).select(["A", "B"]).with_columns(C=pl.col("A") * 2).group_by("A").agg(pl.sum("B"))
# lazy_df = pl.scan_csv("data.csv")

# SciPy
# scipy.optimize.minimize
# scipy.stats.norm
# scipy.integrate.quad
# scipy.interpolate, scipy.signal, scipy.spatial, scipy.sparse
```

**Python:**
```python
import numpy as np
import pandas as pd
import polars as pl
import scipy

# NumPy
arr = np.array([1, 2, 3])
ls = np.linspace(0, 10, 50)
ar = np.arange(10)
z = np.zeros(5)
o = np.ones(5)
r = np.random.rand(3, 3)
np.linalg.solve(np.eye(2), np.array([1, 2]))
np.linalg.eig(np.eye(2))
np.fft.fft(arr)
np.dot(arr, arr)
np.cross(arr, arr)

# Pandas
df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
# pd.read_csv("data.csv")
# pd.read_excel("data.xlsx")
# df.groupby("A").mean()
# pd.merge(df1, df2)
# df.pivot_table(index="A")
# df.to_csv("out.csv")
# df.describe()
# df.fillna(0)
# df.dropna()

# Polars
# pl.read_csv("data.csv")
# df.filter(pl.col("A") > 1).select(["A", "B"]).with_columns(C=pl.col("A") * 2).group_by("A").agg(pl.sum("B"))
# lazy_df = pl.scan_csv("data.csv")

# SciPy
# scipy.optimize.minimize
# scipy.stats.norm
# scipy.integrate.quad
# scipy.interpolate, scipy.signal, scipy.spatial, scipy.sparse
```

## 6. Reinforcement Learning

**Jakana:**
```jakana
use gymnasium as gym
use stable_baselines3.PPO

# Other algorithms: A2C, DQN, SAC

env = gym.make("CartPole-v1", render_mode="human")
# obs, info = env.reset()
# obs, reward, terminated, truncated, info = env.step(action)
# env.render()

# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10000)

# Custom Environment requires extending gym.Env
```

**Python:**
```python
import gymnasium as gym
from stable_baselines3 import PPO

# Other algorithms: A2C, DQN, SAC

env = gym.make("CartPole-v1", render_mode="human")
# obs, info = env.reset()
# obs, reward, terminated, truncated, info = env.step(action)
# env.render()

# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=10000)

# Custom Environment requires extending gym.Env
```

## 7. Computer Vision

**Jakana:**
```jakana
use cv2
use PIL.Image
use torchvision.transforms as transforms
use torchvision.datasets as datasets
use torchvision.models as models

# OpenCV
# img = cv2.imread("image.jpg")
# resized = cv2.resize(img, (224, 224))
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (5, 5), 0)
# edges = cv2.Canny(blur, 100, 200)
# contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cap = cv2.VideoCapture(0)

# Pillow
# img = Image.open("image.jpg")
# img.resize((200, 200))
# img.rotate(90)
# img.filter(ImageFilter.BLUR)
# img.save("out.jpg")

# Torchvision
resnet = models.resnet18(pretrained=True)
# models: VGG, EfficientNet
transform = transforms.Compose([transforms.ToTensor()])
```

**Python:**
```python
import cv2
from PIL import Image
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models

# OpenCV
# img = cv2.imread("image.jpg")
# resized = cv2.resize(img, (224, 224))
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (5, 5), 0)
# edges = cv2.Canny(blur, 100, 200)
# contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cap = cv2.VideoCapture(0)

# Pillow
# img = Image.open("image.jpg")
# img.resize((200, 200))
# img.rotate(90)
# img.filter(ImageFilter.BLUR)
# img.save("out.jpg")

# Torchvision
resnet = models.resnet18(pretrained=True)
# models: VGG, EfficientNet
transform = transforms.Compose([transforms.ToTensor()])
```

## 8. NLP

**Jakana:**
```jakana
use spacy
use nltk
use gensim.models.Word2Vec
use gensim.models.Doc2Vec
use gensim.models.TfidfModel

# spaCy
# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Jakana makes NLP easy.")
# doc.ents |> echo
# doc.sents |> echo
# [token.pos_ for token in doc] |> echo
# [token.dep_ for token in doc] |> echo

# NLTK
# nltk.word_tokenize("Hello world")
# nltk.sent_tokenize("Hello. World.")
# nltk.pos_tag(["Hello", "world"])
# nltk.corpus.stopwords.words("english")
# nltk.corpus.wordnet
```

**Python:**
```python
import spacy
import nltk
from gensim.models import Word2Vec
from gensim.models import Doc2Vec
from gensim.models import TfidfModel

# spaCy
# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Jakana makes NLP easy.")
# print(doc.ents)
# print(doc.sents)
# print([token.pos_ for token in doc])
# print([token.dep_ for token in doc])

# NLTK
# nltk.word_tokenize("Hello world")
# nltk.sent_tokenize("Hello. World.")
# nltk.pos_tag(["Hello", "world"])
# nltk.corpus.stopwords.words("english")
# nltk.corpus.wordnet
```

## 9. Generative AI

**Jakana:**
```jakana
use diffusers.StableDiffusionPipeline
use langchain.chains.LLMChain
use langchain.prompts.PromptTemplate
use langchain.agents
use openai

# Diffusers
# pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
# image = pipe("a photo of an astronaut riding a horse on mars").images[0]

# LangChain
# prompt = PromptTemplate(input_variables=["product"], template="What is a good name for a company that makes {product}?")
# chain = LLMChain(llm=llm, prompt=prompt)

# OpenAI API Pattern
# openai.api_key = "..."
# response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
```

**Python:**
```python
from diffusers import StableDiffusionPipeline
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain import agents
import openai

# Diffusers
# pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
# image = pipe("a photo of an astronaut riding a horse on mars").images[0]

# LangChain
# prompt = PromptTemplate(input_variables=["product"], template="What is a good name for a company that makes {product}?")
# chain = LLMChain(llm=llm, prompt=prompt)

# OpenAI API Pattern
# openai.api_key = "..."
# response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
```
