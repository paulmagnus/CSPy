import pickle, sys

f = open(sys.argv[1])
lst = pickle.load(f)

for key in lst:
    print(str(key) + " : " + str(lst[key]))

f.close()