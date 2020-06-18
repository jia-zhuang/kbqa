import re
import copy
import requests
import json

import jieba.posseg as posseg
from jieba import suggest_freq

from refo import finditer, Predicate, Plus

from config import QUERY, prefix


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos
    
    def __repr__(self):
        return '<{}|{}>'.format(self.token, self.pos)


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            return self.action(sentence[i:j])


def who_is_question(phrase):
    query_str = None
    for w in phrase:
        if w.pos == 'nr':
            query_str = '''
                {prefix}

                SELECT ?des
                WHERE {{
                    VALUES ?p {{:name :alias}}
                    ?s ?p "{mention}" .
                    ?s :description ?des .
                }}
            '''.format(prefix=prefix, mention=w.token)
    return query_str


# custom rules
person = (W(pos='nr') | W(pos='x'))

rules = [
    Rule(condition=W(pos='r') + W('是') + person | person + W('是') + W(pos='r'),
         action=who_is_question),
]

def query(question):
    words = posseg.cut(question)
    seg_list = [Word(w, p) for w, p in words]
    for rule in rules:
        query_str = rule.apply(seg_list)
        
        if query_str is not None:
            headers = {
                'Content-Type': 'application/sparql-query', 
                'Accept': 'application/json'
            }
            r = requests.post(QUERY, data=query_str.encode('utf-8'), headers=headers)
            if r.status_code == 200:
                return json.loads(r.content.decode('utf-8'))


def format_paragraph_output(json_data):
    res = []
    var_name = json_data['head']['vars'][0]
    for para in json.loads(json_data['results']['bindings'][0][var_name]['value']):
        res.append(para['text'])
    return '\n'.join(res)

if __name__ == '__main__':
    print(format_paragraph_output(query('杨幂是谁？')))
    print(format_paragraph_output(query('大幂幂是谁？')))