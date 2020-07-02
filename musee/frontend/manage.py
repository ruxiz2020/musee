from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from musee.frontend.app import create_app
from musee.frontend.model import db, KeyWords
from musee.collect_text_data.textFromUrl import TextFromUrl
from musee.keyword_extract.extractKeywords import ExtractKeywords

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


def gen_input_text_keywords(url):
    '''Generate example inputs'''

    extractText = TextFromUrl(url)
    text = extractText.extract_text_from_html()

    extractKeywords = ExtractKeywords(text, 10)
    extractKeywords.extract_keywords()
    keywords = extractKeywords.keywords

    return keywords


@manager.command
def seed():
    url1 = "https://www.animalwised.com/blood-in-cat-urine-home-remedies-3068.html"
    keywords1 = gen_input_text_keywords(url1)
    str_keywords1 = ", ".join(str(x) for x in keywords1)
    KeyWords(url=url1, release_date=str_keywords1).insert()

    url2 = "https://www.akc.org/expert-advice/health/why-wont-my-dog-eat/"
    keywords2 = gen_input_text_keywords(url2)
    str_keywords2 = ", ".join(str(x) for x in keywords2)
    KeyWords(url=url2, release_date=str_keywords2).insert()


if __name__ == '__main__':
    manager.run()
