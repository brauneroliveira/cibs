from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from HospitalBed import HospitalBed
from XMLFile import XMLFile
import os, json
from db import db

app = Flask(__name__)
app.secret_key = 'd5581c21abc693c36798ae91ec69b5aa521c3755b95d63eb399df7ec69b5aa52'

@app.route('/persistHospitalBed', methods=['POST'])
def persistHospitalBed():
    requestxml = request.files['file']
    xmlfile = XMLFile(string=requestxml.read())

    hb = HospitalBed(xmlfile)

    query = '''SELECT L.id_leito FROM tb_leito L
        JOIN tb_estabelecimento_saude E ON(L.id_estabelecimento_saude=E.id_estabelecimento_saude)
        WHERE E.cod_cnes = {} AND
        L.id_leito_unidade = {}'''.format(hb.getHeaderField('cnes'), hb.getId())

    id_dbhb = db.query(query)

    if id_dbhb:
     
        query = '''UPDATE tb_leito SET id_estado_leito = {}, area = '{}' 
        WHERE id_leito = {}'''.format(hb.getStatus(), hb.getArea(), id_dbhb[0][0])

        db.execute(query)

        return 'Leito já existente. Atualizando dados.'
    else:
        query = '''WITH id_leito_tb_leito AS(

        INSERT INTO tb_leito(id_estado_leito, id_estabelecimento_saude, area, id_leito_unidade) VALUES 
        ({}, (SELECT id_estabelecimento_saude FROM tb_estabelecimento_saude WHERE cod_cnes = {}), '{}', {}) RETURNING id_leito

        )
        INSERT INTO tb_classificacao(id_referencia, id_leito, id_tipo_ref) VALUES
        ((SELECT id_referencia FROM tb_referencia WHERE descricao = 'CNES_GENERICO'), 
        (SELECT id_leito FROM id_leito_tb_leito), {})'''.format(hb.getStatus(), hb.getHeaderField('cnes'), hb.getArea(), hb.getId(), hb.getType())

        db.execute(query)
        
        return 'Novo leito cadastrado.'

    return hb.id

@app.route('/getHospitalBedsFromCNES/<int:cod_cnes>', methods=['GET'])
def getHospitalBedsFromCNES(cod_cnes):

    query = '''SELECT array_to_json(array_agg(row_to_json(j))) FROM (
        SELECT US.cod_cnes, L.* FROM tb_estabelecimento_saude US
        JOIN tb_leito L ON(L.id_estabelecimento_saude=US.id_estabelecimento_saude)
        WHERE US.cod_cnes = {}
        ) j'''.format(cod_cnes)
    
    r = db.query(query)
    
    return jsonify(r[0][0])

@app.route('/getHealthcareEstablishments/<int:cod_ibge>', methods=['GET'])
def getHealthCareEstablishments(cod_ibge):

    query = '''SELECT array_to_json(array_agg(row_to_json(j))) FROM (
        SELECT ES.id_estabelecimento_saude, ES.nome_fantasia AS "nome", ES.cod_cnes, M.cod_ibge, M.nome AS "cidade", ES.lat, ES.lng FROM tb_estabelecimento_saude ES
        JOIN tb_municipio M ON(ES.id_municipio=M.id_municipio)
        WHERE M.cod_ibge = {} AND ES.lat IS NOT NULL
    ) j'''.format(cod_ibge)
    
    r = db.query(query)

    if r:
        return jsonify(r[0][0])

@app.route('/getMunicipiosFromRS/<int:cod_reg_saude>', methods=['GET'])
def getMunicipiosFromRS(cod_reg_saude):

    query = '''SELECT array_to_json(array_agg(j)) FROM (
        SELECT M.cod_ibge, M.nome FROM tb_municipio M
        WHERE M.id_reg_saude = {}
        ) j'''.format(cod_reg_saude)
    
    r = db.query(query)
    
    if r:
        response = jsonify(r[0][0])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/getAVailableHospitalBedsByRRAS/', methods=['GET'])
def getHospitalBedOccupiedByRRAS():

    query = '''SELECT array_to_json(array_agg(row_to_json(j))) FROM (
        SELECT RR.id_rras, count(L.id_estado_leito) AS "qtde_disponivel" FROM tb_rras RR
        JOIN tb_regsaude RS ON(RR.id_rras=RS.id_rras)
        JOIN tb_municipio M ON(M.id_reg_saude=RS.id_reg_saude)
        JOIN tb_estabelecimento_saude ES ON(ES.id_municipio=M.id_municipio)
        JOIN tb_leito L ON(L.id_estabelecimento_saude=ES.id_estabelecimento_saude)
        WHERE L.id_estado_leito=0
        GROUP BY RR.id_rras
        )j'''

    r = db.query(query)

    response = jsonify(r[0][0])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAvailableHospitalBedsByES/<int:id_estabelecimento_saude>', methods=['GET'])
def getAvailableHospitalBedsFromES(id_estabelecimento_saude):

    query = '''SELECT array_to_json(array_agg(j)) FROM (
        SELECT count(L.id_leito) AS "disp" FROM tb_leito L
        JOIN tb_estabelecimento_saude ES ON(L.id_estabelecimento_saude=ES.id_estabelecimento_saude)
        WHERE L.id_estado_leito=0 AND
        ES.id_estabelecimento_saude={}
        )j'''.format(id_estabelecimento_saude)

    r = db.query(query)

    response = jsonify(r[0][0])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAvailableHospitalBedsFromRRAS/<int:id_rras>', methods=['GET'])
def getAvailableHospitalBedsFromRRAS(id_rras):

    query = '''SELECT count(L.id_estado_leito) AS "qtde_disponivel" FROM tb_rras RR
        JOIN tb_regsaude RS ON(RR.id_rras=RS.id_rras)
        JOIN tb_municipio M ON(M.id_reg_saude=RS.id_reg_saude)
        JOIN tb_estabelecimento_saude ES ON(ES.id_municipio=M.id_municipio)
        JOIN tb_leito L ON(L.id_estabelecimento_saude=ES.id_estabelecimento_saude)
        WHERE RR.id_rras = {} AND
        L.id_estado_leito=0
        GROUP BY RR.id_rras'''.format(id_rras)

    r = db.query(query)
    
    if r:
        response = jsonify(r[0][0])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = jsonify(0)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/getTotalNumberOfHospitalBedsFromRRAS/<int:id_rras>', methods=['GET'])
def getTotalNumberOfHospitalBedsFromRRAS(id_rras):

    query = '''SELECT count(L.id_estado_leito) AS "qtde_disponivel" FROM tb_rras RR
        JOIN tb_regsaude RS ON(RR.id_rras=RS.id_rras)
        JOIN tb_municipio M ON(M.id_reg_saude=RS.id_reg_saude)
        JOIN tb_estabelecimento_saude ES ON(ES.id_municipio=M.id_municipio)
        JOIN tb_leito L ON(L.id_estabelecimento_saude=ES.id_estabelecimento_saude)
        WHERE RR.id_rras = {}
        GROUP BY RR.id_rras'''.format(id_rras)

    r = db.query(query)

    if r:
        response = jsonify(r[0][0])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/getHealthcareEstablishmentsFromRS/<int:id_reg_saude>', methods=['GET'])
def getHealthcareEstablishmentsFromRS(id_reg_saude):

    query = '''SELECT array_to_json(array_agg(row_to_json(j))) FROM (
        SELECT RS.id_reg_saude, ES.nome_fantasia, ES.lat, ES.lng FROM tb_regsaude RS
        JOIN tb_municipio M ON(M.id_reg_saude=RS.id_reg_saude)
        JOIN tb_estabelecimento_saude ES ON(ES.id_municipio=M.id_municipio)
        WHERE RS.id_reg_saude = {}
        )j
        '''.format(id_reg_saude)
    
    r = db.query(query)

    if r:
        response = jsonify(r[0][0])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response