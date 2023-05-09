close all;
clear;
clc;

% check dimensions orientation
name = '46cm_walabot_100ms_tag'
A = readmatrix(append(name, '.csv')); % 4k by 256
%A_background = readmatrix(append(name, '_narrow_bg.csv')); % 1 by 4k
timestamps = readmatrix(append(name, '_timestamps.csv'))% timestamp between each for loop (make sure they are in seconds)

[bins,~] = size(A);
T = 79.98; % change 7.998046875e-08 seconds to ns
tau = T/bins;

from = 1;
to = bins;

As = A %- A_background;
tag_switch = 0.1; % in seconds


title = append(name, ' tag')
tag1 = pipeline(As, timestamps, from, to, T, tag_switch, title)
