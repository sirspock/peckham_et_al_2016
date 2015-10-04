Dakota experiments that fit profiles to data from Beaver Creek
==============================================================

Create new channel profile
--------------------------

    >>> import numpy as np
    >>> data = np.fromtxt('beaver_creek_channel_profile_new.csv')
    >>> x = data[1:, 0] * 1000. # Convert distances from km to m
    >>> z = data[1:, 1] # dakota doesn't like the first position to be 0.
    >>> out = np.vstack((x.T, z.T))
    >>> np.save('beaver_creek_new.npy', out)

Change the number of calibrations terms in the dakota config files to be the
new number of points along the profile.

Run the experiments
-------------------

Use the `submit_all_experiments.sh` script to submit each of the experiments
as a separate job.

    $ mkdir _experiments
    $ cd _experiments
    $ bash ../submit_all_experiments.sh

Check the results
-----------------

When a job completes, check the best-fit parameters in it's output file,
`<model_name>.out`, and search for a line that begins with the following:

    <<<<< Best parameters

