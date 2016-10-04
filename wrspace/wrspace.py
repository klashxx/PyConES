# -*- coding: utf-8 -*-
from flask import Flask, flash, redirect, render_template, request

import rspace.db.mysqlm as db
from rspace.common.exceptions import DBError

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        data=[{'name': 'pymysql'}, {'name': 'pyserver'}, {'name': 'invented'}])


@app.route("/space", methods=['GET', 'POST'])
def space():
    dbid = request.form.get('comp_select')

    try:
        db_conn = db.connect(dbid)
        rows = db.avaliable_space(db_conn).fetchall()
    except DBError:
        return render_template('error.html',
                               error="Can't connect to {0}".format(dbid))

    return render_template('space.html', data=rows, dbid=dbid)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
