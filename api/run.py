from api.app import config_app

def main():
    import argparse
    parser = argparse.ArgumentParser(description="picoCTF API configuration")

    parser.add_argument("-v", "--verbose", action="count", help="increase verbosity", default=0)

    parser.add_argument("-p", "--port", action="store", help="port the server should listen on.", type=int, default=8000)
    parser.add_argument("-l", "--listen", action="store", help="host the server should listen on.", default="0.0.0.0")
    parser.add_argument("-d", "--debug", action="store_true", help="run the server in debug mode.", default=False)

    args = parser.parse_args()

    config_app().run(host=args.listen, port=args.port, debug=args.debug)

if __name__ == '__main__': main()
