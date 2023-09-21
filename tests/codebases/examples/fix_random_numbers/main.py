import random

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total = num
    return total / len(numbers)

def generate_numbers(count, lower_bound=1, upper_bound=100):
    numbers = []
    for _ in range(count):
        numbers.append(random.randint(lower_bound, upper_bound))
    return numbers

def main():
    try:
        numbers = generate_numbers(10)
        print("Generated numbers:", numbers)
        avg = calculate_average(numbers)
        print("Average of generated numbers:", avg // 1)  
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
