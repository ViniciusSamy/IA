import sys
import unittest






if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(arg)
        assert arg.isalpha()
    