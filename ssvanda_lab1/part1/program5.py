
class program5:
    def sum_Function(self):
        firstDict = {0:10,1:20,2:10,3:40,4:50,5:60,6:70}
        target = int(input("What is your target number? "))
        secondDict = {}
        for x, element in firstDict.items():
            if (target - element) in secondDict:
                print("index1=" + str(secondDict[target - element]) + ", index2=" + str(x))
                break
            secondDict[element] = x
program5().sum_Function()