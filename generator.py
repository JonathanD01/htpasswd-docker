# Source https://prometheus.io/docs/guides/basic-auth/

import sys
import os
import argparse
import getpass
import bcrypt
from pathlib import Path
from shutil import rmtree

def init_parser():
    """ Init parser """
    parser = argparse.ArgumentParser(description='Configure the .htpasswd file')
    parser.add_argument("-f", "--file-name", help="Name of the file. Default is '.htpasswd'", default=".htpasswd")
    parser.add_argument("-u", "--user", help="The user for authentication")
    parser.add_argument("-p", "--password", help="The password for authentication")  
    parser.add_argument("-ph", "--path", help="The path where the file will be generated. Default is '/'", default="/")
    return parser


def validate_args(parser, args):
    """ Validate arguments exists """
    if not args.user or not args.password or not args.path:
        parser.print_help()
        sys.exit(1)
    elif not args.path.startswith("/"):
        print("The path must start with a /")
        sys.exit(1)
    else:
        print("User, password and path args are present... continuing")


def get_hashed_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def write_file(file_name, user, hashed_password, path):
    """ Write the htpasswd """
    path = os.path.join(os.getcwd() + path)
    p = Path(path)

    p.mkdir(parents=True, exist_ok=True)

    filepath = p / file_name
    with filepath.open("w", encoding="utf-8") as f:
        f.write("{}:{}".format(user, hashed_password.decode("utf-8")))
    
    print("Created {}".format(os.path.normpath(os.path.join(os.getcwd() + args.path, file_name))))


if __name__ == "__main__":

    parser = init_parser()

    args = parser.parse_args()

    validate_args(parser, args)

    file_name = args.file_name

    user = args.user

    hashed_password = get_hashed_password(args.password)

    write_file(file_name, user, hashed_password, args.path)
