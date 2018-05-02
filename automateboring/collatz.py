"""Write a function named collatz() that has one parameter named number. If number is even, then collatz() should print number // 2 and return this value. If number is odd, then collatz() should print and return 3 * number + 1."""

def collatz(number):
    seq_num = (number // 2) if number % 2 == 0 else (3 * number + 1)
    print(seq_num)
    return seq_num

our_int = int(input('Enter an integer: '))
num = collatz(our_int)

while True:
    if num == 1:
        break
    num = collatz(num)

