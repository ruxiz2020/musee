import requests
from bs4 import BeautifulSoup
#import base64
#from langdetect import detect


class TextFromUrl:

    def __init__(self, url):
        """
        Extract text data from url
        """
        self._url = url

    def extract_text_from_html(self):

        response = requests.get(self._url)
        data = response.content.decode('utf-8', errors="replace")

        soup = BeautifulSoup(data, "lxml")
        page = soup.findAll('p')

        sentences = []
        for pp in page:

            text = pp.getText()
            if text.strip() != '':
                sentences.append(text + " ")
            # print(text)

        paragraph = ' '.join(sentences)
        return paragraph


if __name__ == "__main__":

    url = "https://www.animalwised.com/blood-in-cat-urine-home-remedies-3068.html"
    print(url)

    extractText = TextFromUrl(url)
    text = extractText.extract_text_from_html()

    print(text)
