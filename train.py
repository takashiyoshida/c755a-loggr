#!/usr/bin/env python

import argparse
import sys

class Train:
    def __init__(self, train_num, car_num, atc_car_num):
        self._train_num = train_num
        self._car_num = car_num
        self._atc_car_num = atc_car_num

    def __repr__(self):
        return "Train: %d, Car: %d, ATC Car: %d" % (self._train_num, self._car_num, self._atc_car_num)

DATA = [ {'train': 1, 'car': 1, 'atc': 257},
         {'train': 1, 'car': 2, 'atc': 256},
         {'train': 2, 'car': 3, 'atc': 261},
         {'train': 2, 'car': 4, 'atc': 260},
         {'train': 3, 'car': 5, 'atc': 265},
         {'train': 3, 'car': 6, 'atc': 264},
         {'train': 4, 'car': 7, 'atc': 269},
         {'train': 4, 'car': 8, 'atc': 268},
         {'train': 5, 'car': 9, 'atc': 273},
         {'train': 5, 'car': 10, 'atc': 272},
         {'train': 6, 'car': 11, 'atc': 277},
         {'train': 6, 'car': 12, 'atc': 276},
         {'train': 7, 'car': 13, 'atc': 281},
         {'train': 7, 'car': 14, 'atc': 280},
         {'train': 8, 'car': 15, 'atc': 285},
         {'train': 8, 'car': 16, 'atc': 284},
         {'train': 9, 'car': 17, 'atc': 289},
         {'train': 9, 'car': 18, 'atc': 288},
         {'train': 10, 'car': 19, 'atc': 293},
         {'train': 10, 'car': 20, 'atc': 292},
         {'train': 11, 'car': 21, 'atc': 297},
         {'train': 11, 'car': 22, 'atc': 296},
         {'train': 12, 'car': 23, 'atc': 301},
         {'train': 12, 'car': 24, 'atc': 300},
         {'train': 13, 'car': 25, 'atc': 305},
         {'train': 13, 'car': 26, 'atc': 304},
         {'train': 14, 'car': 27, 'atc': 309},
         {'train': 14, 'car': 28, 'atc': 308},
         {'train': 15, 'car': 29, 'atc': 313},
         {'train': 15, 'car': 30, 'atc': 312},
         {'train': 16, 'car': 31, 'atc': 317},
         {'train': 16, 'car': 32, 'atc': 316},
         {'train': 17, 'car': 33, 'atc': 321},
         {'train': 17, 'car': 34, 'atc': 320},
         {'train': 18, 'car': 35, 'atc': 325},
         {'train': 18, 'car': 36, 'atc': 324},
         {'train': 19, 'car': 37, 'atc': 329},
         {'train': 19, 'car': 38, 'atc': 328},
         {'train': 20, 'car': 39, 'atc': 333},
         {'train': 20, 'car': 40, 'atc': 332},
         {'train': 21, 'car': 41, 'atc': 337},
         {'train': 21, 'car': 40, 'atc': 336},
         {'train': 22, 'car': 43, 'atc': 341},
         {'train': 22, 'car': 44, 'atc': 340},
         {'train': 23, 'car': 45, 'atc': 345},
         {'train': 23, 'car': 46, 'atc': 344},
         {'train': 24, 'car': 47, 'atc': 349},
         {'train': 24, 'car': 48, 'atc': 348},
         {'train': 25, 'car': 49, 'atc': 353},
         {'train': 25, 'car': 50, 'atc': 352},
         {'train': 26, 'car': 51, 'atc': 385},
         {'train': 26, 'car': 52, 'atc': 384},
         {'train': 27, 'car': 53, 'atc': 389},
         {'train': 27, 'car': 54, 'atc': 388},
         {'train': 28, 'car': 55, 'atc': 393},
         {'train': 28, 'car': 56, 'atc': 392},
         {'train': 29, 'car': 57, 'atc': 397},
         {'train': 29, 'car': 58, 'atc': 396},
         {'train': 30, 'car': 59, 'atc': 401},
         {'train': 30, 'car': 60, 'atc': 400},
         {'train': 31, 'car': 61, 'atc': 405},
         {'train': 31, 'car': 62, 'atc': 404},
         {'train': 32, 'car': 63, 'atc': 409},
         {'train': 32, 'car': 64, 'atc': 408},
         {'train': 33, 'car': 65, 'atc': 413},
         {'train': 33, 'car': 66, 'atc': 412},
         {'train': 34, 'car': 67, 'atc': 417},
         {'train': 34, 'car': 68, 'atc': 416},
         {'train': 35, 'car': 69, 'atc': 421},
         {'train': 35, 'car': 70, 'atc': 420},
         {'train': 36, 'car': 71, 'atc': 425},
         {'train': 36, 'car': 72, 'atc': 424},
         {'train': 37, 'car': 73, 'atc': 429},
         {'train': 37, 'car': 74, 'atc': 428},
         {'train': 38, 'car': 75, 'atc': 433},
         {'train': 38, 'car': 76, 'atc': 432},
         {'train': 39, 'car': 77, 'atc': 437},
         {'train': 39, 'car': 78, 'atc': 436},
         {'train': 40, 'car': 79, 'atc': 441},
         {'train': 40, 'car': 80, 'atc': 440},
         {'train': 41, 'car': 81, 'atc': 445},
         {'train': 41, 'car': 82, 'atc': 444},
         {'train': 42, 'car': 83, 'atc': 449},
         {'train': 42, 'car': 84, 'atc': 448},
         {'train': 43, 'car': 85, 'atc': 453},
         {'train': 43, 'car': 86, 'atc': 452} ]

def convert_text_to_num(text, is_hex=False):
    try:
        if is_hex:
            num = int(text, 16)
        else:
            num = int(text)
    except ValueError as e:
        print e
        num = None
    return num

def print_train_data(data):
    print "Train: %d Car: %d ATC Car: %d (%s)" % (data['train'], data['car'], data['atc'], hex(data['atc']))

def search_train_by_car(car):
    for train in DATA:
        if train['car'] == car:
            print_train_data(train)
            break

def search_train_by_atc_car(atc_car):
    for train in DATA:
        if train['atc'] == atc_car:
            print_train_data(train)
            break

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(prog='train.py')
    argparser.add_argument('-c', '--car', required=False, help='Physical car number', dest='car')
    argparser.add_argument('-a', '--atc-car', required=False, help='ATC car number', dest='atc')
    argparser.add_argument('-x', '--hex', action='store_true', required=False, help='ATC car number is hexadecimal', dest='hex')

    args = argparser.parse_args()

    if args.car:
        car = convert_text_to_num(args.car)
        if car:
            search_train_by_car(car)
    if args.atc:
        is_hex = False
        if args.hex:
            is_hex = True
        atc_car = convert_text_to_num(args.atc, is_hex)
        if atc_car:
            search_train_by_atc_car(atc_car)
