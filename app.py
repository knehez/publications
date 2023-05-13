from flask import Flask, render_template
import requests
import collections

app = Flask(__name__)

@app.route('/')
def display_table():
    url = 'https://m2.mtmt.hu/api/publication?cond=publicationRole%3Beq%3BCORE&cond=authorships.organizations%3Binica%3B19408&cond=fullPublication%3Beq%3Btrue&cond=publishedYear%3Beq%3B2023&ty_on=1&ty_on_check=1&st_on=1&st_on_check=1&url_on=1&url_on_check=1&cite_type=2&sort=subType%2Casc&size=5000'

    response = requests.get(url)
    data = response.json()

    authors = {}

    publications = data['content']
    for publication in publications:
        numberOfAuthors = len(publication['authorships'])
        for author in publication['authorships']:
            if 'author' not in author:
                continue
            mtid = author['author']['mtid']
            if mtid not in authors.keys():
                authors[mtid] = {'name': author['familyName'] + ' ' + author['givenName'], 'numOfPublications': 0, 'pubs': []}
            authors[mtid]['numOfPublications'] += 1 / numberOfAuthors
            authors[mtid]['pubs'].append(publication['title'])

    authors = collections.OrderedDict(sorted(authors.items(), key=lambda x: x[1]['name']))

    return render_template('table.html', authors=authors)

if __name__ == '__main__':
    app.run()
