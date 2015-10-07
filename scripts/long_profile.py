#! /usr/bin/env python
from __future__ import print_function

import argparse
import re
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


def str2num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


class Dakota(object):
    FLOAT_REGEX = '[-+]?[0-9]*\.?[0-9]*([eE][-+]?[0-9]+)?'
    KEY_REGEX = '(?P<key>\w+)'
    VALUE_REGEX = '(?P<value>' + FLOAT_REGEX + ')'

    @staticmethod
    def read_params(filename):
        pattern = re.compile('\s*' + Dakota.VALUE_REGEX + '\s+' +
                             Dakota.KEY_REGEX)

        params = {}
        with open(filename, 'r') as fp:
            for line in fp:
                m = pattern.match(line)
                if m is not None:
                    params[m.group('key')] = str2num(m.group('value'))

        return params

    @staticmethod
    def read_aprepro(filename):
        pattern = re.compile('\s*\{\s+' + Dakota.KEY_REGEX + '\s+=\s+' +
                             Dakota.VALUE_REGEX + '\s+\}')

        params = {}
        with open(filename, 'r') as fp:
            for line in fp:
                m = pattern.match(line)
                if m is not None:
                    params[m.group('key')] = str2num(m.group('value'))

        return params

    @staticmethod
    def print_gradients(fp, grads):
        for items in zip(*grads):
            format_str = '[ ' + ' '.join(['%f'] * len(items)) + ' ]'
            print(format_str % items, file=fp)

    @staticmethod
    def print_hessians(fp, hessians):
        for items in zip(*hessians):
            format_str = '[[ ' + ' '.join(['%f'] * len(items)) + ' ]]'
            print(format_str % items, file=fp)

    @staticmethod
    def print_results(filename, x, gradients=None, hessians=None):
        gradients = gradients or ([], )
        hessians = hessians or ([], )

        np.savetxt(filename, x)
        with open(filename, 'a+') as fp:
            Dakota.print_gradients(fp, gradients)
            Dakota.print_hessians(fp, hessians)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('params', type=str, nargs='?',
                        help='Dakota parameters file')
    parser.add_argument('results', type=str, nargs='?',
                        help='Dakota results file')
    parser.add_argument('--model', choices=('power', 'log', 'peckham'),
                        default='power',
                        help='Model used to calculate longitudinal profile')
    parser.add_argument('--data', type=str,
                        default='beaver_creek.npy',
                        #default='beaver_channel_profile.csv',
                        help='Data file containing profile elevations')
    parser.add_argument('--sum-residuals', action='store_true',
                        help='Print only the sum of residuals to results file')
    parser.add_argument('--r-squared', action='store_true',
                        help='Print only the r-squared to results file')
    parser.add_argument('--fix-slope', action='store_true',
                        help='Fix s0 from data.')

    args = parser.parse_args()

    if args.params:
        params = Dakota.read_params(args.params)
    else:
        params = {}

    x, z = measured_elevations_from_file(args.data)
    params['x0'] = x[0]
    params['z0'] = z[0]
    if args.fix_slope:
        params['s0'] = - (z[1] - z[0]) / (x[1] - x[0])

    if args.model == 'power':
        model = PowerLawModel(params=params)
    elif args.model == 'log':
        model = LogModel(params=params)
    else:
        model = PeckhamModel(params=params)

    if args.results:
        if args.sum_residuals:
            response = model.residual_rms(x, z)
        elif args.r_squared:
            response = model.r_squared(x, z)
        else:
            response = model.residual(x, z)

        Dakota.print_results(args.results, response,
                             gradients=model.gradients(x))
    else:
        model.plot(x, z)


def sum_of_squares(y, f):
    return np.sum(np.power(y - f, 2.))


def r_squared(y, f):
    return 1. - sum_of_squares(y, f) / sum_of_squares(y, y.mean())


def measured_elevations_from_file(filename):
    (x, z) = np.load(filename)
    return (x, z)


class ChannelProfileModel(object):
    def __init__(self, params=None):
        self._params = params or {}

        self._x0 = params.get('x0')
        self._z0 = params.get('z0')

    def eval(self, x):
        raise NotImplementedError('eval')

    def residual(self, x, z):
        return self.eval(x) - z

    def residual_sum(self, x, z):
        return np.array(np.mean(self.eval(x) - z), dtype=float).reshape((1, ))

    def residual_rms(self, x, z):
        return np.array(np.sqrt(np.sum(self.residual(x, z) ** 2.))).reshape((1, ))

    def r_squared(self, x ,z):
        return np.array(r_squared(self.eval(x), z), dtype=float).reshape((1, ))

    def gradients(self, x):
        return (self._grad_wrt_c(x), self._grad_wrt_p(x))

    def _grad_wrt_c(self, x):
        return []

    def _grad_wrt_p(self, x):
        return []

    def plot(self, x, z):
        bbox_props = dict(boxstyle='square,pad=.5', fc='none')

        sns.set_style('whitegrid')

        plt.plot(x / 1000., z)
        plt.plot(x / 1000., self.eval(x))

        annotation = '\n'.join(['R^2 = %f' % r_squared(z, self.eval(x)),
                                self.text_summary()])
        plt.annotate(annotation, xy=(.05, .95),
                     xycoords='axes fraction', ha='left', va='top',
                     bbox=bbox_props)
        plt.title('Distance (km) vs elevation (m) for main channel profile of '
                  'Beaver Creek, KY.')
        plt.show()

    def text_summary(self):
        text = []
        for item in self._params.items():
            text.append('%s = %f' % item)
        return '\n'.join(text)


class PowerLawModel(ChannelProfileModel):
    def __init__(self, params=None):
        super(PowerLawModel, self).__init__(params=params)

        # newton
        #self._params.setdefault('c', 2.1784678105e+01)
        #self._params.setdefault('p', 1.4312563604e-01)
        # global
        #self._params.setdefault('c', 4.1460189615e+01)
        #self._params.setdefault('p', 5.4463636358e-02)
        # local
        #self._params.setdefault('c', 6.1090204531e+01)
        #self._params.setdefault('p', 1.0056306635e-03)
        self._params.setdefault('c', 3.9999968015e+01)
        self._params.setdefault('p', 6.1132405380e-02)

    def eval(self, x):
        c, p, x0 = self._params['c'], self._params['p'], self._params['x0']
        return self._z0 - (c / p) * (np.power(x, p) - np.power(x0, p))

    def _grad_wrt_c(self, x):
        p, x0 = self._params['p'], self._params['x0']
        return (- 1. / p) * (np.power(x, p) - np.power(x0, p))

    def _grad_wrt_p(self, x):
        c, p, x0 = self._params['c'], self._params['p'], self._params['x0']
        if np.abs(x0) < 1e-12:
            x0_log_x0 = 0.
        else:
            x0_log_x0 = np.power(x0, p) * np.log(x0)

        deriv = - (c / p ** 2.) * (
            - np.power(x, p) + p * np.power(x, p) * np.log(x) +
              np.power(x0, p) - p * x0_log_x0)

        deriv[np.abs(x) < 1e-12] = - (c / p ** 2.) * (np.power(x0, p) -
                                                      p * x0_log_x0)

        return deriv

    def __str__(self):
        return '$f(p,x) = (1/p) \, x^p$'


class LogModel(ChannelProfileModel):
    def __init__(self, params=None):
        super(LogModel, self).__init__(params=params)

        # newton
        self._params.setdefault('c', 2.0785632989e+02)
        self._params.setdefault('p', 6.0921199008e-01)
        # local
        #self._params.setdefault('c', 1.7369029258e+02)
        #self._params.setdefault('p', 6.6198835493e-01)
        # global
        #self._params.setdefault('c', 2.5405015305e+02)
        #self._params.setdefault('p', 5.5275361485e-01)

    def eval(self, x):
        c, p, x0 = self._params['c'], self._params['p'], self._params['x0']
        return self._z0 - c * (np.log(x) ** p - np.log(x0) ** p)

    def _grad_wrt_c(self, x):
        p, x0 = self._params['p'], self._params['x0']
        return - (np.log(x) ** p - np.log(x0) ** p)

    def _grad_wrt_p(self, x):
        c, p, x0 = self._params['c'], self._params['p'], self._params['x0']
        return - c * (np.log(np.log(x)) * np.power(np.log(x), p) -
                      np.log(np.log(x0)) * np.power(np.log(x0), p))

    def __str__(self):
        return '$f(p,x) = \log^p(x)$'


class PeckhamModel(ChannelProfileModel):
    def __init__(self, params=None):
        super(PeckhamModel, self).__init__(params=params)

        self._params.setdefault('gamma', -7.6991826046e-01)
        self._params.setdefault('r', 5.2248736972e-03)
        self._params.setdefault('s0', 6.7005230518e-01)
        self._params.setdefault('x0', 0.)
        self._params.setdefault('z0', 668.33)

    def eval(self, x):
        z0, x0, s0 = self._params['z0'], self._params['x0'], self._params['s0']
        r_star, gamma = self._params['r'], self._params['gamma']
        p_gamma = (gamma + 1.) / gamma
        return z0 + (1. / (p_gamma * r_star)) * (
            np.power(s0, gamma + 1.) - np.power(np.power(s0, gamma) +
                                                r_star * (x - x0), p_gamma)
        )

    def gradients(self, x):
        return ([], [], [])

    def _grad_wrt_s0(self, x):
        raise NotImplemented('grad_wrt_s0')

    def _grad_wrt_gamma(self, x):
        raise NotImplemented('grad_wrt_gamma')

    def _grad_wrt_r(self, x):
        raise NotImplemented('grad_wrt_r')

    def __str__(self):
        return '$f(x) = x$'


if __name__ == '__main__':
    main()
