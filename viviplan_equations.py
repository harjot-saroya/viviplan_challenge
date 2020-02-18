def presval(payment,rate,num_periods):
    '''
    (float, float, int) -> Present
    value of annuity due

    Rate is to be entered as a decimal 
    ex. 1% -> 0.01

    This function takes 3 inputs and returns a calulation
    '''

    res =  1
    for i in range(0,num_periods-1):
        res = res *  1/(1 + rate)
    present_value = payment + payment * ((1-res)/rate)
    return round(present_value,2)

def futureval(payment,rate,num_periods):
    '''
    (float, float, int) -> Future
    value of annuity due

    Rate is to be entered as a decimal 
    ex. 1% -> 0.01

    This function takes 3 inputs and returns a calulation
    '''

    res =  1
    for i in range(0,num_periods):
        res = res *  (1 + rate)
    
    rs = payment * (res -1)/rate
    result = ((1+rate) * rs)
    return round(result,2)

def anndue(presentval,rate,num_periods):
    '''
    (float, float, int) -> annuity due payment

    Rate is to be entered as a decimal 
    ex. 1% -> 0.01

    This function takes 3 inputs and returns a calulation
    '''
    res = 1
    for i in range(0,num_periods):
        res = res *  1/(1 + rate)
    
    anndue = (presentval * (rate/(1-res))) * 1/(1+rate)
    return round(anndue,2)

def greeting():
    '''
    () -> float

    This function takes input from the user and gives the calculation
    they want
    '''
    done = False
    while not done:

        print('Welcome, please enter the type of calculation you want:')
        print('a for future value of annuity due')
        print('b for present value of annuity due')
        print('c for annuity due payment')
        print('Enter q to quit')
        calc = input('Please enter here: ')
        if calc == 'a':
            inp = greeting_help(calc)
            return futureval(inp[0],inp[1],inp[2])
        elif calc == 'b':
            inp = greeting_help(calc)
            return presval(inp[0],inp[1],inp[2])
        elif calc == 'c':
            inp = greeting_help(calc)
            return anndue(inp[0],inp[1],inp[2])
        elif calc == 'q':
            print('Goodbye!')
            done = True

def greeting_help(calc):
    present_value = 0
    payment = 0
    rate = 0
    num_periods = 0

    if calc == 'ad':
        present_value = input('Type in present value: ')
        rate = input('Type in rate (as percentage ie. 1% = 0.01): ')
        num_periods = input('Type in number of periods: ')
        return (present_value,rate,num_periods)
    payment = input('Type in present value: ')
    rate = input('Type in rate (as percentage ie. 1% = 0.01): ')
    num_periods = input('Type in number of periods: ')
    return (payment,rate,num_periods)

print(greeting())