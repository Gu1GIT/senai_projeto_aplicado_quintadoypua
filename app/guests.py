from datetime import datetime
from flask import abort, make_response, redirect, render_template
from flask import Blueprint, jsonify, request
from markupsafe import escape

from app.data.dao.guest_dao import GuestDAO
from app.data.database.db import get_db
from app.domain.Guests import Guest, GuestDTO

bp = Blueprint('guests', __name__, url_prefix='/hospedes')

@bp.get('/')
def hospedes():
    db = get_db()
    guest_dao = GuestDAO(db)
    guests = guest_dao.find_many()

    guests = list(map( lambda guest: guest.to_dict(), guests))
    return jsonify(guests)
    # return render_template('cadastroHospedes.html', guests=guests) # Retorna um JSON com os dados, deve retornar um render_page com a pagina que lista todos os registros.


@bp.post('/cadastro')
def cria_hospede():
    if request.form is None:
        abort(400)

    guest_dto: GuestDTO = {
        'document': request.form['document'],
        'name': request.form['name'],
        'surname': request.form['surname'],
        'country': request.form['country'],
        'phone': request.form['phone'],
        'created_at': None
    }

    guest =  Guest(guest_dto)

    db = get_db()
    guest_dao = GuestDAO(db)
    guest_dao.insert(guest)
    return 'CREATED', 201


@bp.get('/<document>')
def hospede(document):
    db = get_db()
    guest_dao = GuestDAO(db)
    url_param = escape(document)
    guest = guest_dao.find(str(url_param))
    if guest is None:
        abort(404)
    return jsonify(guest.to_dict())


@bp.delete('/<document>')
# deve deletar um hospede
def deletar_hospede(document):
    db = get_db()
    guest_dao = GuestDAO(db)
    url_param = escape(document)
    exists = guest_dao.find(str(url_param))
    if not exists:
        abort(404)
    guest_dao.delete(url_param)
    return 'DELETED', 200


@bp.put('/')
def atualizar_hospede():
# deve atualizar hospede
    db = get_db()
    guest_dao = GuestDAO(db)

    if request.form['document'] is None or request.form['document'] == '':
        abort(400)

    exists = guest_dao.find(request.form['document'])

    if not exists:
        abort(404)

    guest_dto: GuestDTO = {
        'document': request.form['document'],
        'name': request.form['name'],
        'surname': request.form['surname'],
        'country': request.form['country'],
        'phone': request.form['phone'],
        'created_at': exists.created_at
    }
    guest = Guest(guest_dto)
    guest_dao.update(guest)
    return 'UPDATED', 200

@bp.get('/list')
def list():
        
    # Connect to the SQLite3 datatabase and 
    # SELECT  Rows from the guest table.
    db = get_db()
    guest_dao = GuestDAO(db)
    rows = guest_dao.find_many()

    
    # Send the results of the SELECT to the list.html page
    return render_template("list.html", rows=rows)   