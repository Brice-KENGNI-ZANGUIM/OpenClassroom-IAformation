# -*- coding: utf-8 -*-
"""

Created on Thu Sep 15 18:11:37 2022


@author: KENGNI ZANGUIM BRICE

"""

import requests
from main import app
from flask import jsonify, request


app.config["DEBUG"] = False


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



@app.route("/")
def home_view():
	return "<h1>Ma toute première API faite de zéro</h1> <p>Dans le cadre du projet 7 de ma formation en \
		   intelligence artificielle je dois <strong> Créer une API pour déployer mon modèle de machine Learning \
			   <strong>   </p>"


# A route to return all of the available entries in our catalog.
@app.route('/books/all', methods=['GET'])
def api_all():
 return jsonify(books)


@app.route('/ressourses/books/<int:book_id>', methods=['GET'])
@app.route('/books/<int:book_id>', methods=['GET'])
def api_book_id( book_id ):
 return jsonify(books[book_id])


@app.route('/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Erreur: Vous n'avez pas spécifié une ID. \n veillez fournir une ID à l'API svp ! ! "
    # Create an empty list for our results
    results = []
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

  
if __name__ == "__main__" :
	app.run( host ="0.0.0.0" ) 
