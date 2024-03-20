def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def reverse_string(s):
    return s[::-1]


if __name__ == "__main__":
    example = "6"
    try:
        num = int(example)
        if num < 0:
            result = "Please enter a non-negative number."
        else:
            result = f"The factorial of {num} is {factorial(num)}"
    except ValueError:
        print("Invalid input. Please enter a number.")

    string_to_reverse = result
    print(f"The reversed string is: {reverse_string(string_to_reverse)}")
    print(f"The original string was: {string_to_revers}")
