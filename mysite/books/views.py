from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from .models import book_model
from . import urls
# Create your views here.
def index(request):
    return render(request,"master.html")

def result(request):
	context = {}
	if ("book_code" in request.POST): 
		try:
			if request.POST["book_code"] != '':
				
				books_isbn = get_recommends(request.POST["book_code"])
			else:
				
				books_isbn = get_recommends()
			
			books = get_books_info(books_isbn)
			books = list(map(book_model,books))
			
			context = {
			'books': books,
			}
			return render(request,'results.html',context=context)
		except KeyError:
			return render(request,'fail.html')
	return render(request,'results.html',context=context)
			
	
	

def get_recommends(isbn = None):

  if isbn == None: isbn = "0451524934"
  
  x=urls.piv.loc[isbn].array.reshape(1, -1)
  distances,indices=urls.model_knn.kneighbors(x,n_neighbors=6)
  R_books=[]
  for distance,indice in zip(distances[0],indices[0]):
    if distance!=0:
      R_book=urls.piv.index[indice]
      R_books.append(R_book)
  if isbn in R_books: R_books.remove(isbn)
  return R_books

def get_books_info(isbn_list):
	df = pd.read_csv(
    os. getcwd() + r"\mystaticfiles\BX-Books.csv",
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author','release_year','publisher','Image-URL-S',"Image-URL-M","Image-URL-L"],
    usecols=['isbn', 'title', 'author','release_year','publisher','Image-URL-S',"Image-URL-M","Image-URL-L"],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str',
	'release_year':'str','publisher':'str',"Image-URL-S":'str',"Image-URL-M":'str',"Image-URL-L":'str'})
	
	df = df[df['isbn'].isin(isbn_list)]
	return(df.to_dict(orient='records'))
	