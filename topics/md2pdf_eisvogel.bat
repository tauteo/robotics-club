@echo off
pandoc %1^
 -f markdown^
 --template eisvogel^
 --listings^
 -o %2