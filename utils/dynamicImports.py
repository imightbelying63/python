"""quick demo of how to dynamically import a list of modules and hanlde
   ImportError exception
"""
to_import = ['re', 'subprocess', 'platform', 'argparse', 'time']
for mod in to_import:
  try:
    exec('import '+mod)
  except ImportError:
    print('failed to import '+mod) #this is a fake function as an example
