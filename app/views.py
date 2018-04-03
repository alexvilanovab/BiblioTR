from app import app, db, basedir
from forms import LoginForm, RegisterForm, VerifyForm, editUserForm, deleteUserForm, searchTDRForm, searchUserForm
from models import User
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import text
import os


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear_perfil', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        existing_user_username = User.query.filter_by(username=form.username.data).first()
        existing_user_email = User.query.filter_by(email=form.email.data).first()

        if existing_user_username or existing_user_email:
            if existing_user_username:
                flash("Ja existeix un usuari amb aquest nom d'usuari")

            if existing_user_email:
                flash("Ja existeix un usuari amb aquest correu")
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')

            user_new = User(
                name = form.name.data,
                bio = form.bio.data,
                username = form.username.data,
                email = form.email.data,
                tdr_title = form.tdr_title.data,
                tdr_description = form.tdr_description.data,
                tdr_subject = form.tdr_subject.data,
                tdr_year = form.tdr_year.data,
                password = hashed_password,
                creation_date = datetime.now()
            )

            tdr_file = request.files['tdr_file']

            if os.path.splitext(tdr_file.filename)[1][1:] != 'pdf':
                flash("El fitxer ha de ser un PDF")

                return render_template('register.html', form=form)

            tdr_file.save(basedir + '/static/tdr-pdf/' + user_new.username + '.pdf')

            db.session.add(user_new)
            db.session.commit()

            login_user(user_new, remember=form.remember.data)

            return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/iniciar_sessió', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user_email = User.query.filter_by(email=form.email_username.data).first()

        if user_email:
            if check_password_hash(user_email.password, form.password.data):
                login_user(user_email, remember=form.remember.data)

                return redirect(url_for('index'))

        user_username = User.query.filter_by(username=form.email_username.data).first()

        if user_username:
            if check_password_hash(user_username.password, form.password.data):
                login_user(user_username, remember=form.remember.data)

                return redirect(url_for('index'))

        flash("Combinació de correu/usuari i contrasenya errònia")

    return render_template('login.html', form=form)

@app.route('/tancar_sessió')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))

@app.route('/usuari/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()

    if user == None:
        return render_template('error.html', error='user_not_found', username=username), 404

    return render_template('user.html', user=user)

@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def edit_user():
    formEdit = editUserForm()
    formDelete = deleteUserForm()

    if formEdit.submitEditUser.data and formEdit.validate():
        current_user.bio = formEdit.bio.data
        db.session.commit()

        return redirect(url_for('user', username=current_user.username))

    elif formDelete.submitDeleteUser.data and formDelete.validate():
        if check_password_hash(current_user.password, formDelete.password.data):
            os.remove('static/tdr-pdf/{0}.pdf'.format(current_user.username))

            db.session.delete(current_user)
            db.session.commit()

            return redirect(url_for('index'))

        flash("Contrasenya errònia")

    return render_template('edit_user.html', formEdit=formEdit, formDelete=formDelete)

@app.route('/treballs', methods=['GET', 'POST'])
def tdr():
    formTDR = searchTDRForm()
    formUser = searchUserForm()
    tdr_list = []

    if formTDR.submitSearchTDR.data and formTDR.validate():
        sql_conditions = []

        if formTDR.title.data != "":
            sql_conditions.append('tdr_title=:title')

        if formTDR.subject.data != "":
            sql_conditions.append('tdr_subject=:subject')

        if formTDR.year.data != "":
            sql_conditions.append('tdr_year=:year')

        if formTDR.verifiedOnly.data:
            sql_conditions.append('tdr_mark IS NOT NULL')

        sql = 'SELECT * FROM user'
        if len(sql_conditions) >= 1:
            sql += ' WHERE ' + ' AND '.join(sql_conditions)

        for user in db.engine.execute(text(sql)
            .params(
                title=formTDR.title.data,
                subject=formTDR.subject.data,
                year=formTDR.year.data
            )
        ):
            tdr_list.append({
                'username': user.username,
                'name': user.name,
                'title': user.tdr_title,
                'description': user.tdr_description,
                'subject': user.tdr_subject,
                'year': user.tdr_year,
                'mark': user.tdr_mark,
                'school': user.tdr_school
            })

    elif formUser.submitSearchUser.data and formUser.validate():
        user = User.query.filter_by(username=formUser.username.data).first()

        if user:
            tdr_list.append({
                'username': user.username,
                'name': user.name,
                'title': user.tdr_title,
                'description': user.tdr_description,
                'subject': user.tdr_subject,
                'year': user.tdr_year,
                'mark': user.tdr_mark,
                'school': user.tdr_school
            })

    else:
        for user in User.query:
            tdr_list.append({
                'username': user.username,
                'name': user.name,
                'title': user.tdr_title,
                'description': user.tdr_description,
                'subject': user.tdr_subject,
                'year': user.tdr_year,
                'mark': user.tdr_mark,
                'school': user.tdr_school
            })

    return render_template('tdr.html', tdr_list=tdr_list, formTDR=formTDR, formUser=formUser)

@app.route('/verificar', methods=['GET', 'POST'])
def verify():
    form = VerifyForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            if form.mantra.data == "secret":
                user.tdr_mark = int(form.mark.data)
                user.tdr_school = form.school.data
                db.session.commit()

                return redirect(url_for('verify'))

            else:
                flash("Aquest mantra no és vàlid")

        else:
            flash("No existeix cap usuari amb aquest correu")

    return render_template('verify.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='page_not_found'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('error.html', error='forbidden'), 403

@app.errorhandler(410)
def gone(e):
    return render_template('error.html', error='gone'), 410

@app.errorhandler(413)
def request_entity_too_large(e):
    return render_template('error.html', error='request_entity_too_large'), 413

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error='internal_server_error'), 500

@app.route('/error')
def login_required_error():
    return render_template('error.html', error='login_required_error')
