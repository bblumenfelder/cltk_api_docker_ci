# NLTK Dependencies
from cltk.data.fetch import FetchCorpus
from cltk.utils import CLTK_DATA_DIR, get_file_with_progress_bar
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
corpus_importer.import_corpus('latin_lexica_perseus')
corpus_importer.import_corpus('latin_training_set_sentence_cltk')
corpus_importer.import_corpus('latin_text_antique_digiliblt')
corpus_importer.import_corpus('latin_text_poeti_ditalia')
corpus_importer.import_corpus('lat_text_tesserae')
corpus_importer.import_corpus('latin_text_corpus_grammaticorum_latinorum')
