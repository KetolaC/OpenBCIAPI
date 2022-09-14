import os
from OpenBCIAPI import OpenBCIAPI


subject_id = "example"
day = "X"

cwd = os.getcwd()
fs = subject_id + "_Day" + day + "_"

bci = OpenBCIAPI(num_ch=16, debug=False)
bci.connect()
print("Ready to collect test battery data")

print("\nSymbol Match")
input("Press enter when you are ready to record")

f1 = fs + "Symbol_Match.txt"
f1 = os.path.join(cwd, f1)
bci.cont_record(filename=f1)

print("\nItem Price")
input("Press enter when you are ready to record")

f2 = fs + "Item_Price.txt"
f2 = os.path.join(cwd, f2)
bci.cont_record(filename=f2)

print("\nTrails")
input("Press enter when you are ready to record")

f3 = fs + "Trails.txt"
f3 = os.path.join(cwd, f3)
bci.cont_record(filename=f3)

print("\nFlankers")
input("Press enter when you are ready to record")

f4 = fs + "Flankers.txt"
f4 = os.path.join(cwd, f4)
bci.cont_record(filename=f4)

print("\nGo/No-Go")
input("Press enter when you are ready to record")

f5 = fs + "Go-No-Go.txt"
f5 = os.path.join(cwd, f5)
bci.cont_record(filename=f5)

print("Test battery done")

bci.disconnect()

print("OpenBCI board may be powered down while surveys are being conducted")
input("Press enter when motor movement test is set-up and bord is powered on.")

bci.connect()

print("\nMotor Movement")

input("\nPress enter when ready to record 10 seconds of relaxed state (eyes-open) data")

f6 = fs + "MM_Relaxed.txt"
f6 = os.path.join(cwd, f6)

bci.timed_record(seconds=10, filename=f6)

input("\nPress enter when ready to record 10 seconds of open hand data")

f7 = fs + "MM_Open.txt"
f7 = os.path.join(cwd, f7)

bci.timed_record(seconds=10, filename=f7)

input("\nPress enter when ready to record 10 seconds of pointing data")

f8 = fs + "MM_Index.txt"
f8 = os.path.join(cwd, f8)

bci.timed_record(seconds=10, filename=f8)

input("\nPress enter when ready to record 10 seconds of thumbs up data")

f9 = fs + "MM_Thumb.txt"
f9 = os.path.join(cwd, f9)

bci.timed_record(seconds=10, filename=f9)

input("\nPress enter when ready to record 10 seconds of index and thumb data")

f10 = fs + "MM_Index_and_Thumb.txt"
f10 = os.path.join(cwd, f10)

bci.timed_record(seconds=10, filename=f10)

input("\nPress enter when ready to record 10 seconds of closed fist data")

f11 = fs + "MM_Closed.txt"
f11 = os.path.join(cwd, f11)

bci.timed_record(seconds=10, filename=f11)

input("\nPress enter when ready to record 10 seconds of ok sign data")

f12 = fs + "MM_OK.txt"
f12 = os.path.join(cwd, f12)

bci.timed_record(seconds=10, filename=f12)

input("\nPress enter when ready to record 10 seconds of four fingers (thumb closed) data")

f13 = fs + "MM_Four_Fingers.txt"
f13 = os.path.join(cwd, f13)

bci.timed_record(seconds=10, filename=f13)

input("\nPress enter when ready to record 10 seconds of pinched fingers data")

f14 = fs + "MM_Pinch.txt"
f14 = os.path.join(cwd, f14)

bci.timed_record(seconds=10, filename=f14)

print("Done recording motor movement")

print("\nMotor Imagery")

input("\nPress enter when ready to record 10 seconds of relaxed state (eyes-open) data")

f15 = fs + "MI_Relaxed.txt"
f15 = os.path.join(cwd, f15)

bci.timed_record(seconds=10, filename=f15)

input("\nPress enter when ready to record 10 seconds of open hand data")

f16 = fs + "MI_Open.txt"
f16 = os.path.join(cwd, f16)

bci.timed_record(seconds=10, filename=f16)

input("\nPress enter when ready to record 10 seconds of pointing data")

f17 = fs + "MI_Index.txt"
f17 = os.path.join(cwd, f17)

bci.timed_record(seconds=10, filename=f17)

input("\nPress enter when ready to record 10 seconds of thumbs up data")

f18 = fs + "MI_Thumb.txt"
f18 = os.path.join(cwd, f18)

bci.timed_record(seconds=10, filename=f18)

input("\nPress enter when ready to record 10 seconds of index and thumb data")

f19 = fs + "MI_Index_and_Thumb.txt"
f19 = os.path.join(cwd, f19)

bci.timed_record(seconds=10, filename=f19)

input("\nPress enter when ready to record 10 seconds of closed fist data")

f20 = fs + "MI_Closed.txt"
f20 = os.path.join(cwd, f20)

bci.timed_record(seconds=10, filename=f20)

input("\nPress enter when ready to record 10 seconds of ok sign data")

f21 = fs + "MI_OK.txt"
f21 = os.path.join(cwd, f21)

bci.timed_record(seconds=10, filename=f21)

input("\nPress enter when ready to record 10 seconds of four fingers (thumb closed) data")

f22 = fs + "MI_Four_Fingers.txt"
f22 = os.path.join(cwd, f22)

bci.timed_record(seconds=10, filename=f22)

input("\nPress enter when ready to record 10 seconds of pinched fingers data")

f23 = fs + "MI_Pinch.txt"
f23 = os.path.join(cwd, f23)

bci.timed_record(seconds=10, filename=f23)

print("Done recording motor imagery")

bci.disconnect()

print("Board can be powered off while setting up 9-hole peg test")
input("Press enter when the 9-hole peg test is set up and board is powered on.")

bci.connect()

print("\n9-hole Peg Test")

input("Press enter to record 9-hole peg test.")

f24 = fs + "Peg_Test.txt"
f24 = os.path.join(cwd, f24)
bci.cont_record()

bci.disconnect()

print("Test Done. You may power off the board.")
