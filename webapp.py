from flask import Flask, render_template
from keys import key
from scraper_script import scrape

app = Flask(__name__)


@app.route('/')
def index():
    return "NOTHING HERE"

@app.route(f'/{key}')
def sc():
    scrape()
    return 979



if __name__ == '__main__':
    app.run()



