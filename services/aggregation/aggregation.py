from flask import Flask, request, redirect, url_for, flash
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

        return '{}, {}'.format(hb.getId(), hb.getHeaderField('cnes'))
    else:
        query = '''WITH id_leito_tb_leito AS(

        INSERT INTO tb_leito(id_estado_leito, id_estabelecimento_saude, area, id_leito_unidade) VALUES 
        ({}, (SELECT id_estabelecimento_saude FROM tb_estabelecimento_saude WHERE cod_cnes = {}), '{}', {}) RETURNING id_leito

        )
        INSERT INTO tb_classificacao(id_referencia, id_leito, id_tipo_ref) VALUES
        ((SELECT id_referencia FROM tb_referencia WHERE descricao = 'CNES_GENERICO'), 
        (SELECT id_leito FROM id_leito_tb_leito), {})'''.format(hb.getStatus(), hb.getHeaderField('cnes'), hb.getArea(), hb.getId(), hb.getType())

        db.execute(query)
        
        return 'Data inserted.'

    return hb.id

@app.route('/getHospitalBedsFromCNES/<int:cod_cnes>', methods=['GET'])
def getHospitalBedsFromCNES(cod_cnes):

    query = '''SELECT array_to_json(array_agg(row_to_json(j))) FROM (
        SELECT US.cod_cnes, L.* FROM tb_estabelecimento_saude US
        JOIN tb_leito L ON(L.id_estabelecimento_saude=US.id_estabelecimento_saude)
        WHERE US.cod_cnes = {}
        ) j'''.format(cod_cnes)
    
    r = db.query(query)
    
    return str(r[0][0])