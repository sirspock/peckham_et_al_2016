#!/usr/bin/env python
import argparse

import yaml
import matplotlib.pyplot as plt
import seaborn as sns

from long_profile import (PowerLawModel, LogModel, PeckhamModel,
                          measured_elevations_from_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('params', type=str, nargs='?', help='Dakota parameters file')
    parser.add_argument('results', type=str, nargs='?',
                        help='Dakota results file')
    parser.add_argument('--model', choices=('power', 'log', 'peckham'),
                        default='power',
                        help='Model used to calculate longitudinal profile')
    parser.add_argument('--data', type=str,
                        default='beaver_channel_profile.csv',
                        help='Data file containing profile elevations')

    args = parser.parse_args()

    with open(args.params, 'r') as fp:
        params = yaml.load(fp)
    plot_models(args.data, params)


def plot_models(data_file, params):
    models = [
        PowerLawModel(params=params['power']),
        LogModel(params=params['log']),
        #PeckhamModel(params=params['peckham']),
    ]
    bbox_props = dict(boxstyle='square,pad=.5', fc='none')

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    #sns.set_style('whitegrid')
    sns.set_style('ticks')
    sns.set_context('talk', font_scale=1.5)

    x, z = measured_elevations_from_file(data_file)
    plt.plot(x / 1000., z, linestyle='-', color='k', label='observed')
    for model, style in zip(models, [':', '--']):
        plt.plot(x / 1000., model.eval(x), label=str(model), linestyle=style,
                 color='k')

    plt.legend()
    plt.title('\\textbf{Logitudinal profile for Beaver Creek, KY.}\n'
              'Distance (km) vs. elevation (m) for modeled and observed',
              loc='left')#, fontweight='bold')

    sns.despine()
    plt.show()


if __name__ == '__main__':
    main()
