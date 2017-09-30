from flask import Flask, jsonify, render_template, url_for
import json
import pandas as pd
import gensim


"""
	Data read
"""
model = gensim.models.Doc2Vec.load('./models/100features_40minwords_8context_doc')
data = pd.read_pickle('doc2vec/id_title_lang.pkl')

articles = {}

with open("doc2vec/output.json") as json_file:
    articles = json.load(json_file)


"""
	Main app
"""
app = Flask(__name__)
app.config.update(SERVER_NAME='127.0.0.1:5000', debug=True)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/api/books/<term>')
def get_articles_by(term):
	return jsonify(articles)

@app.route('/api/search/<string>')
def look_simular_books(string):
	if not isinstance(string, str):
		print('Some error')

	doc = string.split()
	inf_vec = model.infer_vector(doc)
	res = model.docvecs.most_similar([inf_vec])
	
	result = []
	for simular in res:
		obj = {}
		obj['id'] = str(simular[0])
		obj['prob'] = str(simular[1])
		obj['text'] = data.loc[simular[0]].title
		result.append(obj)
	return jsonify(result)

# @app.route('/api/get_topics/')
# def get_topics():
# 	result = []
# 	for claster in articles:
# 		top = {}
# 		top['id'] = claster['cluster']
# 		top['topics'] = claster['topics']
# 		result.append(top)
# 	return jsonify(result)

with app.app_context():
    url_for('static', filename='style.css')


