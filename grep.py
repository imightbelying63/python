#!/bin/env python

for line in open("wwwacct.conf"):
  if "HOMEMATCH" in line:
    hmatch = line
    break

if hmatch:
  hsplit = hmatch.split(" ")[1]
  print hsplit.rstrip("\n")

