from flask import Flask, render_template, request
import requests
import hashlib
#import sys

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def index():
    output = None
    if(request.method=="POST"):
        password = request.form['password']
        output = check(password)
    return render_template('index.html', output=output)



def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count(hashes, hash_to_text):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_text:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    #print(response)
    return get_password_leaks_count(response, tail)

# def main(args):
#     for password in args:
#         count = pwned_api_check(password)
#         if count:
#             response = f"{password} was found {count} times,  you should change your password."
#         else:
#             response = f'{password} was not found, carry on'

#     return response


def check(password):
    count = pwned_api_check(password)
    if count:
        response = f"{password} was found {count} times,  you should change your password."
    else:
        response = f'{password} was not found, carry on'

    return response
# if __name__ == '__main__':
#     sys.exit(main(sys.argv[1:]))