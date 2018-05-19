
def aboveten(data):
    num1 = int(data["num1"])
    num2 = int(data["num2"])
    num3 = int(data["num3"])

    if (num1+num2+num3)>10:
        return True
    else:
        return False 
