def truncate_and_split_file(input_file, train_file, valid_file, test_file, truncate_fraction, train_fraction, valid_fraction, test_fraction):
    # input file is the original train.txt
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Truncate the dataset to a fraction of its original size
    truncated_size = int(len(lines) * truncate_fraction)
    truncated_lines = lines[:truncated_size] 

    # Extract times , which is the 4th column
    times = []
    for line in truncated_lines:
        times.append(int(line.split()[3]))

    # Find unique time points
    unique_times = sorted(set(times))

    # Calculate the number of time points for train, valid, and test sets
    train_time_size = int(train_fraction * len(unique_times))
    valid_time_size = int(valid_fraction * len(unique_times))

    # split so there is no overlapping between times for each dataset
    train_times = unique_times[:train_time_size]
    valid_times = unique_times[train_time_size:train_time_size + valid_time_size]
    test_times = unique_times[train_time_size + valid_time_size:]

    # since we can't have overlapping timeframes in train, val, and test
    if valid_times[0] < train_times[-1] + 15:
        valid_times = []
        for t in unique_times:
            if t >= train_times[-1] + 15:
                valid_times.append(t)
            if len(valid_times) >= valid_time_size:
                break
    if test_times[0] < valid_times[-1] + 15:
        test_times = []
        for t in unique_times:
            if t >= valid_times[-1] + 15:
                test_times.append(t)

    train_lines = []
    valid_lines = []
    test_lines = []

    for line in truncated_lines:
        time = int(line.split()[3])
        if time in train_times:
            train_lines.append(line)
        elif time in valid_times:
            valid_lines.append(line)
        elif time in test_times:
            test_lines.append(line)

    # Write to train, valid, and test files
    with open(train_file, 'w') as f:
        f.writelines(train_lines)
    with open(valid_file, 'w') as f:
        f.writelines(valid_lines)
    with open(test_file, 'w') as f:
        f.writelines(test_lines)

    print(f"Data split complete. Truncated: {truncated_size} lines. Train: {len(train_lines)}, Validation: {len(valid_lines)}, Test: {len(test_lines)}")


input_train_file = 'train_whole.txt'  # The original train.txt file
output_train_file = 'train.txt'
output_valid_file = 'valid.txt'
output_test_file = 'test.txt'

truncate_fraction = 0.1 #the percentage that we take from train.txt
train_fraction = 0.80
valid_fraction = 0.10
test_fraction = 0.10

truncate_and_split_file(input_train_file, output_train_file, output_valid_file, output_test_file, truncate_fraction, train_fraction, valid_fraction, test_fraction)
