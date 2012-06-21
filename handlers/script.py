import sys

list = []

for arg in sys.argv[1:]:
#    sys.stdout.write("Arg: %s"%arg)
    list.append(arg)
print list
