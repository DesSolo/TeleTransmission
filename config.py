from yaml import load

with open('config.yml') as file:
    config = load(file.read())