#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import requests
import time

SECS = 30
URL = '<your deta micro url>'
# URL = 'http://localhost:8000'# for debug locally

def restart_by_name(name):
  print(f'restarting by name: {name}')
  os.system(f'shutdown -r -t 01 -f -m \\\\{name}')


def consume_tokens():
  response = requests.get(URL + '/tokens')
  data = json.loads(response.text)
  print(data)
  return data


def get_machine(token):
  response = requests.get(URL + '/machine?token=' + token)
  data = json.loads(response.text)
  return data


def main():
  while True:
    print('checking tokens')
    tokens = consume_tokens()
    for token in tokens:
      try:
        token_value = token['token']
        name = get_machine(token_value)
        if name:
          restart_by_name(name)
      except:
        print('valid token not found, run again in 120 secs')
    time.sleep(SECS)

""" define main """
if __name__ == '__main__':
  main()
