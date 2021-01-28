from flask import Flask, request, render_template
from itertools import islice

app = Flask(__name__)
feature_classes = {
    'A': 'страна, государство, регион,...',
    'H': 'ручей, озеро, ..',
    'L': 'парки,площади, ...',
    'P': 'города, села,...',
    'R': 'дороги, железная дорога',
    'S': 'здания, фермы',
    'T': 'горы,холмы,скалы,..',
    'U': 'подводный',
    'V': 'лес,пустошь,...'
}
name_doc = 'RU.txt'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200


@app.route('/id', methods=['POST'])
def handle_id():
    id = request.form['id']
    f = open(name_doc, 'r')

    text = 'ничего не найдено'
    for line in f.readlines():
        if id == line.split('\t')[0]:
            text = line
    if text != 'ничего не найдено':
        name = text.split('\t')[1] + ',' + text.split('\t')[2] + ',' + text.split('\t')[3]
        latitude = text.split('\t')[4]
        longitude = text.split('\t')[5]
        feature_class = feature_classes[text.split('\t')[6]]
        feature_code = text.split('\t')[7]
        country_code = text.split('\t')[8]
        timezone = text.split('\t')[17]
        modification_date = text.split('\t')[18]
        return render_template('geoname_id.html', id=id, name=name, latitude=latitude, longitude=longitude,
                               feature_class=feature_class, feature_code=feature_code,
                               country_code=country_code, timezone=timezone, modification_date=modification_date), 200
    else:
        return render_template('geoname_id.html', text=text), 200


@app.route('/page', methods=['POST'])
def handle_page():
    page = int(request.form['page'])
    number_page = int(request.form['number_page'])
    start_line = page * number_page - number_page
    stop_line = page * number_page
    f = open(name_doc, 'r')
    line = f.readlines()[start_line:stop_line]
    return render_template('page.html', posts=line), 200


@app.route('/equal', methods=['POST'])
def handle_equal():
    f = open(name_doc, 'r')
    first = {}
    second = {}
    clock = ''
    first_country = request.form['first']
    second_country = request.form['second']
    for line in f.readlines():
        if first_country == line.split('\t')[3].split(',')[-1]:
            first = {
                'id': line.split('\t')[0],
                'population': line.split('\t')[10],
                'name': line.split('\t')[1] + ',' + line.split('\t')[2] + ',' + line.split('\t')[3],
                'latitude': line.split('\t')[4],
                "longitude": line.split('\t')[5],
                "feature_class": feature_classes[line.split('\t')[6]],
                "feature_code": line.split('\t')[7],
                "country_code": line.split('\t')[8],
                "timezone": line.split('\t')[17],
                "modification_date": line.split('\t')[18]
            }
        if second_country == line.split('\t')[3].split(',')[-1]:
            second = {
                'id': line.split('\t')[0],
                'population': line.split('\t')[10],
                'name': line.split('\t')[1] + ',' + line.split('\t')[2] + ',' + line.split('\t')[3],
                'latitude': line.split('\t')[4],
                "longitude": line.split('\t')[5],
                "feature_class": feature_classes[line.split('\t')[6]],
                "feature_code": line.split('\t')[7],
                "country_code": line.split('\t')[8],
                "timezone": line.split('\t')[17],
                "modification_date": line.split('\t')[18]
            }
    if first != {} and second != {}:
        if first['latitude'] > second['latitude']:
            first_show = first
            second_show = second
        else:
            first_show = second
            second_show = first
        if first['timezone'] == second['timezone']:
            clock = 'одинаковые'
        else:
            clock = 'разные'
    else:
        first_show = first
        second_show = second
    return render_template('equal_page.html', first=first_show, second=second_show, clock=clock), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
