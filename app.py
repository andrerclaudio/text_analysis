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
from replacers import RegexpReplacer

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

        # Init dicts and english stopwords
        self.replacer = RegexpReplacer()
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


def run(interval):
    """ Method that runs forever """
    while True:
        try:
            time.sleep(interval)

        except ThreadError as e:
            logger.exception('{}'.format(e))

        finally:
            pass


class ThreadingProcessQueue(object):
    """
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval):
        """
        Constructor
        """
        self.interval = interval

        thread = Thread(target=run, args=(self.interval,), name='Thread_name')
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution


def application():
    """" All application has its initialization from here """
    logger.info('Main application is running!')

    # NLTK initializer
    nlp = LanguageProcessor()
