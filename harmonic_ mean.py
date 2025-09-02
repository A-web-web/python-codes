#Input: List of numbers
data = [1, 2, 3, 4, 5]

# Ensure the dataset is not empty
if len(data) == 0:
    print("The dataset is empty. Harmonic mean cannot be calculated.")
else:
    # Calculate the harmonic mean
    reciprocal_sum = 0
    for num in data:
        if num != 0:  # Avoid division by zero
            reciprocal_sum += 1 / num
        else:
            print("Harmonic mean is undefined for datasets containing zero.")
            break
    else:
        harmonic_mean = len(data) / reciprocal_sum
        print(f"The harmonic mean of the dataset is: {harmonic_mean}")
