import numpy as np

def main(filename):
    # Load the .npy file
    data = np.load(filename, encoding='latin1', allow_pickle=True)
    # Display the contents
    print(data)
    for key in data.keys():
        print("Array name:", key)
        print("Array shape:", data[key].shape)
        print("Array dtype:", data[key].dtype)
        print("Array min:", data[key].min())
        print("Array max:", data[key].max())
        print()

if __name__ == "__main__":
    filename = input("Enter filename: ")
    main(filename)
