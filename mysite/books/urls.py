from django.urls import path
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import os
from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("search", views.result, name="results"),
	
]



df_books = pd.read_csv(
    os. getcwd() + r"\mystaticfiles\BX-Books.csv",
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author'],
    usecols=['isbn', 'title', 'author'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

df_ratings = pd.read_csv(
    os. getcwd() +  r"\mystaticfiles\BX-Book-Ratings.csv",
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

df = df_ratings

counts1 = df['user'].value_counts()
counts2 = df['isbn'].value_counts()

df = df[~df['user'].isin(counts1[counts1 < 200].index)]
df = df[~df['isbn'].isin(counts2[counts2 < 100].index)]

df = pd.merge(right=df, left = df_books, on="isbn")
df = df.drop_duplicates(["title", "user"])
piv = df.pivot(index='isbn', columns='user', values='rating').fillna(0)



matrix = piv.values

model_knn=NearestNeighbors(metric='cosine',algorithm='brute')
model_knn.fit(matrix)

print("model has been trained")