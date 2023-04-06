# import BooksCollaborativeFilteringSystem as cf 

import joblib 

sm = joblib.load(open('similarity.pkl','rb'))
books_idx = joblib.load(open('books_idx','rb'))
books_ratings = joblib.load(open('books_ratings','rb'))

from flask import Flask,render_template,request,jsonify
app = Flask(__name__)
 

def books(title):
    for b in books_idx:
        if title in b.lower():
            return books_idx.index(b)
collect=[]
for b in books_idx:
    all=books_ratings[books_ratings['Book-Title']==b][:1][['Book-Title','Book-Author','Year-Of-Publication','Image-URL-M']].values
    collect.append(list(all[0]))

@app.route('/')
def home():
    return render_template('index.html',books=collect)

@app.route('/Recommendation',methods=['POST'])
def books_recommend():
    data=[]
    title=request.form['input']
    idx=books(title.lower())
    if idx is not None:
        top = sorted(list(enumerate(sm[idx])),key=lambda x : x[1])[::-1][:10]
        for i,val in top:
            titles=books_ratings[books_ratings['Book-Title']==books_idx[i]][:1][['Book-Title','Book-Author','Year-Of-Publication','Image-URL-M']].values
            data.append(list(titles[0]))
        # print(data)
        return render_template('recommend.html',data=data,inp=title)
    
    return render_template('recommend.html',data=data,inp=title)
 
if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')

