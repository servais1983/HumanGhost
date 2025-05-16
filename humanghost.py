#!/usr/bin/env python3

import argparse
from core import create, send, host
from core.utils import run_script_yaml

def main():
    parser = argparse.ArgumentParser(prog="humanghost", description="Social Engineering CLI - Kali Linux")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("create", help="Création d'un scénario social")
    subparsers.add_parser("send", help="Envoi de l'attaque")
    subparsers.add_parser("host", help="Lance le faux site")
      
    run_cmd = subparsers.add_parser("run")
    run_cmd.add_argument("file")

    args = parser.parse_args()

    if args.command == "create":
        create.run()
    elif args.command == "send":
        send.run()
    elif args.command == "host":
        host.run()
    elif args.command == "run":
        run_script_yaml(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()