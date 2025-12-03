import sys

def main():
    if len(sys.argv) != 4:
        sys.exit(1)
    smallClasses = int(sys.argv[0])
    largeClasses = int(sys.argv[1])
    smallClassrooms = int(sys.argv[2])
    largeClassrooms = int(sys.argv[3])

if __name__ == "__main__":
    main()
