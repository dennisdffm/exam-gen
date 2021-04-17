import docx
import yaml
import sys

archivo = sys.argv[1]

document = docx.Document('./Templates/base_nj.docx')

# f = open('./Otros/test.yaml', 'r', encoding='utf-8')
f = open(archivo, 'r', encoding='utf-8')
examen = yaml.safe_load(f)
f.close()

# For new document (document-wide):
# Set language value in the documents' default Run's Properties element.
styles_element = document.styles.element
rpr_default = styles_element.xpath('./w:docDefaults/w:rPrDefault/w:rPr')[0]
lang_default = rpr_default.xpath('w:lang')[0]
lang_default.set(docx.oxml.shared.qn('w:val'), 'es-ES')

# Escribir contenido en el template
for key, value in examen.items():
    if key.count('info'):
        # Mejorar, iterar a traves de los parrafos y buscar en cada objeto run para reemplazar
        encabezado = document.paragraphs

        asignatura = encabezado[0].runs[0]
        asignatura.text = value['asignatura']

        # Agregar opcion de fecha automatica o patrón de fechas
        fecha = encabezado[2].runs[1]
        fecha.text = value['fecha']

        curso = encabezado[2].runs[7]
        curso.text = value['curso']

        prof = encabezado[2].runs[12]
        prof.text = value['prof']

        tipo = encabezado[3].runs[2]
        tipo.text = value['tipo_examen']

        puntos = encabezado[4].runs[1]
        puntos.text = value['puntos']

    if key.count('Tema '):
        document.add_heading(key, level=2)
        # Se espera una lista con los subtemas
        for k, subtema in enumerate(value):
            # Cada subtema tendrá 'tipo' y 'contenido'
            if subtema['tipo'] == 'sel-m':
                # Se espera que contenido tenga 'Enunciado' y 'Opciones'
                document.add_paragraph(
                    subtema['contenido']['Enunciado'], style='Normal')

                for k, opcion in enumerate(subtema['contenido']['Opciones']):
                    document.add_paragraph(opcion, style='List Bullet')

            elif subtema['tipo'] == 'v-f':
                # Se espera que contenido tenga 'Enunciado' y 'Items'
                document.add_paragraph(
                    subtema['contenido']['Enunciado'], style='Normal')

                for k, item in enumerate(subtema['contenido']['Items']):
                    document.add_paragraph(
                        item + ' [V] [F]\n\n', style='List Bullet')

            elif subtema['tipo'] == 'cita':
                # Se espera que contenido tenga 'Enunciado' y 'Cantidad'
                document.add_paragraph(
                    subtema['contenido']['Enunciado'], style='Normal')

                aux = document.add_paragraph()
                for k in range(subtema['contenido']['Cantidad']):
                    # document.add_paragraph(str(k+1) + '- ', style='Normal')
                    aux.add_run(str(k+1) + '- \t\t\t')


document.save('./test.docx')
