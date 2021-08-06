from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fcdsfdsf'

response = requests.get(
    'https://api.nbp.pl/api/exchangerates/tables/C?format=json')

content = response.content
data = json.loads(content)

currency_dict = {}

for x in (data[0]['rates']):
    currency_dict[x['code']] = x['bid']

for k, v in currency_dict.items():
    print(k, k)


class Form(FlaskForm):
    curre_code = SelectField('curre_code', choices={})


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'GET':
        form = Form()
        form.curre_code.choices = [(k, k) for k, v in currency_dict.items()]
        return render_template('walutomat.html', form=form)

    elif request.method == 'POST':
        print('We received POST')
        print(request.form)
        return redirect('/result.html')


@app.route('/result', methods=['POST'])
def form():
    currency_code = request.form.get('curre_code')
    currency_amount = request.form.get('currency_amount')

    total_value_pln = float(
        currency_dict[currency_code]) * float(currency_amount)
    total_value_pln = round(total_value_pln, 2)
    print(total_value_pln)

    title = "Kalkulator"
    return render_template('result.html', title=title, currency_code=currency_code, currency_amount=currency_amount, total_value_pln=total_value_pln)
