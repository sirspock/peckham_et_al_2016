#! /usr/bin/env python


def main():
    import numpy as np
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='Name of input CSV file.')
    parser.add_argument('out', help='Name of output npy file.')

    args = parser.parse_args()
    data = np.loadtxt(args.csv)

    x = data[:, 0] * 1000. # Convert distances from km to m
    z = data[:, 1] # dakota doesn't like the first position to be 0.

    out = np.vstack((x.T, z.T))
    np.save(args.out, out)


if __name__ == '__main__':
    main()
