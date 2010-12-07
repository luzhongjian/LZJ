from os import walk
from os.path import join

def main():
   for parent, dirs, files in walk('.'):
      for file in files:
         if (file.endswith('.wav')):
            print file

if __name__ == '__main__':
   main()

