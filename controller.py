#!/usr/bin/env python3

import json
import os
import random
import shutil

# https://docs.python.org/3/howto/logging.html
import logging
# https://gist.github.com/ibeex/3257877
from logging.handlers import RotatingFileHandler

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
from flask_wtf import FlaskForm, CSRFProtect, Form  # type: ignore

from wtforms import StringField, validators, FieldList, FormField, IntegerField, RadioField, PasswordField, SubmitField, BooleanField  # type: ignore


# https://hplgit.github.io/web4sciapps/doc/pub/._web4sa_flask004.html
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    flash,
    jsonify,
    Response,
)

from config import (
    Config,
)  # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

import compute


# https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
csrf = CSRFProtect()

app = Flask(__name__, static_folder="static")
app.config.from_object(
    Config
)  # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

# https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask
csrf.init_app(app)


log_size = 10000000
# https://gist.github.com/ibeex/3257877
handler_debug = RotatingFileHandler(
        "logs/flask_critical_and_error_and_warning_and_info_and_debug.log",
        maxBytes=log_size,
        backupCount=2,
    )
handler_debug.setLevel(logging.DEBUG)
handler_info = RotatingFileHandler(
        "logs/flask_critical_and_error_and_warning_and_info.log",
        maxBytes=log_size,
        backupCount=2,
    )
handler_info.setLevel(logging.INFO)
handler_warning = RotatingFileHandler(
        "logs/flask_critical_and_error_and_warning.log",
        maxBytes=log_size,
        backupCount=2,
    )

handler_warning.setLevel(logging.WARNING)

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
        handlers=[handler_debug, handler_info, handler_warning],
        level=logging.DEBUG,
        format="%(asctime)s|%(filename)-13s|%(levelname)-5s|%(lineno)-4d|%(funcName)-20s|%(message)s"  # ,
)

logger = logging.getLogger(__name__)
# http://matplotlib.1069221.n5.nabble.com/How-to-turn-off-matplotlib-DEBUG-msgs-td48822.html
# https://github.com/matplotlib/matplotlib/issues/14523
logging.getLogger("matplotlib").setLevel(logging.WARNING)


class TableSizeForm(FlaskForm):
    logger.info("[trace]")
    #    r = FloatField(validators=[validators.InputRequired()])
    #    r = FloatField()
    table_rows = IntegerField(
        "number of rows", validators=[validators.InputRequired(), validators.Length(max=100)]
    )
    table_cols = IntegerField(
        "number of columns", validators=[validators.InputRequired(), validators.Length(max=100)]
    )
    number_of_single = IntegerField(
        "number of single", validators=[validators.InputRequired(), validators.Length(max=100)]
    )
    number_of_double_sym = IntegerField(
        "number of symmetric double", validators=[validators.InputRequired(), validators.Length(max=100)]
    )
    number_of_double_asym = IntegerField(
        "number of asymmetric double", validators=[validators.InputRequired(), validators.Length(max=100)]
    )
    filename = StringField("name of output file", validators=[validators.InputRequired(), validators.Length(max=1000)])


@app.route("/table_dimensions", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def table_dimensions():
    """
    step 1: how big is the table?
    """
    trace_id = str(random.randint(1000000, 9999999))
    logger.info("[trace page start " + trace_id + "]")

    webform = TableSizeForm(request.form)

    if request.method == "POST":  #  and webform.validate():
        logger.debug("request.form = %s", request.form)
        #request.form = ImmutableMultiDict([('table_rows', '4'), ('table_cols', '9'), ('number_of_single', '8'), ('number_of_double', 'sdf'), ('filename', 'asdf'), ('submit_button', 'create JSON')])

        try:
            x=int(request.form['table_rows'])
        except Exception as err:
            flash(str(err))
            return redirect(url_for("table_dimensions"))
        try:
            x=int(request.form['table_cols'])
        except Exception as err:
            flash(str(err))
            return redirect(url_for("table_dimensions"))
        try:
            x=int(request.form['number_of_single'])
        except Exception as err:
            flash(str(err))
            return redirect(url_for("table_dimensions"))
        try:
            x=int(request.form['number_of_sym_double'])
        except Exception as err:
            flash(str(err))
            return redirect(url_for("table_dimensions"))
        try:
            x=int(request.form['number_of_asym_double'])
        except Exception as err:
            flash(str(err))
            return redirect(url_for("table_dimensions"))

        return redirect(url_for("entry_types", 
                  num_rows=request.form['table_rows'],
                  num_cols=request.form['table_cols'],
                  num_single=request.form['number_of_single'],
                  num_sym_double=request.form['number_of_sym_double'],
                  num_asym_double=request.form['number_of_asym_double'],
                  filename=request.form['filename']))
        

    logger.info("[trace page end " + trace_id + "]")
    return render_template("table_dimensions.html", 
                           webform=webform)


@app.route("/entry_types/<num_rows>/<num_cols>/<num_single>/<num_sym_double>/<num_asym_double>/<filename>", methods=["GET", "POST"])
def entry_types(num_rows, num_cols, num_single, num_sym_double, num_asym_double, filename):
    """
    step 2: what goes in the table?
    """
    trace_id = str(random.randint(1000000, 9999999))
    logger.info("[trace page start " + trace_id + "]")

    if request.method == "POST":  #  and webform.validate():
        logger.debug("request.form = %s", request.form)


    logger.info("[trace page end " + trace_id + "]")
    return render_template("entry_types.html",
                num_single=num_single,
                num_double=num_double)


@app.route("/table_content/<num_rows>/<num_cols>/<num_single>/<num_sym_double>/<num_asym_double>/<filename>", methods=["GET", "POST"])
def table_content(num_rows, num_cols, num_single, num_sym_double, num_asym_double, filename):
    """
    step 3: table content
    """
    trace_id = str(random.randint(1000000, 9999999))
    logger.info("[trace page start " + trace_id + "]")

    if request.method == "POST":  #  and webform.validate():
        logger.debug("request.form = %s", request.form)


    logger.info("[trace page end " + trace_id + "]")
    return render_template("table_content.html")


if __name__ == "__main__":
    # this is only applicable for flask (and not gunicorn)
    app.run(debug=True, host="0.0.0.0")
