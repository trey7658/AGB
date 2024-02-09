from pyprobs import Probability as pr

# This file is for the base commands of the bot, it has been put in a separate file to make the main file cleaner.
# I also have a seperate bot that uses this too, so it makes it easier to copy over the commands. It may be removed later.

async def uwu(message):
    splitlist = message.split()
    new = ''
    wordlist = ['lol', 'fun']
    lastuwu = False
    for value in splitlist:
        if not value in wordlist:
            value = value.replace('L', 'W').replace('l', 'w').replace('R', 'W').replace('r', 'w').replace('n', 'nw').replace('N', 'NW')
        if pr.prob(1/7) and lastuwu == False:
            lastuwu = True
            if pr.prob(2/3):
                new = new + ' UwU ' + value
            else:
                new = new + ' OwO ' + value
        else:
            new = new + ' ' + value
            lastuwu = False
    new = new + ' :3'
    return new

async def num(num: int):
    for unit in ("", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion"):
        if abs(num) < 1000:
            return f"{round(num, 1)} {unit}"
        num /= 1000
    return f"{num:}Yi"
