import csv
import json
import requests


from faker import Faker
from flask import Flask, request
from markupsafe import escape
from statistics import mean

app = Flask(__name__)
fake = Faker()


@app.route('/')
def hello():
    return '<h2> Hello user! <h2/>'


@app.route('/requirements')
def get_requirements():
    requirements_str = f'<h3> REQUIREMENTS <br/> <h3/>'
    with open('requirements.txt', mode='rb') as file:
        reader = file.read()
        requirements = reader.decode('utf-16').split()
        for item in requirements:
            requirements_str += f'<h3> {item} <br/> <h3/>'
        return requirements_str


@app.route('/user/generate/')
def get_people_email():
    number = request.args.get('number', 100)
    try:
        people_number = int(escape(number))
    except ValueError:
        return '<h2>User please enter a number!<h2/>', 422
    people_str = generate_people_email(people_number)
    return people_str


def generate_people_email(people_number):
    people_str = f' <h5> RANDOM PEOPLE AND EMAIL <br/> <h5/>'
    random_people = []
    for _ in range(people_number):
        random_people.append([fake.name(), fake.email()])
    for item in random_people:
        people_str += f' <h5> {item[0]} ---- {item[1]} <br/> <h5/>'
    return people_str


@app.route('/mean/')
def get_weight_height():
    weight, height = weight_height('hw.csv')
    mean_weight = round(mean(weight) * 0.45359237, 2)
    mean_height = round(mean(height) * 2.54, 2)
    weight_height_str = f'<h3>середній зріст: {mean_height} см, середня вага: {mean_weight} кг <h3/>'
    return weight_height_str


def weight_height(file):
    weight = []
    height = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            if row:
                weight.append(float(row[2]))
                height.append(float(row[1]))
        return weight, height


@app.route('/space/')
def get_people_in_space():
    people_list = people_in_space()
    people_in_space_str = f'<h4> PEOPLE IN SPACE <br/> <h4/>'
    for people in people_list:
        people_in_space_str += f'<h4> {people["name"]} --- {people["craft"]} <br/> <h4/>'
    return people_in_space_str


def people_in_space():
    get_requests = requests.get('http://api.open-notify.org/astros.json')
    if get_requests.status_code == 200:
        people_list = json.loads(get_requests.content)
        return people_list['people']


if __name__ == '__main__':
    app.run(debug=True)

