import yake
from musee.collect_text_data.textFromUrl import TextFromUrl


class ExtractKeywords:

    def __init__(self, text, top_n):
        """
        Extract top n keywords from string that contains sentences.
        """
        self._text = text
        self._language = "en"
        self._max_ngram_size = 4
        self._deduplication_thresold = 0.9
        self._deduplication_algo = 'seqm'
        self._windowSize = 1
        self._numOfKeywords = top_n

        self.keywords = []

    def extract_keywords(self):

        custom_kw_extractor = yake.KeywordExtractor(lan=self._language,
                                                    n=self._max_ngram_size,
                                                    dedupLim=self._deduplication_thresold,
                                                    dedupFunc=self._deduplication_algo,
                                                    windowsSize=self._windowSize,
                                                    top=self._numOfKeywords,
                                                    features=None)

        keywords = custom_kw_extractor.extract_keywords(self._text)

        for kw in keywords:
            self.keywords.append(kw)


if __name__ == "__main__":

    url = "https://www.animalwised.com/blood-in-cat-urine-home-remedies-3068.html"
    print(url)

    extractText = TextFromUrl(url)
    text = extractText.extract_text_from_html()

    extractKeywords = ExtractKeywords(text, 10)
    extractKeywords.extract_keywords()
    keywords = extractKeywords.keywords

    print(text[:100])
    print(keywords)
