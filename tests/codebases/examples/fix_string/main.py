
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def reverse_string(s):
    return s[::-1]


if __name__ == "__main__":
    try:
        num = int(input("Enter a number to find its factorial: "))
        if num < 0:
            print("Please enter a non-negative number.")
        else:
            print(f"The factorial of {num} is {factorial(num)}")
    except ValueError:
        print("Invalid input. Please enter a number.")

    string_to_reverse = input("Enter a string to reverse: ")
    print(f"The reversed string is: {reverse_string(string_to_reverse)}")
    print(f"The original string was: {string_to_revers}")
