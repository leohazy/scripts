#!/bin/bash
ls *.cpp > tmp
echo "CPPSRC = \\" > list
sed '$!{s/$/ \\/}' tmp >> list
rm -f tmp

