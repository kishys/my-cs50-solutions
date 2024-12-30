import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    database = []
    with open(sys.argv[1], mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for key in row:
                if key != "name":
                    row[key] = int(row[key])
            database.append(row)

    with open(sys.argv[2], mode='r') as file:
        dna_sequence = file.read()

    str_keys = list(database[0].keys())[1:]

    str_counts = {}
    for str_key in str_keys:
        str_counts[str_key] = longest_match(dna_sequence, str_key)

    match_found = False
    for person in database:
        if all(person[str_key] == str_counts[str_key] for str_key in str_keys):
            print(person["name"])
            match_found = True
            break

    if not match_found:
        print("No match")


def longest_match(sequence, subsequence):
    """Returns the longest run of consecutive repeats of 'subsequence' in 'sequence'."""
    longest_run = 0
    subseq_len = len(subsequence)
    seq_len = len(sequence)

    for i in range(seq_len):
        count = 0

        while sequence[i + count * subseq_len:i + (count + 1) * subseq_len] == subsequence:
            count += 1

        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
