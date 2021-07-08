# Basic imports
from flask import Flask, request, jsonify
import json

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

app = Flask(__name__)
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
@app.route("/macronize1")
def macronize1():
    sentence = request.form['sentence']
    macronizer = Macronizer('tag_ngram_123_backoff')
    result = macronizer.macronize_text(sentence)
    return json.dumps(result)
# ROUTE MAMCRONIZE2
@app.route("/macronize2")
def macronize2():
    sentence = request.form['sentence']
    macronizer = Macronizer('tag_tnt')
    result = macronizer.macronize_tags(sentence)
    return result
# ROUTE MAMCRONIZE3
@app.route("/macronize3")
def macronize3():
    sentence = request.form['sentence']
    macronizer = Macronizer('tag_crf')
    result = macronizer.macronize_text(sentence)
    return result
# ROUTE SCAN
@app.route("/scan")
def scan():
    sentence = request.form['sentence']
    scanner = Scansion()
    list = scanner.scan_text(sentence)
    return json.dumps(list)
    
# ROUTE MACRONIZE + SCAN
@app.route("/macro-scan")
def macronize_scan():
    sentence = request.form['sentence']
    scanner = Scansion()
    macronizer = Macronizer('tag_ngram_123_backoff')
    sentence_macronized = macronizer.macronize_text(sentence)
    result = scanner.scan_text(sentence_macronized)
    return json.dumps(result)
# ROUTE HEXAMETER
@app.route("/hexameter")
def hexameter():
    sentence = request.form['sentence']
    hexameter_scanner = HexameterScanner()
    list = hexameter_scanner.scan(sentence)
    return json.dumps(list.__dict__)
# ROUTE HEXAMETER
@app.route("/test")
def test():
    return request.form['sentence']




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
