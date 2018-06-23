import xml.etree.cElementTree as ET
import pandas
import csv
from openpyxl import load_workbook
from random import randint
from datetime import datetime
from xml.etree import ElementTree
from xml.dom import minidom

#todo
#csv
#adicionar arquivos em pasta
###############################


###CSV######
#cnesfile = open("cnes.csv", newline='')
#cnesList = list(csv.reader(cnesfile))
#tipofile = open("tipo.csv")
#tipoList = list(csv.reader(tipofile))

####Excel#######
wb = load_workbook('bd.xlsx')
cnes = wb["CNES"]
tipo = wb["Tipo"]
qtdLeitos = 50
qtdArquivos = 1000

for i in range(qtdArquivos):
	leito = ET.Element("leito", id=str(randint(1,qtdLeitos)))
	header = ET.SubElement(leito, "header")

	ET.SubElement(header, "nivel").text = "2"
	ET.SubElement(header, "referencia").text = "CNES_GENERICO"
	ET.SubElement(header, "cnes").text = str(cnes.cell(row=randint(1,782), column=1).value)
	ET.SubElement(header, "date").text = str(datetime.now())

	ET.SubElement(leito, "area").text = "area/subarea/subsubarea..."
	ET.SubElement(leito, "tipo").text = str(tipo.cell(row=randint(1,7), column=1).value)
	ET.SubElement(leito, "estado").text = str(randint(1,4))

	tree = ET.ElementTree(leito)
	filename = "xmlfiles/file" + str(i) + ".xml"
	tree.write(str(filename), encoding='utf-8', xml_declaration=True)
	print(i)
	
	
	#xmlfileGenerated = ET.parse(filename) 
	#root = xmlfileGenerated.getroot()
	#xml_str = ElementTree.tostring(root).decode()
	#xml_str_encoded = "<?xml version='1.0' encoding='utf-8'?>" + xml_str
	
	#string = ElementTree.tostring(xmlfileGenerated) 
	#print(xmlfileGenerated)
	#fd = open('xmlfiles.csv','a')
	#fd.write(xml_str_encoded)
	#fd.close()
#, encoding="us-ascii", method="xml", *, short_empty_elements=True))
