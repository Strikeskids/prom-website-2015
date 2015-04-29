#!/usr/bin/env python3

import api
import os
import yaml

def main():
    import argparse

    parser = argparse.ArgumentParser('qload', 'Question loader')

    parser.add_argument('-l','--location', 
        dest='location', type=str, action='store', help='Directory where questions are loaded', default='../web/_posts/')

    args = parser.parse_args()

    for fname in os.listdir(args.location):
        print(fname)
        if os.path.isfile(fname):
            try:
                with open(fname, 'r') as f:
                    doc = yaml.load(f)
                    if 'question' in doc and 'answer' in doc and 'success' in doc and ('name' in doc or 'title' in doc):
                        print('Inserting', doc)
                        num = doc['question']
                        name = doc['name'] if 'name' in doc else doc['title']
                        answer = doc['answer']
                        success = doc['success']
                        failure = doc['failure'] if 'failure' in doc else 0
                        api.question.add_question(num, name, answer, success, failure)
            except:
                import traceback
                traceback.print_exc()

if __name__ == '__main__': main()