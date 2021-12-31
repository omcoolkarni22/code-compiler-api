import subprocess
import os
from flask import Flask, jsonify
import random
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import string

app = Flask(__name__)
api = Api(app)
# cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()


# Checks if Return Code of Process is 0 or 1
# 0 means successful, 1 means error
def r_code(arg):
    return True if arg.returncode == 0 else False


class ExecuteCPP:
    """This class is used for Execution of C++ Codes."""

    def __init__(self, filename, custom_input, timeout):
        self.filename = filename  # File Name
        self.custom_input = custom_input  # Input to script
        self.timeout = timeout  # Timeout, quits execution if timeout exceeds
        self.outfile = self.filename[:-3] + 'out'  # .out file name

    def execute(self):
        error_check = subprocess.run(["g++", self.filename, '-o', self.outfile],
                                     capture_output=True,
                                     timeout=self.timeout
                                     )  # Compiles .cpp file and generates the .out file if no compilation error found

        if r_code(error_check):  # No compilation error found
            try:
                process = subprocess.run(
                    ['./' + self.outfile],
                    input=self.custom_input,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    text=True,
                    timeout=self.timeout
                )  # Execute .out file and check for run time error

                if r_code(process):  # No run time error
                    os.remove('./' + self.outfile)  # Delete the .out file
                    return process.stdout, process.returncode, False  # Return stdout and Return Code of code
                else:  # If run time error
                    return process.stderr, process.returncode, False

            except subprocess.TimeoutExpired:  # If code gets terminated by timeout error
                os.remove('./' + self.outfile)  # Removes the out file even if it's timeout error
                return '', 1, True

        else:  # Compilation error found
            return error_check.stderr.decode(), error_check.returncode, False

    # As the object gets deleted it will delete the .cpp file
    def __del__(self):
        os.remove('./' + self.filename)


class ExecuteC:
    """This class is used for Execution of C Codes."""

    def __init__(self, filename, custom_input, timeout):
        self.filename = filename
        self.timeout = timeout
        self.custom_input = custom_input
        self.outfile = self.filename[:-1] + 'out'

    def execute(self):
        error_check = subprocess.run(["gcc", self.filename, "-o", self.outfile],
                                     capture_output=True,
                                     timeout=self.timeout)
        if r_code(error_check):
            try:
                p = subprocess.run(['./' + self.outfile], input=self.custom_input, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   text=True, timeout=self.timeout)
                if r_code(p):
                    os.remove('./' + self.outfile)
                    return p.stdout, p.returncode, False
                else:
                    return p.stderr, p.returncode, False
            except subprocess.TimeoutExpired:
                os.remove('./' + self.outfile)
                return '', 1, True
        else:
            return error_check.stderr.decode(), error_check.returncode, False

    def __del__(self):
        os.remove('./' + self.filename)


class ExecuteJava:
    pass


class ExecutePython:
    """ This class is used for execution of Python3 codes. """

    def __init__(self, filename, custom_input, timeout):
        self.filename = filename
        self.timeout = timeout
        self.custom_input = custom_input

    def execute(self):
        try:
            process = subprocess.run(['python', self.filename], input=self.custom_input, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True, timeout=self.timeout)

            if r_code(process):
                return process.stdout, process.returncode, False
            else:
                return process.stderr, process.returncode, False

        except subprocess.TimeoutExpired:
            return '', 1, True

    def __del__(self):
        os.remove('./' + self.filename)


class Home(Resource):
    @staticmethod
    def get_file_name(file_type, extension, source):
        # This static function generates random filename and writes code to it then returns filename

        name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=5))
        filename = file_type + name + extension
        with open(filename, 'w+') as file:
            file.write(source)
        return filename

    def post(self):
        parser.add_argument('source', type=str)
        parser.add_argument('language', type=str)
        parser.add_argument('testcases', type=str)
        parser.add_argument('timeout', type=int)
        args = parser.parse_args()

        source = args['source']
        language = args['language']
        timeout = args['timeout']
        testcases = args['testcases']

        # If language is python
        if language == 'PYTHON':
            filename = self.get_file_name(file_type='PYTHON', extension='.py', source=source)
            python_object = ExecutePython(filename, testcases, timeout)
            output, return_code, timeout_error = python_object.execute()

        # if it's cpp
        elif language == 'CPP':
            filename = self.get_file_name(file_type='C++', extension='.cpp', source=source)
            cpp_object = ExecuteCPP(filename=filename, custom_input=testcases, timeout=timeout)
            output, return_code, timeout_error = cpp_object.execute()

        # if it's C
        elif language == 'C':
            filename = self.get_file_name(file_type='C', extension='.c', source=source)
            c_object = ExecuteC(filename, testcases, timeout)
            output, return_code, timeout_error = c_object.execute()

        # if language is not among above or we don't support it
        else:
            return jsonify({
                "Request Status Code": 204,
                "Output": "Support for {} language will be added soon!!!".format(language)
            })

        return_json = {
            "Request Status Code": 200,
            "Input": {
                "source": source,
                "language": language,
                "testcases": testcases,
                "timeout": timeout
            },
            "Output": {
                "stdout": output,
                "ReturnCode": return_code,
                "timeoutError": timeout_error
            }
        }
        return jsonify(return_json)


# Add home class to resource
api.add_resource(Home, '/execute/v2/')

if __name__ == '__main__':
    app.run(debug=True)
