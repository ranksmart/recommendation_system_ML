#!/usr/bin/env python
# coding: utf-8

# In[198]:


import numpy as np
import pandas as pd
import joblib
# import pickle 


books = pd.read_csv('Books.csv')
ratings = pd.read_csv('Ratings.csv')
# users = pd.read_csv('Users.csv')



print(books.isnull().sum())
print(ratings.isnull().sum())

books.dropna(inplace=True)


books_ratings = books.merge(ratings,on='ISBN')

x=books_ratings.groupby('User-ID')['Book-Rating'].count()>100
user_id=x[x].index

books_ratings = books_ratings[books_ratings['User-ID'].isin(user_id)]

x=books_ratings.groupby('Book-Title')['Book-Rating'].count()>30
title=x[x].index


books_ratings = books_ratings[books_ratings['Book-Title'].isin(title)][['Book-Title','Book-Author','Year-Of-Publication','Image-URL-M','Book-Rating','User-ID']]


final_books = books_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')


final_books.fillna(0,inplace=True)

from sklearn.metrics.pairwise import cosine_similarity


sm=cosine_similarity(final_books)

books_idx =list(final_books.index)

def books(title):
    for b in books_idx:
        if title in b.lower():
            return books_idx.index(b)
    

def books_recommend(title):
    data=[]
    idx=books(title.lower())
    top = sorted(list(enumerate(sm[idx])),key=lambda x : x[1])[::-1][:10]
    for i,val in top:
        titles=books_ratings[books_ratings['Book-Title']==books_idx[i]][:1][['Book-Title','Book-Author','Year-Of-Publication','Image-URL-M']].values
        data.append(list(titles[0]))
    return data

joblib.dump(sm,open(r'similarity.pkl','wb'))

joblib.dump(books_ratings,open(r'books_ratings','wb'))
joblib.dump(books_idx,open(r'books_idx','wb'))
    




