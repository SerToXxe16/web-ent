import flask
from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
secret='gfyfhfhfhfthfhfhyfh'
# Create some test data for our catalog in the form of a list of dictionaries.
books = [
{'id': 0,
'title': 'A Fire Upon the Deep',
'author': 'Vernor Vinge',
'first_sentence': 'The coldsleep itself was dreamless.',
'year_published': '1992'},
{'id': 1,
'title': 'The Ones Who Walk Away From Omelas',
'author': 'Ursula K. Le Guin',
'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
'published': '1973'},
{'id': 2,
'title': 'Dhalgren',
'author': 'Samuel R. Delany',
'first_sentence': 'to wound the autumnal city.',
'published': '1975'}
]

@app.route('/', methods=['GET'])

def home():
    return render_template("login.html") 
# A route to return all of the available entries in ourcatalog.

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
# Check if an ID was provided as part of the URL.
# If ID is provided, assign it to a variable.
# If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        _id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    for book in books:
        if book['id'] == _id:
            results.append(book)
# Use the jsonify function from Flask to convert our list of
# Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
