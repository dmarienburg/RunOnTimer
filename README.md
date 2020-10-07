# RunOnTimer

## A library for automating tasks

The timer library is built to allow a user to set an interval and the function
will run a method/function provided as a parameter at that interval.

***

## Updates

***

### v.0.6 - 2020-10-07 - Fixed kwargs["params"]

* The create_class_vars now correctly assings values from the kwargs["params"] to the self.params class variable
* All calls to **self.kwargs["params"] have been replaced with calls to self.params
* Checks have been added to call the self.function with or without params depending on if they exist or not

### v.0.5.3 - 2020-05-06 - Expanded docstrings

* Added to the doc strings to explain how parameters are passed to the target function
* Added examples of usage to the docstrings

### v.0.5.2 - 2020-05-06 - Testing Fixes

* Various bug fixes as a result of testing

### v.0.5.1 - 2020-05-05 - Bug Hunting

* Lots of small changes to the format of the code
  * Switched from explicit keyword arguments to just using a kwargs call
* Fixed calls that check the stop_date so that they actually function
* Replaced usage of timedelta with relativedelta where the later actually provides the intended functionality
* Reformatted the docstrings (I'll probably do this 50 more times because I'm obsessive about things that don't really matter)
* Have begun testing
  * probably should add a valid time interval that is shorter than a day so that I can test in a reasonable timeframe
  * an alternative, and probably better option would be to also add logging so I can just run a bunch of tests in different instances then view the output to check for errors
* Have recruited a contributor - Hi Will

### v.0.5 - 2020-05-04 - added the calls needed to run the provided function

* Altered return values of methods to be consistent.  1 is continue 0 is end.
* Lots of logical checks to see which of the optional parameters are being used.  There is probably a better way to do this.
* Testing is still needed but this is very close to v.1.0

### v.0.4 - 2020-05-04 - Added a time_check method

* New method checks to make sure the functions are running at their assigned trigger time.

### v.0.3 - 2020-05-04 - Added more checking to clearly identify sources of errors

* Lots of type checking on the params to make sure they are matching the required types.

### v.0.2 - 2020-05-04 - re-envisioned as a class

* I realized that this will work better as a class simply for readability.

### v.0.1 - 2020-05-04 - Initial version

* Just the first bits going in here.  Basic structure and ideas
