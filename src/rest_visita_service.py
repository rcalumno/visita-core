from collections import namedtuple

from flask import Flask, abort, request

from visita_engine import VisitaEngine

app = Flask(__name__)

FileDto = namedtuple('FileDto', 'filename filetype fileMonth sheet value ruta ')


def convert_input_to(class_):
    def wrap(f):
        def decorator(*args):
            obj = class_(**request.get_json())
            return f(obj)

        return decorator

    return wrap


@app.route('/procesararchivo', methods=['POST'])
@convert_input_to(FileDto)
def do_something(fileDto):
    if not request.json:
        abort(400)

    print(fileDto)

    VisitaEngine.getInstance().leer_achivo(fileDto.ruta)
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)