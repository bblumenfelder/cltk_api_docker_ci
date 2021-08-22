# Basic imports
from cltk.dependency.tree import DependencyTree
from cltk import NLP
from cltk.prosody.lat.hexameter_scanner import HexameterScanner
from cltk.prosody.lat.pentameter_scanner import PentameterScanner
from cltk.prosody.lat.scanner import Scansion
from cltk.prosody.lat.macronizer import Macronizer
from cltk.prosody.lat.scansion_formatter import ScansionFormatter
from cltk.tag.pos import POSTag
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.morphology.lat import CollatinusDecliner
from cltk.stem.lat import stem
from cltk.sentence.lat import LatinPunktSentenceTokenizer
from macronizer import Macronizer
from scanner import scan_cltk_format

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json
import jsonpickle
import unicodedata

# Initialize CLTK-Pipeline
cltk_nlp = NLP(language="lat")
cltk_nlp.pipeline.processes.pop(-1)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# ROUTE: TAG
@app.route("/tag/<form>")
def tag(form):
    tagger = POSTag("lat")
    list = tagger.tag_ngram_123_backoff(form)
    return json.dumps(list)

# ROUTE: STEM


@app.route("/stem/<form>")
def get_stem(form):
    string = stem(form)
    return json.dumps(string)

# ROUTE DECLINE


@app.route("/decline/<form>")
def decline(form):
    decliner = CollatinusDecliner()
    list = decliner.decline(form)
    return json.dumps(list)

# ROUTE LEMMATIZE


@app.route("/lemmatize/<form>")
def lemmatize(form):
    lemmatizer = LatinBackoffLemmatizer()
    list = lemmatizer.lemmatize(form)
    return json.dumps(list)

# ROUTE MAMCRONIZE1


@app.route("/macronize", methods=['POST'])
@cross_origin()
def macronize1():
    data = request.get_json(force=True)
    sentence = data['sentence']
    macronizer = Macronizer('tag_ngram_123_backoff')
    list = macronizer.macronize_text(sentence)
    return json.dumps(list)

# ROUTE MAMCRONIZE2


@app.route("/macronize-utf", methods=['POST'])
@cross_origin()
def macronize_utf():
    data = request.get_json(force=True)
    sentence = data['sentence']
    macronizer = Macronizer('tag_ngram_123_backoff')
    list = macronizer.macronize_text(sentence)
    return list


@app.route('/alatius/macronize/ambig-html', methods=['POST'])
@cross_origin()
def alatius_macronize_ambig_html():
    data = request.get_json(force=True)
    sentence = data['sentence']
    macronizer = Macronizer()
    macronizedtext = macronizer.macronize(
        sentence, performitoj=True, markambigs=True, tojson=False, minimaltext=False, ambiguousvowels=False)
    return macronizedtext


@app.route('/alatius/macronize/ambig-json', methods=['POST'])
@cross_origin()
def alatius_macronize_ambig_json():
    data = request.get_json(force=True)
    sentence = data['sentence']
    macronizer = Macronizer()
    macronizedtext = macronizer.macronize(
        sentence, performitoj=True, markambigs=True, tojson=True, minimaltext=False, ambiguousvowels=False)
    return macronizedtext


@app.route('/alatius/macronize/ambig-vowels', methods=['POST'])
@cross_origin()
def alatius_macronize_ambig_vowels():
    data = request.get_json(force=True)
    sentence = data['sentence']
    macronizer = Macronizer()
    macronizedtext = macronizer.macronize(
        sentence, performitoj=True, markambigs=True, tojson=False, minimaltext=False, ambiguousvowels=True)
    return json.dumps(macronizedtext)


@app.route('/alatius/macronize/min', methods=['POST'])
@cross_origin()
def alatius_macronize_min():
    data = request.get_json(force=True)
    sentence = data['sentence']
    macronizer = Macronizer()
    macronizedtext = macronizer.macronize(
        sentence, performitoj=True, markambigs=False, tojson=False, minimaltext=True, ambiguousvowels=False)
    return macronizedtext


@app.route('/alatius/scan', methods=['POST'])
@cross_origin()
def alatius_scan():
    data = request.get_json(force=True)
    verse = unicodedata.normalize('NFC', data['sentence'])
    meter = data['meter']
    scansion = scan_cltk_format(verse, meter)

    return json.dumps(scansion)


# ROUTE SCAN


@app.route("/scan", methods=['POST'])
@cross_origin()
def scan():
    data = request.get_json(force=True)
    sentence = data['sentence']
    scanner = Scansion()
    list = scanner.scan_text(sentence)
    return list

# ROUTE MACRONIZE + SCAN


@app.route("/macro-scan", methods=['POST'])
@cross_origin()
def macronize_scan():
    data = request.get_json(force=True)
    sentence = data['sentence']
    scanner = Scansion()
    macronizer = Macronizer('tag_ngram_123_backoff')
    sentence_macronized = macronizer.macronize_text(sentence)
    result = scanner.scan_text(sentence_macronized)
    return jsonpickle.encode(result, unpicklable=False)

# ROUTE HEXAMETER


@app.route("/hexameter", methods=['POST'])
@cross_origin()
def hexameter():
    data = request.get_json(force=True)
    verse = data['verse']
    if("macronize" in data):
        macronize = data['macronize']
    else:
        macronize = True
    if ("macronizer" in data):
        macronizertype = data['macronizer']
    else:
        macronizertype = 'tag_ngram_123_backoff'
    if(macronize == True):
        macronizer = Macronizer(macronizertype)
        verse = macronizer.macronize_text(verse)
    hexameter_scanner = HexameterScanner()
    Result = hexameter_scanner.scan(verse).__dict__
    scansion_formatter = ScansionFormatter()
    formatted = scansion_formatter.hexameter(
        Result['scansion'].replace(" ", ""))
    Result['formatted'] = formatted
    return json.dumps(Result)

# ROUTE PENTAMETER


@app.route("/pentameter", methods=['POST'])
@cross_origin()
def pentameter():
    data = request.get_json(force=True)
    verse = data['verse']
    if("macronize" in data):
        macronize = data['macronize']
    else:
        macronize = True
    if ("macronizer" in data):
        macronizertype = data['macronizer']
    else:
        macronizertype = 'tag_ngram_123_backoff'
    if(macronize == True):
        macronizer = Macronizer(macronizertype)
        verse = macronizer.macronize_text(verse)
    pentameter_scanner = PentameterScanner()
    list = pentameter_scanner.scan(verse)
    return json.dumps(list.__dict__)

# ROUTE HENDEKASYLLABUS


@app.route("/hendecasyllabus", methods=['POST'])
@cross_origin()
def hendecasyllabus():
    data = request.get_json(force=True)
    verse = data['verse']
    hendecasyllabus_scanner = HendecasyllableScanner()
    list = hendecasyllabus_scanner.scan(verse)
    return json.dumps(list.__dict__)


# ROUTE TOKENIZATION
@app.route('/tokenize', methods=['POST'])
@cross_origin()
def sentence_tokenization():
    data = request.get_json(force=True)
    text = data['text']
    splitter = LatinPunktSentenceTokenizer(strict=True)
    sentences = splitter.tokenize(text)
    return jsonpickle.encode(sentences, unpicklable=False)


# ROUTE ANALYSIS
@app.route('/analyze', methods=['POST'])
@cross_origin()
def analysis():
    data = request.get_json(force=True)
    text = data['text']
    cltk_doc = cltk_nlp.analyze(text=text)
    return jsonpickle.encode(cltk_doc.sentences[0], unpicklable=False)

# ROUTE DEPENDENCY TREE


@app.route('/dependency-tree', methods=['POST'])
@cross_origin()
def dependency():
    data = request.get_json(force=True)
    sentence = data['sentence']
    cltk_doc = cltk_nlp.analyze(text=sentence)
    dep_tree = DependencyTree.to_tree(cltk_doc.sentences[0])
    return jsonpickle.encode(dep_tree.get_dependencies(), unpicklable=False)

# ROUTE TEST


@app.route('/test')
@cross_origin()
def test():
    return "Successful"


@app.route('/')
@cross_origin()
def welcome():
    return "Welcome to Hermeneus-API!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
