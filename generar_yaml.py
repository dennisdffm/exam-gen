import sys
path = sys.argv[0]
path = path[:path.rfind('\\')]
while True:
    nombre = input('Nombre para el examen:')
    nombre += '.yaml'
    try:
        f = open(nombre, 'x')
        f.write('# Genera un encabezado y al menos un tema.\n')
        f.write('# Puedes generar un encabezado escribiendo "enc" y presionando "CTRL + ESPACIO".\n')
        f.write('# Luego, puedes generar temas escribiendo "tem" y presionando "CTRL + ESPACIO".\n')
        f.close()
        from subprocess import check_output
        comando = 'code ' + path
        check_output(comando, shell=True)
        comando = 'code ' + nombre
        check_output(comando, shell=True)
        break
    except FileExistsError:
        print('Ya existe un archivo con ese nombre. Escoge otro...')