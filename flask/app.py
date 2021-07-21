# Basic imports
from cltk.dependency.tree import DependencyTree
from cltk import NLP
from cltk.prosody.lat.hexameter_scanner import HexameterScanner
from cltk.prosody.lat.scanner import Scansion
from cltk.prosody.lat.macronizer import Macronizer
from cltk.tag.pos import POSTag
from cltk.lemmatize.lat import LatinBackoffLemmatizer
from cltk.morphology.lat import CollatinusDecliner
from cltk.stem.lat import stem
from cltk.data.fetch import FetchCorpus
from cltk.utils import CLTK_DATA_DIR, get_file_with_progress_bar
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pprint import pprint
import json
import jsonpickle


# NLTK Dependencies
import stanza
stanza.download("la")
model_url = "http://vectors.nlpl.eu/repository/20/56.zip"
get_file_with_progress_bar(model_url="https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.la.vec",
                           file_path="/root/cltk_data/lat/embeddings/fasttext/wiki.la.vec")

# CLTK Corpora
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

# CLTK Decliner

# CLTK Lemmatizer

# CLTK POSTagger

# CLTK Macronizer

# CLTK Prosody Scanner

# CLTK Hexameter Scanner

# CLTK NLP-Pipeline

# CLTK Dependency Module

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
    return result

# ROUTE HEXAMETER


@app.route("/hexameter", methods=['POST'])
@cross_origin()
def hexameter():
    data = request.get_json(force=True)
    verse = data['verse']
    hexameter_scanner = HexameterScanner()
    list = hexameter_scanner.scan(verse)
    return json.dumps(list.__dict__)

# ROUTE PENTAMETER


@app.route("/pentameter", methods=['POST'])
@cross_origin()
def pentameter():
    data = request.get_json(force=True)
    verse = data['verse']
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


@app.route("/test1", methods=['POST'])
@cross_origin()
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


@app.route("/test4",  methods=['POST'])
@cross_origin()
def test4():
    data = request.get_json(force=True)
    return data["sentence"]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
