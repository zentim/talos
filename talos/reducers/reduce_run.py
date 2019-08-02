def reduce_run(self):

    '''The process run script for reduce
    procedures; takes care of everything
    related with reduction. When new
    reduction methods are added, they need
    to be added as options here.

    To add new reducers, create a file in /reducers
    which is where this file is located. In that file,
    take as input self from Scan() and give as output
    either False, which does nothing, or a tuple of
    'value' and 'label' where value is a parameter
    value and label is parameter name. For example
    batch_size and 128. Then add a reference to
    reduce_run.py and make sure that you process
    the self.param_object.param_index there before
    wrapping up.

    '''

    from .correlation import correlation
    from .local_strategy import local_strategy
    from .limit_by_metric import limit_by_metric

    # check if performance target is met
    if self.performance_target is not None:
        status = limit_by_metric(self)

        # handle the case where performance target is met
        if status is True:
            self.param_object.param_index = []

    # stop here if no reduction method is set
    if self.reduction_method is None:
        return self

    # setup what's required for updating progress bar
    left = (self.param_object.round_counter + 1)
    right = self.reduction_interval
    len_before_reduce = len(self.param_object.param_index)

    # apply window based reducers
    if left % right == 0:

        # check if correlation reducer can do something
        if self.reduction_method in ['pearson', 'kendall', 'spearman']:
            self = correlation(self, self.reduction_method)

        # check if correlation reducer can do something
        if self.reduction_method == 'correlation':
            self = correlation(self, 'spearman')

        # check if random forrest can do something
        if self.reduction_method == 'random_forrest':
            pass

        # check if random forrest can do something
        if self.reduction_method == 'extra_trees':
            pass

        # check if monte carlo can do something
        if self.reduction_method == 'monte_carlo':
            pass

        if self.reduction_method == 'local_strategy':
            self = local_strategy(self)

        # finish up by updating progress bar
        total_reduced = len_before_reduce - len(self.param_object.param_index)
        total_reduced = max(0, total_reduced)
        self.pbar.update(total_reduced)

    return self
