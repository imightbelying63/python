import os
import sys

for filename in os.listdir('./'):
	file_ext = os.path.splitext(filename)[1]
	print file_ext

