from asltutor.models.dictionary import Dictionary
from flask_mongoengine import MongoEngine
from flask import request, Response
from flask import Blueprint


dictionary = Blueprint('dictionary', __name__)


@dictionary.route('/dictionary/create', methods=['POST'])
def add_word():
    """Add a word to the dictionary

    Admins are able to add an ASL animation to our dictionary

    path parameter: /dictionary/create
    request body

    :rtype: None
    """
    if request.content_type != 'application/json':
        return Response('Failed: Content must be json', 400)

    r = request.get_json()
    o = Dictionary.objects(word__contains=r['word'])
    if o:
        o = Dictionary.objects.get(word=r['word'])
        for i in r:
            o[i] = r[i]
        o.save()
    else:
        Dictionary(**r).save()
    return Response('Success', 200)


@dictionary.route('/dictionary/delete', methods=['POST'])
def delete_word():
    """Delete a word from the dictioary

    Admins are able to delete a whole word object and animation from the database

    query parameter: /dictionary/delete?input=someword
    no request body

    :rtype: None
    """
    input_ = request.args.get('input')
    Dictionary.objects.get_or_404(word=input_).delete()
    return Response('Success', 200)


@dictionary.route('/dictionary', methods=['GET'])
def get_word():
    """Get a word in the dictionary

    Returns a JSON response contianing the word document of the word requested

    query parameter: /dictionary?input=someword
    no request body

    :rtype: JSON
    """
    input_ = request.args.get('input')
    o = Dictionary.objects.get_or_404(word=input_)
    if o.in_dictionary == False:
        Dictionary.objects(word=input_).update_one(
            upsert=True, inc__times_requested=1)
    return Response(o.to_json(), 200, mimetype='application/json')
