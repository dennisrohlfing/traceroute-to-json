#!/bin/bash
times=10000
for i in {1..10000}
do
   printf  "\n $i times from $times \n"

   printf "\n Trace google4 \n"
   traceroute -q 1 -4 www.google.de >> google4.txt
    for i in {01..30}; do
    sleep 1
    printf "\r Wait $i from 30 seconds"
    done

   printf "\n Trace Uni4 \n"
   traceroute -q 1 -4 www.uni-bremen.de >> uni4.txt
    for i in {01..30}; do
    sleep 1
    printf "\r Wait $i from 30 seconds"
    done

#   printf "\n Trace google6 \n"
#   traceroute -q 1 -6 www.google.de >> google6.txt
#    for i in {01..30}; do
#    sleep 1
#    printf "\r Wait $i from 30 seconds"
#    done

#   printf "\n Trace Uni6 \n"
#   traceroute -q 1 -6 www.uni-bremen.de >> uni6.txt
#    for i in {01..30}; do
#    sleep 1
#    printf "\r Wait $i from 5 seconds"
#    done

done