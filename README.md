# Code Compiler API - Documentation
**Introduction:**<br>
The Code Compiler API is developed for the developer community and can be used to build online code compilers. This can be used with any Frontend Technology.<br>
Currently, the API supports three languages mainly __C, C++, and Python__. The support for other languages will be added soon.<br>
The REST-API is built using the combination of the latest technologies named __Python, Flask, Flask-Restful API, subprocess, and OOPS concepts__.<br>
The production version is deployed to __Heroku__ and can be accessed at [here](https://flask-compiler-api.herokuapp.com).<br>
<br>

**Using API:**<br>
1. The API uses __POST method__ for code compilation and the endpoint for compilation is https://flask-compiler-api.herokuapp.com/execute/v2/.
2. The data required for compilation is __source code, language, input, and timeout__.
3. You must name languages in this format _C-> C, C++ -> CPP_ and _Python -> PYTHON_ while sending a request.
4. The datatypes of the post data must be _source: str, language: str, input: str_ and _timeout: int_.
5. Ex: {source: 'a = input()\nprint(a)', language: 'PYTHON', input: '5', timeout: 10}
6. I recommend using Postman for sending the requests. 

**Installing in your Local System:**
1. The installation is only supported on Linux Based Machines and doesn't support Windows OS.
2. [Python](https://www.python.org/downloads/) must be installed in order to execute the API. Clone the repo using _git clone https://github.com/omcoolkarni22/compiler-api.git_.
3. Install the requirements.txt file using command _pip install -r requirements.txt_(pip must be installed).
4. Once you are ready with installed requirements, you can directly execute _python app.py_ or use flask environment variable _export FLASK_APP=app_ and _flask run_.
5. the above command will start a development server on localhost port: 5000 and the app will be ready for use.

**P.S.:** <br>
1. GET methods are not supported by any means.
2. You can add more languages of your choice.
