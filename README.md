Dakota experiments that fit profiles to data from Beaver Creek
==============================================================

Run the experiments
-------------------

Use the `submit_all_experiments.sh` script to submit each of the experiments
as a separate job.

    $ bash ./scripts/submit_all_experiments.sh

Check the results
-----------------

When a job completes, check the best-fit parameters in it's output file,
`<model_name>.out`, and search for a line that begins with the following:

    <<<<< Best parameters

Results
-------

Best-fit parameters for Beaver Creek main profile data with *x0=0* using the
Power-Law Model}

| Method                                  | *p0*  | *c0* | *eps* |
| :-------------------------------------- | :---: | :--: | :---: |
| NL2SOL (analytic gradients)             | 0.133 | 14.7 |  784. |
| NL2SOL (numeric gradients)              | 0.133 | 14.7 |  784. |
| OPT++ Gauss-Newton (analytic gradients) | 0.133 | 14.7 |  784. |
| OPT++ Gauss-Newton (numeric gradients)  | 0.133 | 14.7 |  784. |
| Pattern Search (no gradients)           | 0.133 | 14.7 |  784. |
| Evolutionary Algorithm (no gradients)   | 0.130 | 14.8 |  786. |

Best-fit parameters for Beaver Creek main profile data with *x0=0* using the
Peckham Model}

| Method                                  | *r*  | *gamma* | *eps* |
| :-------------------------------------- | :----: | :---: | :---: |
| NL2SOL (numeric gradients)              | 0.0035 | -.702 |  223. |
| OPT++ Gauss-Newton (numeric gradients)  | 0.0035 | -.702 |  223. |
| Pattern Search (no gradients)           | 0.0041 | -.741 |  292. |
| Evolutionary Algorithm (no gradients)   | 0.0031 | -.678 |  253. |
