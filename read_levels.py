import pygame
import csv


def get_level(id):
    with open('data/levels.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = list(next(reader))
        for i, r in enumerate(reader):
            if i == id:
                return {el[0]: el[1] for el in zip(headers, r)}
