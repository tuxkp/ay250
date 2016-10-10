import os
from app import app
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pybtex.database.input import bibtex
import sqlite3
import itertools
import unicodedata

@app.route('/')
@app.route('/index')

def index():
    app = Flask(__name__)
    if os.path.isfile('bibtex.db'):
        conn = sqlite3.connect('bibtex.db')
        c = conn.cursor()
        collections = {}
        for row in c.execute("SELECT collection from bibtex"):
           for member in row:
               collections[str(member)] = 1
        return render_template('index.html', database='bibtex.db', collections=collections)
    return render_template('index.html')

@app.route('/insert_collection')
def insert_collection():
    app = Flask(__name__)
    if os.path.isfile('bibtex.db'):
        return render_template('insert_collection.html',database='bibtex.db')
    return render_template('insert_collection.html')

@app.route('/upload', methods=['POST'])
def upload():
    app = Flask(__name__)
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('data/', filename))
    collection = os.path.splitext(filename)[0]
    conn = sqlite3.connect('bibtex.db')
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE bibtex (collection text, ref_id text, title text, volume text, journal text, pages text, year text, author_list text)''')
        print("CREATING DATABASE")
    except:
        print("DATABASE EXISTS")
    parser = bibtex.Parser()
    bibdata = parser.parse_file(os.path.join('data/',filename))
    count = 0
    for bib_id in bibdata.entries:
        b = bibdata.entries[bib_id].fields 
        count += 1
        try:
            REF_ID = bib_id.encode('ascii', 'ignore')
            TITLE = b["title"].encode('ascii', 'ignore')
            VOLUME = b["volume"].encode('ascii', 'ignore')
            JOURNAL = b["journal"].encode('ascii', 'ignore')
            PAGES = b["pages"].encode('ascii', 'ignore')
            YEAR = b["year"].encode('ascii', 'ignore')
            AUTHORS = ""
            for author in bibdata.entries[bib_id].persons["author"]:
                if AUTHORS:
                    AUTHORS += " and " + author.last_names[0].encode('ascii', 'ignore') + ", " + author.first_names[0].encode('ascii','ignore')
                else:
                    AUTHORS += author.last_names[0].encode('ascii', 'ignore') + ", " + author.first_names[0].encode('ascii','ignore')
            AUTHORS = AUTHORS.replace("'", "")
            AUTHORS = AUTHORS.replace("{", "")
            AUTHORS = AUTHORS.replace("}", "")
            TITLE = TITLE.replace("}", "")
            TITLE = TITLE.replace("{", "")
            c.execute("INSERT INTO bibtex VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(collection, REF_ID, TITLE, VOLUME, JOURNAL, PAGES, YEAR, AUTHORS ))
        except(KeyError):
            print("ERROR!!!  --- " + str(count) + " -----")
            continue
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/query', methods = ['GET', 'POST'])

def query():
    app = Flask(__name__)
    results = []
    querystring = ""
    try:
        querystring = request.form['querystring']
    except:
        print("NO QUERYSTRING")
    print("________________________________")
    print(querystring)
    print("________________________________")
    conn = sqlite3.connect('bibtex.db')
    c = conn.cursor()
    if querystring:
        for row in dict_gen(c.execute("SELECT * from bibtex where " + querystring)):
            print("GOT ONE")
            results.append(row) 
    if os.path.isfile('bibtex.db'):
        if results:
            return render_template('query.html', database='bibtex.db', results=results)
        return render_template('query.html', database='bibtex.db')
    return render_template('query.html')


def dict_gen(curs):
    ''' From Python Essential Reference by David Beazley
    '''
    field_names = [d[0].lower() for d in curs.description]
    while True:
        rows = curs.fetchmany()
        if not rows: return
        for row in rows:
            yield dict(itertools.izip(field_names, row))

