# Build-in modules
import logging
import time
from datetime import timedelta
from threading import ThreadError, Thread

import enchant
import nltk
from nltk.corpus import stopwords
# Added modules
from ttictoc import TicToc

# Project modules
from replacers import RegexpReplacer, SpellingReplacer, RepeatReplacer
from text_parse import text_parser as parser

# Print in file
# logging.basicConfig(filename='logs.log',
#                     filemode='w',
#                     level=logging.INFO,
#                     format='%(asctime)s | %(process)d | %(name)s | %(levelname)s:  %(message)s',
#                     datefmt='%d/%b/%Y - %H:%M:%S')

# Print in software terminal
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(process)d | %(name)s | %(levelname)s:  %(message)s',
                    datefmt='%d/%b/%Y - %H:%M:%S')

logger = logging.getLogger(__name__)


class LanguageProcessor(object):
    """
    Natural language processor package initializer
    """

    def __init__(self):
        """
        Download or/and update the language-neutral sentence segmentation tool
        """
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        # Init dicts and english stopwords
        self.replacer = RegexpReplacer()
        self.repeat = RepeatReplacer()
        self.spelling = SpellingReplacer()
        self.word_dict = enchant.Dict("en_US")
        self.stops = set(stopwords.words('english'))


class ElapsedTime(object):
    """
    Measure the elapsed time between some "object.t" and "object.elapsed".
    """

    def __init__(self):
        self.t = TicToc(__name__)
        self.t.tic()

    def elapsed(self):
        self.t.toc()
        _elapsed = self.t.elapsed
        d = timedelta(seconds=_elapsed)
        logger.info('< {} >'.format(d))


class ThreadingProcess(object):
    """
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval, nlp):
        """
        Constructor
        """
        self.interval = interval
        self.nlp = nlp

        thread = Thread(target=run, args=(self.interval, self.nlp), name='Processor')
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        thread.join()


def run(interval, nlp):
    """ Method that runs forever """
    while True:
        try:
            file = open_file()
            if file is not False:
                parser(nlp, file)
            time.sleep(interval)

        except ThreadError as e:
            logger.exception('{}'.format(e))

        finally:
            pass


def application():
    """" All application has its initialization from here """
    logger.info('Main application is running!')

    # NLTK initializer
    nlp = LanguageProcessor()

    # Set a delay between thread call
    process_timing = 1
    # Start processing all information
    ThreadingProcess(process_timing, nlp)


def open_file():
    """
    Open a txt file and return it, or False otherwise.
    """
    try:
        with open('file.txt', 'r') as file:
            stream = file.read()
            if len(stream) > 0:
                file.close()
                return stream

    except Exception as e:
        logger.exception('{}'.format(e), exc_info=False)

    return False
