from types import FunctionType, BuiltinMethodType, BuiltinFunctionType
from functools import partial
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta as rd
from time import sleep


class RunOnTimer:
    """Run the 'function_to_run' at the provided interval.  If the fail_check
    parameter is provided, the function will check the dict of
    fail_check_responses if a failure state is encountered and will respond
    using the provided value.

    :param function_to_run: *required* Method or function

    :param frequency: String, int, or dateutil.relativedelta.relativedelta
        object
        -Defaults to 'Daily'
        String options (not case sensitive)-
            'daily' -- Every 24 hrs
            'semi-weekly' -- Every 3 days 12 hrs.
            'weekly' -- Every week
            'bi-weekly' -- Every 2 weeks
            'monthly' -- Ever 2 month
            'bi-monthly' -- Every 2 months
            'quarterly' -- Every 3 months
            'semi-annualy' -- Every 6 months
            'annually' -- Every 1 year
            'bi-annually' -- Every 2 years
        Int - Ints are treated as a number of days

    :param trigger_time: Datetime time object or string using the HH:MM:SS 24hr
    clock format
        -string example '16:00:00' for 4pm

    :param iterations: Int or None
        -Defaults to None
        -Sets a maximum number of times the function will trigger.

    :param stop_date: String or None
        -Defaults to None
        -Sets a date when the script will stop running.
        -Use the YYYY/MM/DD date format

    :param fail_check: Boolean (Not Currenly Implemented)
        -Defaults to False
        -If set to true the function will respond to failures in the provided
        method/function using the methods described in the fail_check_responses
        paramter

    :param fail_check_responses: *required if the fail_check parameter is set
    to True* Dictionary or None (Not Currently Implemented)
        -Defaults to None

    :param params: a value, dict, or list of parameters to be passed to the function to run as
    **kwargs or None
        -Defaults to None
        -in a future version this should check to see if the params are a
        single value (not a list or a dictionary), a list (which will be
        treated as * args) or a dict (which will be treated as **kwargs)


    ---------------------------------------------------------------------------
    Examples:
    ---------------------------------------------------------------------------
    Run the print_hi function daily for the next two days at noon without
    providing any kwargs to the print hi function.  If this is run prior to
    noon it will trigger the print_hi function at noon on the day the run is
    started and the next day.  If run after noon it will trigger the next day
    and the day after.

    def print_hi():
        now = dt.now()
        print('Hi {}!  It is currently {}'.format('No Kwargs ', now))

    TriggerTimer(
        print_hi,
        **{
            'frequency':'daily',
            'trigger_time':'12:00:00',
            'iterations': 2,
            'stop_date':None,
            'fail_check':False,
            'fail_check_responses':None
        }
    )

    Run the print_hi function daily at noon until the 15th of June providing
    kwargs to the print_hi function.  If this is run prior to noon it will
    trigger the print_hi function at noon on the day the run is started and the
    next day.  If run after noon it will trigger the next day and the day
    after.

    def print_hi(**kwargs):
        now = dt.now()
        print('Hi {}!  It is currently {}'.format(kwargs['name'], now))

    TriggerTimer(
        print_hi,
        frequency='daily',
        trigger_time='12:00:00',
        iterations=None,
        stop_date="2020/06/15",
        fail_check=False,
        fail_check_responses=None,
        params={'name':'David'}
    )
    """
    def __init__(self, function_to_run, **kwargs):
        self.kwargs = kwargs
        self.function = function_to_run
        self.frequency = None
        self.trigger_time = None
        self.iterations = None
        self.stop_date = None
        self.fail_check = None
        self.fail_check_responses = None
        self.current_iteration = 0
        self.last_run = None
        self.params = None

        self.create_class_vars()

        if self.test_function(self.function) and self.test_fail_check() \
            and self.check_iterations():
            if not self.iterations:
                if not self.stop_date:
                    while True:
                        if self.trigger_time:
                            self.check_date()
                            self.check_time()
                            if self.params:
                                self.function(self.params)
                            else:
                                self.function()
                            self.last_run = dt.now().date()
                        else:
                            self.check_date()
                            if self.params:
                                self.function(self.params)
                            else:
                                self.function()
                            self.last_run = dt.now().date()
                else:
                    while self.check_stop_date() == 1:
                            if self.trigger_time:
                                self.check_date()
                                self.check_time()
                                if self.params:
                                    self.function(self.params)
                                else:
                                    self.function()
                                self.last_run = dt.now().date()
                            else:
                                self.check_date()
                                if self.params:
                                    self.function(self.params)
                                else:
                                    self.function()
                                self.last_run = dt.now().date()
            else:
                if not self.stop_date:
                    while self.current_iteration != self.iterations:
                        if self.trigger_time:
                            self.check_date()
                            self.check_time()
                            if self.params:
                                self.function(self.params)
                            else:
                                self.function()
                            self.current_iteration += 1
                            self.last_run = dt.now().date()
                        else:
                            self.check_date()
                            if self.params:
                                self.function(self.params)
                            else:
                                self.function()
                            self.current_iteration += 1
                            self.last_run = dt.now().date()
                else:
                    while (self.check_stop_date() == 1) and (self.current_iteration != self.iterations):
                        if self.trigger_time:
                            self.check_date()
                            self.check_time()
                            if self.params:
                                self.function(self.params)
                            else:
                                self.function()
                            self.current_iteration += 1
                            self.last_run = dt.now().date()
                        else:
                            self.check_date()
                            if self.params:
                                self.function(self.params)
                            else:
                                self.function()
                            self.current_iteration += 1
                            self.last_run = dt.now().date()

    def create_class_vars(self):
        """
        Fill the class variables from the **kwargs values
        """
        if "frequency" in self.kwargs.keys():
            self.frequency = self.kwargs["frequency"]
        else:
            pass
        if "trigger_time" in self.kwargs.keys():
            self.trigger_time = self.kwargs["trigger_time"]
        else:
            pass
        if "iterations" in self.kwargs.keys():
            self.iterations = self.kwargs["iterations"]
        else:
            pass
        if "stop_date" in self.kwargs.keys():
            self.stop_date = self.kwargs["stop_date"]
        else:
            pass
        if "fail_check" in self.kwargs.keys():
            self.fail_check = self.kwargs["fail_check"]
        else:
            pass
        if "fail_check_responses" in self.kwargs.keys():
            self.fail_check_responses = self.kwargs["fail_check_responses"]
        else:
            pass
        if "params" in self.kwargs.keys():
            self.params = self.kwargs["params"]
        else:
            pass

    def check_date(self):
        """
        Check the last_run varaiable value vs the meaning of the frequency
        parameter using a dictionary and a
        dateutil.relativedelta.relativedelta object
        """
        lookup_dict = {
            "daily": rd(days=+1),
            "semi-weekly": rd(days=+3, hours=+12),
            "weekly": rd(weeks=+1),
            "bi-weekly": rd(weeks=+2),
            "monthly": rd(months=+1),
            "bi-monthly": rd(months=+2),
            "quarterly": rd(months=+3),
            "semi-annualy": rd(months=+6),
            "annually": rd(years=+1),
            "bi-annually": rd(years=+2)
        }
        if type(self.frequency) == str:
            try:
                delta_value = lookup_dict[self.frequency.lower()]
            except KeyError:
                raise KeyError("The object passed to the frequency " + \
                    "parameter is not a known value")
        elif type(self.frequency) == rd:
            delta_value = self.frequency
        elif type(self.frequency) == int:
            delta_value = td(days=self.frequency)
        else:
            raise ValueError("The object provided to the frequency " + \
                "parameter is not of a type understood")

        if not self.last_run:
            return 1
        elif (self.last_run + delta_value) <= dt.now().date():
            return 1
        elif (self.last_run + delta_value) > dt.now().date():
            sleep(((self.last_run + delta_value) - dt.now().date()).total_seconds())
            return 1
        else:
            return 0

    def check_iterations(self):
        """
        Checks to see if the value of the current_iteration variable is the
        same as the iterations parameter.  If this is the case it returns a
        value of 1.  Otherwise the current_iteration value is incremented
        and the method returns a value of 0.
        """
        if self.current_iteration == self.iterations:
            return 0
        else:
            return 1

    def check_stop_date(self):
        """
        Check the current date against the stop date.  If the date value is
        less than the stop date return 1 otherwise return 0.

        :return: 1 or 0
        """
        try:
            if dt.now().date() < dt.strptime(self.stop_date, "%Y/%m/%d").date():
                return 1
            else:
                return 0
        except ValueError:
            try:
                if dt.now().date() < dt.strptime(self.stop_date, "%y/%m/%d"):
                    return 1
                else:
                    return 0
            except ValueError:
                raise ValueError("The object supplied to the stop_date" + \
                    " parameter does not match the know datetime.strptime" + \
                    " patterns of either YYYY/MM/DD or YY/MM/DD")

    def check_time(self):
        """
        Compare the time to the specified trigger_time.  If the times match
        then return a 1. Otherwise sleep until the times match then return
        a 1.  If an error is encountered raise that error.

        :return: 1
        """
        try:
            if self.trigger_time == dt.now().strftime("%H:%M:%S"):
                return 1
            else:
                run_time_string = dt.now().date().strftime("%Y/%m/%d") + \
                    " " + self.trigger_time
                run_time = dt.strptime(run_time_string, "%Y/%m/%d %H:%M:%S")
                if run_time > dt.now():
                    sleep((run_time - dt.now()).total_seconds())
                else:
                    sleep((dt.now() - run_time).total_seconds())
                return 1
        except TypeError:
            raise TypeError("The trigger time value of {} does not " + \
                "follow the H:M:S 24hr clock time format".format(
                self.trigger_time))
        except ValueError as e:
            raise ValueError(e)

    def test_function(self, function):
        """
        Test to see if a function is passed to the function_to_run
        parameter.  If one is not, or the value passed is not a function,
        raise an error.

        :return: 1
        """
        if not self.function:
            raise ValueError(
                "No function_to_run provided to the timer function.")
        elif not isinstance(self.function,
            (FunctionType, BuiltinFunctionType, partial)):
            raise ValueError(
                "The object provided as the function_to_run parameter is\n" + \
                "not a method, funciton, or built-in function."
            )
        else:
            return 1

    def test_fail_check(self):
        """
        Test the fail_check and fail_check_responses parameters to see if
        they are valid options.

        :return: a value of one will be returned if the check succeeds.
        Otherwise a ValueError will be raised.
        """

        if self.fail_check and type(self.fail_check) == str:
            if not self.fail_check_responses:
                raise ValueError()
            elif type(self.fail_check_responses) == dict:
                return 1
            else:
                raise ValueError("The object passed to the " + \
                    "fail_check_responses was not a dictonary")
        else:
            if self.fail_check and type(self.fail_check != str):
                raise ValueError("The object passed to the fail_check " + \
                    "parameter was not a string")
            else:
                return 1
