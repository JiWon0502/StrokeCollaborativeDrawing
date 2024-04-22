import numpy as np

def main(filename):
    # Load the .npy file
    data = np.load(filename)
    # Display the contents
    print(data)

if __name__ == "__main__":
    filename = input("Enter filename: ")
    main(filename)
