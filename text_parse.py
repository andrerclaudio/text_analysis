# Build-in modules
import logging
from string import punctuation

# Added modules
from nltk.tokenize import sent_tokenize, word_tokenize

# Project modules


logger = logging.getLogger(__name__)


def text_parser(nlp, content):
    """
    Text parser
    """
    content = str(content)

    # if content.isprintable() or content.isspace():
    #     logger.exception('{}'.format('The content is not parsable!'), exc_info=False)
    #     return

    content = content.lower()

    # Normalize the content exchanging the contraction form of words with its complete format.
    content = nlp.replacer.replace(content)
    # Split the content into sentences and remove its punctuation
    sentences = [remove_punctuation(i) for i in sent_tokenize(content)]
    # Remove repeated characters from a Word
    sentences = [remove_repeated_chars(nlp, i) for i in sentences]
    # Fix misspellings words
    sentences = [fix_spelling(nlp, i) for i in sentences]
    # Check if a sentence is parsable
    sentences = check_sentences_sanity(sentences)

    for s in sentences:
        logger.info('{}'.format(s))

    return


def remove_punctuation(stream):
    """
    Remove all characters punctuations from a given stream buffer

    :param stream: A string with words to remove punctuation
    :type stream: string
    :return A string with the same words minus punctuations characters
    """
    ch = [char for char in stream if char not in punctuation]
    return ''.join(ch)


def remove_repeated_chars(nlp, stream):
    """
    Remove all repeated characters in a word from a given stream buffer

    :param nlp: Natural language processing object
    :param stream: A string with words to remove repeated chars
    :type stream: string
    :return A string with the same words minus repeated characters
    """
    words = word_tokenize(stream)
    ch = [nlp.repeat.replace(w) for w in words]
    return ' '.join(ch)


def fix_spelling(nlp, stream):
    """
    Fix misspelling words

    :param nlp: Natural language processing object
    :param stream: A string with words to fix spealling
    :type stream: string
    :return A string with the same words with fixed words
    """
    words = word_tokenize(stream)
    ch = [nlp.spelling.replace(w) for w in words]
    return ' '.join(ch)


def check_sentences_sanity(buffer):
    """
    Check each sentence in a list if they are parsable

    :param buffer: A list with sentences
    :type buffer: list
    :return A list with parsable sentences
    """
    ph = []
    while len(buffer) > 0:
        t = buffer.pop()
        if t.isalpha() or t.isspace() or not t.isnumeric:
            logger.exception('{}'.format(t), exc_info=False)
        else:
            ph.append(t)
    if len(ph) > 0:
        ph.reverse()

    return ph
