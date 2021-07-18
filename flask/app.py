# Basic imports
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pprint import pprint
import json
import jsonpickle



# NLTK Dependencies
import stanza
stanza.download("la") 
model_url = "http://vectors.nlpl.eu/repository/20/56.zip"
from cltk.utils import CLTK_DATA_DIR, get_file_with_progress_bar
get_file_with_progress_bar(model_url="https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.la.vec", file_path="/root/cltk_data/lat/embeddings/fasttext/wiki.la.vec")

# CLTK Corpora
from cltk.data.fetch import FetchCorpus
corpus_importer = FetchCorpus(language="lat")
corpus_importer.import_corpus('lat_models_cltk')
corpus_importer.import_corpus('lat_text_perseus')
corpus_importer.import_corpus('latin_pos_lemmata_cltk')
corpus_importer.import_corpus('lat_text_latin_library')
corpus_importer.import_corpus('latin_proper_names_cltk')
corpus_importer.import_corpus('latin_treebank_index_thomisticus')
corpus_importer.import_corpus('latin_lexica_perseus')
corpus_importer.import_corpus('latin_training_set_sentence_cltk')
corpus_importer.import_corpus('latin_text_antique_digiliblt')
corpus_importer.import_corpus('latin_text_poeti_ditalia')
corpus_importer.import_corpus('lat_text_tesserae')
corpus_importer.import_corpus('latin_text_corpus_grammaticorum_latinorum')

# CLTK Stemmer
from cltk.stem.lat import stem

# CLTK Decliner
from cltk.morphology.lat import CollatinusDecliner

# CLTK Lemmatizer
from cltk.lemmatize.lat import LatinBackoffLemmatizer

# CLTK POSTagger
from cltk.tag.pos import POSTag

# CLTK Macronizer
from cltk.prosody.lat.macronizer import Macronizer

# CLTK Prosody Scanner
from cltk.prosody.lat.scanner import Scansion

# CLTK Hexameter Scanner
from cltk.prosody.lat.hexameter_scanner import HexameterScanner

# CLTK NLP-Pipeline
from cltk import NLP

#CLTK Dependency Module
from cltk.dependency.tree import DependencyTree

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
@app.route("/macronize")
@cross_origin()
def macronize1():
    sentence = request.form['sentence']
    macronizer = Macronizer('tag_ngram_123_backoff')
    list = macronizer.macronize_text(sentence)
    return json.dumps(list)

# ROUTE MAMCRONIZE2
@app.route("/macronize-utf")
@cross_origin()
def macronize_utf():
    sentence = request.form['sentence']
    macronizer = Macronizer('tag_ngram_123_backoff')
    list = macronizer.macronize_text(sentence)
    return list

# ROUTE SCAN
@app.route("/scan")
@cross_origin()
def scan():
    sentence = request.form['sentence']
    scanner = Scansion()
    list = scanner.scan_text(sentence)
    return list
    
# ROUTE MACRONIZE + SCAN
@app.route("/macro-scan")
@cross_origin()
def macronize_scan():
    sentence = request.form['sentence']
    scanner = Scansion()
    macronizer = Macronizer('tag_ngram_123_backoff')
    sentence_macronized = macronizer.macronize_text(sentence)
    result = scanner.scan_text(sentence_macronized)
    return result

# ROUTE HEXAMETER
@app.route("/hexameter")
@cross_origin()
def hexameter():
    verse = request.form['verse']
    hexameter_scanner = HexameterScanner()
    list = hexameter_scanner.scan(verse)
    return json.dumps(list.__dict__)

# ROUTE PENTAMETER
@app.route("/pentameter")
@cross_origin()
def pentameter():
    verse = request.form['verse']
    pentameter_scanner = PentameterScanner()
    list = pentameter_scanner.scan(verse)
    return json.dumps(list.__dict__)

# ROUTE HENDEKASYLLABUS
@app.route("/hendecasyllabus")
@cross_origin()
def hendecasyllabus():
    verse = request.form['verse']
    hendecasyllabus_scanner = HendecasyllableScanner()
    list = hendecasyllabus_scanner.scan(verse)
    return json.dumps(list.__dict__)

# ROUTE ANALYSIS
@app.route('/analyze')
@cross_origin()
def analysis():
    text = request.form['text']
    cltk_nlp = NLP(language="lat")
    cltk_nlp.pipeline.processes.pop(-1)
    cltk_doc = cltk_nlp.analyze(text=text)
    return jsonpickle.encode(cltk_doc.sentences[0], unpicklable=False)

# ROUTE DEPENDENCY TREE
@app.route('/dependency-tree')
@cross_origin()
def dependency():
    sentence = request.form['sentence']
    cltk_nlp = NLP(language="lat")
    cltk_nlp.pipeline.processes.pop(-1)
    cltk_doc = cltk_nlp.analyze(text=sentence)
    dep_tree = DependencyTree.to_tree(cltk_doc.sentences[0])
    return jsonpickle.encode(dep_tree.get_dependencies(), unpicklable=False)

# ROUTE TEST
@app.route("/test1")
def test1():
    return request.json["sentence"]
# ROUTE TEST
@app.route("/test2")
def test2():
    return request.get_data()["sentence"]
# ROUTE TEST
@app.route("/test3")
def test3():
    return request.data["sentence"]
# ROUTE TEST
@app.route("/test4")
def test4():
    return request.get_json(force=True)["sentence"]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
