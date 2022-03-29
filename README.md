# logger_default
Package for setting up logging files. Messages are saved to a new directory.

## Usage Example

Start logging and log messages:
 ```
    from logger_default import Logger
    from logging import info, error, exception

    with Logger():
        info('Info message')
        error('Error message')
        exception('Exception message')
```
Print messages to stdout as well:
```
    with Logger(debug=True):
```
