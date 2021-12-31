import requests
from pprint import pprint

# "s = int(input())\na = int(input())\n print(s//a)\n"

s = requests.post('https://flask-compiler-api.herokuapp.com/execute/v2/', json={
    "source": '''i = int(input())\nj = int(input())\nprint(i,j)''',
    "language": "PYTHON",
    "testcases": "10\n10",
    "timeout": 10
})

pprint(s.json())
