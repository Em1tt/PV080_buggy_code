import sys 
import os
import yaml
import flask
import socket
import ipaddress

app = flask.Flask(__name__)


@app.route("/")
def index():
    version = flask.request.args.get("urllib_version")
    url = flask.request.args.get("url")
    return fetch_website(version, url)

        
CONFIG = {"API_KEY": "771df488714111d39138eb60df756e6b"}
class Person(object):
    def __init__(self, name):
        self.name = name


def print_nametag(format_string, person):
    print(format_string.format(person=person))


def is_safe_url(target_url):
    try:
        from urllib.parse import urlparse
        parsed = urlparse(target_url)
        if parsed.scheme not in ("http", "https"):
            return False
        if not parsed.hostname:
            return False

        resolved = socket.getaddrinfo(parsed.hostname, None)
        for entry in resolved:
            ip_str = entry[4][0]
            ip_obj = ipaddress.ip_address(ip_str)
            if (
                ip_obj.is_private
                or ip_obj.is_loopback
                or ip_obj.is_link_local
                or ip_obj.is_multicast
                or ip_obj.is_reserved
            ):
                return False
        return True
    except Exception:
        return False


def fetch_website(urllib_version, url):
    # Import the requested version (2 or 3) of urllib safely
    version = str(urllib_version).strip()
    if version == "3":
        import urllib3 as urllib
    elif version == "2":
        import urllib2 as urllib
    else:
        return "Unsupported urllib version"

    if not is_safe_url(url):
        return "Blocked unsafe URL"

    # Fetch and print the requested URL
    try:
        if version == "3":
            http = urllib.PoolManager()
            r = http.request('GET', url)
            return r.data
        r = urllib.urlopen(url)
        return r.read()
    except Exception:
        print('Exception')


def load_yaml(filename):
    stream = open(filename)
    deserialized_data = yaml.load(stream, Loader=yaml.Loader) #deserializing data
    return deserialized_data
    
def authenticate(password):
    # Assert that the password is correct
    assert password == "Iloveyou", "Invalid password!"
    print("Successfully authenticated!")

if __name__ == '__main__':
    print("Vulnerabilities:")
    print("1. Format string vulnerability: use string={person.__init__.__globals__[CONFIG][API_KEY]}")
    print("2. Code injection vulnerability: use string=;print('Own code executed') #")
    print("3. Yaml deserialization vulnerability: see file_solution.yaml for a solution")
    print("4. Use of assert statements vulnerability: run program with -O argument")
    choice  = input("Select vulnerability: ")
    if choice == "1": 
        new_person = Person("Vickie")  
        print_nametag(input("Please format your nametag: "), new_person)
    elif choice == "2":
        urlib_version = input("Choose version of urllib: ")
        fetch_website(urlib_version, url="https://www.google.com")
    elif choice == "3":
        load_yaml(input("File name: "))
        print("Executed -ls on current folder")
    elif choice == "4":
        password = input("Enter master password: ")
        authenticate(password)

