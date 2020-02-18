
def dice(x,y):
    '''
    (str,str) -> int

    This function returns the total number of ways an x and y sided dice can sum to 12
    '''
    res = 0
    x = int(x)
    y = int(y)
    if(x+y >= 12):
        if (x >= 12 and y >= 12):
            return 11
        elif(max(x,y) >= 12 and min(x,y) < 12):
            return min(x,y)
        else:
            values = {1: 11, 2:10, 3:9, 4:8, 5:7, 6:6, 7:5, 8:4, 9:3, 10:2, 11:1}
            for key in values:
                if(x-key >= 0 and y-values[key] >= 0):
                    res += 1
            return res
    else:
        return 0


x = input('Enter x:')
y = input('Enter y:')
print(dice(x,y))