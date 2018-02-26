#!/bin/bash

cd /home/alma/patrons

mv *.old loaded
#/home/alma/miniconda3/bin/python3 prep_xml.py
#/home/alma/miniconda3/bin/python3 
/home/alma/anaconda3/bin/python Patrons_v1tov2.py
#zip patrons.zip prep_patrons_*.xml
mv *.xml xml



