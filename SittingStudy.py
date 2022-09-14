import os
from OpenBCIAPI import OpenBCIAPI


subject_id = "example"
day = "X"

cwd = os.getcwd()
fs = subject_id + "_Day" + day + "_"

bci = OpenBCIAPI(num_ch=16, debug=False)
bci.connect()

print("Symbol Match")
input("Press enter when you are ready to record")

f1 = fs + "Symbol_Match.txt"
f1 = os.path.join(cwd, f1)
bci.cont_record(filename=f1)

print("Item Price")
input("Press enter when you are ready to record")

f2 = fs + "Item_Price.txt"
f2 = os.path.join(cwd, f2)
bci.cont_record(filename=f2)

print("Trails")
input("Press enter when you are ready to record")

f3 = fs + "Trails.txt"
f3 = os.path.join(cwd, f3)
bci.cont_record(filename=f3)

print("Flankers")
input("Press enter when you are ready to record")

f4 = fs + "Flankers.txt"
f4 = os.path.join(cwd, f4)
bci.cont_record(filename=f4)

print("Go/No-Go")
input("Press enter when you are ready to record")

f5 = fs + "Go-No-Go.txt"
f5 = os.path.join(cwd, f5)
bci.cont_record(filename=f5)

print("Test done")
