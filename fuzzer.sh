#!/bin/bash

for i in {1..20}
do
	python3 fuzz.py|tee out/test_$i.txt;
done
