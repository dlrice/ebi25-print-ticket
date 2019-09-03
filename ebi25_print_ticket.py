#!/usr/bin/env python
import sys
from flask import Flask, render_template, request
from flask_cors import CORS
from jinja2 import Template
import pdfkit
import os
import uuid
import json
import pathlib

app = Flask(__name__)
CORS(app)

TMP = '~/ebi25/tmp'
pathlib.Path(TMP).mkdir(parents=True, exist_ok=True)


template = Template('''
<html>
  <head>
    <style>
      body {
        font-size: 40px;
        padding-left: 18px;
      }
    </style>
  </head>
  <body>
    {{ number }}
  </body>
</html>
''')


def send_pdf_to_printer(pdf_path):
    command = 'lp {}'.format(pdf_path)
    os.system(command)


def generate_pdf(number):
    filename = uuid.uuid4().hex
    html_path = os.path.join(TMP, '{}.html'.format(filename))
    pdf_path = os.path.join(TMP, '{}.pdf'.format(filename))
    with open(html_path, 'w') as f:
        f.write(template.render(number=number))
    pdfkit.from_file(html_path, pdf_path)
    return pdf_path


def success():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def failure(exception):
    return json.dumps({'success': False, 'exception': exception}), 400, {'ContentType': 'application/json'}


@app.route("/<number>/")
def print_number(number):
    try:
        pdf_path = generate_pdf(number)
        send_pdf_to_printer(pdf_path)
    except Exception as e:
        return failure(e)
    else:
        return success()


def test():
    pdf_path = generate_pdf('123456')
    send_pdf_to_printer(pdf_path)


if __name__ == '__main__':
    test()