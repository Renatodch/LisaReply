import subprocess
import sys

def main(args):
    if args[0] == '1':
        try:
            print("Iniciando servidor web")
            subprocess.call(["python", "webproject/manage.py", "runserver"])
        except:
            print("SHUTTING WEB SERVER...")
    elif args[0] == '2':
        print("Iniciando proceso de extracción de datos de congresista")
        subprocess.call(['python', './scraping/congresista.py'])
        
    elif args[0]=='3':
        print("Iniciando proceso de extracción de datos de proyectos de congresista")
        subprocess.call(['python', './scraping/proyecto.py'])

    elif args[0] == '4':
        print("Iniciando proceso de preparación de datos de congresistas y proyectos")
        subprocess.call(['python', './scraping/data_prepare.py'])

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)