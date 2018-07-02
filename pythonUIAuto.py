import subprocess
import uiautomation as automation
import time
import itertools

# Constants 
pieces = ['common','password','pieces', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'abc', 'def']
minPasswordLength = 9
maxPasswordLength = 38
minNumPiecesToCombine = 3

if minNumPiecesToCombine >= len(pieces):
    print("Error, minNumPiecesToCombine must be strictly less than the number of entries in the 'pieces' array")
    exit

print("Sleeping for 3 seconds while you set the mouse focus into the TrueCrypt text input field")
time.sleep(3) 

print(automation.GetRootControl())
edit = automation.GetRootControl().EditControl()
done = False
entryCount = 0

for x in range(minNumPiecesToCombine, len(pieces)):
    
    # Print loop status 
    print("List choose " + str(x))
    print(str(len(pieces)) +"! / " + str(x) +"! / (" + str(len(pieces)) + "-" + str(x) + ")!")
    
    # Iterate over all combinations of 'pieces', where we choose 'x' pieces to combine 
    for entry in itertools.combinations(pieces, x):
        if len(''.join(entry)) < minPasswordLength or len(''.join(entry)) > maxPasswordLength:
            #skip the shorter and longer lengths 
            entryCount += 1
            continue
        edit = automation.GetRootControl().EditControl()
        edit.SetValue(''.join(entry))
        edit.SendKeys('{Enter}')
        edit.SendKeys('{Enter}')
        entryCount += 1

        if automation.GetRootControl().EditControl().AutomationId != '1035':
            #Success
            print(''.join(entry))
            f= open("volumeOutput.txt","w+")
            f.write(''.join(entry))
            f.close()
            done = True
            break;
        if entryCount % 20 == 0:
            # Output our progress every 20 entries 
            f= open("entryCountOutput.txt","w+")
            f.write(''.join(entry))
            f.close()
    if done:
        break;