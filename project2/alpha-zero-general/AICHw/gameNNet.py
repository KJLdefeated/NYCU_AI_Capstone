import sys
sys.path.append('..')
from utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from positional_encodings.torch_encodings import PositionalEncoding2D

class gameNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args
        super(gameNNet, self).__init__()
        self.pos_enc = PositionalEncoding2D(1)
        self.transformer_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=144, nhead=144),
            num_layers=2
        )
        
        self.global_avg_pooling = nn.AdaptiveAvgPool1d(output_size=2048)
        
        self.dense1 = nn.Linear(2048, 2048)
        self.dense3 = nn.Linear(2048, 2048)
        self.dense2 = nn.Linear(2048, 12*12*13)
        self.output_layer = nn.Linear(2048, 1)
        
        self.conv1 = nn.Conv2d(1, args.num_channels, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)
        self.conv4 = nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)

        self.bn1 = nn.BatchNorm2d(args.num_channels)
        self.bn2 = nn.BatchNorm2d(args.num_channels)
        self.bn3 = nn.BatchNorm2d(args.num_channels)
        self.bn4 = nn.BatchNorm2d(args.num_channels)

        self.fc1 = nn.Linear(args.num_channels*(self.board_x-4)*(self.board_y-4), 4096)
        self.fc_bn1 = nn.BatchNorm1d(4096)

        self.fc2 = nn.Linear(4096, 2048)
        self.fc_bn2 = nn.BatchNorm1d(2048)

        self.fc3 = nn.Linear(2048, self.action_size)

        self.fc4 = nn.Linear(2048, 1)

    def forward(self, s):
        s = s.view(-1, 12, 12, 1)
        #s = s.view(-1, 1, self.board_x, self.board_y)
        #s = F.relu(self.bn1(self.conv1(s)))                          # batch_size x num_channels x board_x x board_y
        #s = F.relu(self.bn2(self.conv2(s)))                          # batch_size x num_channels x board_x x board_y
        #s = F.relu(self.bn3(self.conv3(s)))                          # batch_size x num_channels x (board_x-2) x (board_y-2)
        #s = s.view(-1, self.args.num_channels*(self.board_x-3)*(self.board_y-3))
        #s = F.dropout(F.relu(self.fc_bn1(self.fc1(s))), p=self.args.dropout, training=self.training)  # batch_size x 1024
        #s = F.dropout(F.relu(self.fc_bn2(self.fc2(s))), p=self.args.dropout, training=self.training)  # batch_size x 512
        x = self.pos_enc(s)
        x = x.view(-1, 144)
        x = self.transformer_encoder(x)
        x = self.global_avg_pooling(x)
        x = F.relu(self.dense1(x))
        x = F.relu(self.dense3(x))
        pi = self.dense2(x)
        v = self.output_layer(x)


        #pi = self.fc3(s)                                                                         # batch_size x action_size
        #v = self.fc4(s)                                                                          # batch_size x 1

        return F.log_softmax(pi, dim=1), torch.tanh(v)
