#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - cyj <chenyijiethu@gmail.com>
# Date: 17-6-25
# File: AI.py

import os, time, sys
import gtp as gtp_lib
from policy import PolicyNetwork
from strategies import PolicyNetworkBestMovePlayer

STRING = 'abcdefghijklmnopqrstuvwxyz'
DEFAULT_AI_MOUDLE_FILE = './AI_FILE/savedmodel'


class AI(object):
    def __init__(self, game_id, mode=0, moudle_file=DEFAULT_AI_MOUDLE_FILE, debug=False):
        '''
        :param mode:
            mode==0 -> human vs AI
            mode==1 -> AI    vs AI
        :param game_id:
            string
        :param moudle_file:
            string
            the AI moudle file
        '''

        # Activate Logging Debug Information
        self.debug = debug

        # initialize
        self.game_id = game_id
        self.command_list = []

        if not (mode == 1 or mode == 0):
            raise Exception('Invalid Game Mode')
        else:
            self.mode = mode

        self.moudle_file = moudle_file

        try:
            n = PolicyNetwork(use_cpu=True)
            instance = PolicyNetworkBestMovePlayer(n, self.moudle_file)
            self.gtp_engine = gtp_lib.Engine(instance)
        except BaseException as e:
            raise Exception('Initialization of policy network failed')

        # TODO: Remove the code below if using remote database
        # Using path 'game_database/data/' to store game data.
        # Make sure the path exists !
        self.local_data_filepath = 'game_database/data/'

        self.data_file = self.local_data_filepath + self.game_id + '.data'

    def get_former_game_data(self):
        '''

        Read the game data from a local or remote database
        :return: former game data(gtp command in list)
        '''
        # remote database
        # TODO: write code to connect remote database
        #
        #


        # TODO: Remove the code below if using remote database
        # local database (using text file)

        if os.path.exists(self.data_file):
            f = open(self.data_file, 'r')
            self.command_list = f.readlines()
            f.close()
        else:
            f = open(self.data_file, 'w')
            f.close()
            self.command_list = []

    def write_game_data(self, current_command):
        '''
        write the current command to data base
        :param command:
        :return:
        '''
        # remote database
        # TODO: write code to connect remote database
        #
        #

        # TODO: Remove the code below if using remote database
        # local database (using text file)
        if current_command == '':
            return
        f = open(self.data_file, 'a')
        f.write(current_command+'\n')
        f.close()

    def restore_game_state(self):
        for command in self.command_list:
            command = command.strip('\n')
            if command == '':
                continue
            else:
                self.gtp_engine.send(command)

    def play(self, chess_message, first=False):
        '''

        :param chess_message:
        A string to describe the position of the piece IN SGF FORMAT
        example: 'W[aa]'
        :param first:

        :return:
        '''
        self.initialize()


        if self.debug:
            sys.stdout.write(time.asctime() + '\n')
            sys.stdout.flush()

        self.first = first

        if not first:

            x, y, color = self.parse_input_message(chess_message)
            # self.parse_input_message(chess_message)
            self.write_game_data(self.parse_player_input(color, x, y))


            if self.debug:
                sys.stdout.write(str(x) + ' ' + str(y) + ' ' + color + '\n')
                sys.stdout.flush()

            self.get_former_game_data()

            self.restore_game_state()

            if self.debug:
                sys.stdout.write(time.asctime() + '\n')
                sys.stdout.flush()

            if color == 'B':
                color = 'W'
            else:
                color = 'B'
            #change color to AI side

            return self.get_AI_reply(color)

        else:
            color = 'B'
            self.get_former_game_data()  # To create data file

            if self.debug:
                sys.stdout.write(time.asctime() + '\n')
                sys.stdout.flush()

            return self.get_AI_reply(color)

    def get_AI_reply(self, color):
        AI_cmd = self.parse_AI_instruction(color)
        gtp_reply = self.gtp_engine.send(AI_cmd)

        AI_x, AI_y = self.parse_AI_reply(gtp_reply)
        self.write_game_data(self.parse_AI_input(color, gtp_reply))

        response = color + '[' + AI_x + AI_y + ']'
        return response

    def parse_input_message(self, message):
        # get the letters of position
        x = message[2]
        y = STRING.index(message[3])
        color = ''

        # determine color(AI)
        if message[0] == 'B':
            color = 'B'
        else:
            color = 'W'

        # deal with the first of location that larger than 'i'
        if x >= 'i':
            x = STRING[STRING.index(x) + 1]

        # deal with the opposite allocation of vertical axis
        y = 19 - y
        return x, y, color

    def parse_AI_instruction(self, color):
        return "genmove " + color.upper()

    def parse_AI_input(self, color, gtp_reply):
        return "play " + color.upper() + ' ' + gtp_reply[2:]

    def parse_AI_reply(self, gtp_reply):
        AI_x = gtp_reply[2].lower()
        AI_y = int(gtp_reply[3:])

        if AI_x > 'i':
            AI_x = STRING[STRING.index(AI_x) - 1]

        AI_y = 19 - AI_y
        AI_y = STRING[AI_y]

        return AI_x, AI_y

    def parse_player_input(self, color, x, y):
        return "play " + color.upper() + ' ' + x.upper() + str(y)


    def initialize(self):
        try:
            n = PolicyNetwork(use_cpu=True)
            instance = PolicyNetworkBestMovePlayer(n, self.moudle_file)
            self.gtp_engine = gtp_lib.Engine(instance)
        except BaseException as e:
            raise Exception('Initialization of policy network failed')

