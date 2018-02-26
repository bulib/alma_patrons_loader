#!/bin/bash

cd /home/alma/patrons

mv *.old loaded
/home/alma/anaconda3/bin/python Patrons_v1tov2.py
mv *.xml xml



