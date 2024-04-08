#!/bin/bash

pid=$(cat ./pid.txt)

kill -2 $pid

> pid.txt

sleep 7

python main.py