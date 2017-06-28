#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - cyj <chenyijiethu@gmail.com>
# Date: 17-6-24
# File: test.py
from AI import AI
import random


def main():
    ai_1 = AI(str(random.randint(1, 100000)))
    ai_2 = AI(str(random.randint(1, 100000)))
    i = 1
    print(i,':', end='')
    result = ai_1.play('', first=True)
    print(result)
    while True:
        i = i+1
        print(i, ':', end='')
        result = ai_2.play(result)
        print(result)
        i=i+1
        print(i, ':', end='')
        result = ai_1.play(result)
        print(result)

if __name__ == '__main__':
    main()
