class AutoScan:

    def __init__(self,
                 task,
                 max_param_values):

        '''Configure the `AutoScan()` experiment and then use
        the property `start` in the returned class object to start
        the actual experiment.

        `task` | str | 'binary', 'multi_class', 'multi_label', or 'continuous'
        `max_param_values` | int | Number of parameter values to be included
        '''

        self.task = task
        self.max_param_values = max_param_values

    def start(self, x, y, **kwargs):

        '''Start the scan. Note that you can use `Scan()` arguments as you
        would otherwise directly interacting with `Scan()`.

        `x` | array or list of arrays | prediction features
        `y` | array or list of arrays | prediction outcome variable
        `kwargs` | arguments | any `Scan()` argument can be passed here

        '''

        import talos

        p = talos.autom8.AutoParams(task=self.task)
        p.resample_params(self.max_param_values)
        params = p.params

        m = talos.autom8.AutoModel(self.task).model
        scan_object = talos.Scan(x, y, params, m, **kwargs)

        return scan_object
