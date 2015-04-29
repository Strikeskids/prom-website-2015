#!/usr/bin/env python3

import api
import os
import yaml
import itertools

def main():
    import argparse

    parser = argparse.ArgumentParser('qload', 'Question loader')

    parser.add_argument('-l','--location', 
        dest='location', type=str, action='store', help='Directory where questions are loaded', default='../web/_posts/')

    args = parser.parse_args()

    for fname in os.listdir(args.location):
        fname = os.path.join(args.location, fname)
        if os.path.isfile(fname):
            try:
                with open(fname, 'r') as f:
                    it = iter(f)
                    if next(it) != '---\n':
                        continue
                    doc = yaml.load(''.join(itertools.takewhile(lambda k: k != '---\n', it)))
                    if 'question' in doc and 'answer' in doc and 'success' in doc and ('name' in doc or 'title' in doc):
                        num = doc['question']
                        name = doc['name'] if 'name' in doc else doc['title']
                        answer = doc['answer']
                        success = doc['success']
                        failure = doc['failure'] if 'failure' in doc else 0
                        print('Inserting', num, name, doc)
                        api.question.add_question(num, name, answer, success, failure)
            except:
                import traceback
                traceback.print_exc()

if __name__ == '__main__': main()