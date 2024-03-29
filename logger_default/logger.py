from datetime import datetime
from logging import DEBUG, INFO, getLogger, info, StreamHandler, Formatter, FileHandler
from os import listdir, getpid, access, W_OK
from os.path import split, expandvars
from pathlib import Path
from sys import executable, stdout

def get_clean_date():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")  # 2019-03-19 19_50_48_200077


class Logger:
    """
    Set up file logging
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def __init__(self, max_logfile_count=30, debug=False, child=False, log_directory: str = 'log_files'):
        """
        Set log name and formatters, create directory if necessary
        :param max_logfile_count: Maximum number of files to be kept in log file directory
        :param debug: If true, print log messages to console
        :param child: If true, creates no new log file, and appends log messages to  the last written log file
        :param log_directory: Log directory name
        """

        logger = getLogger()
        logger.setLevel(INFO)

        logging_path = self._get_log_path(log_directory)
        self.log_name = self.delete_old_logs(logging_path, max_logfile_count)

        if self.log_name and child:
            self.log_name = Path(logging_path, self.log_name[-1])
        else:
            self.log_name = Path(logging_path, get_clean_date() + '.log')

        if child:
            self._add_handler(logger, FileHandler(self.log_name, mode="a", encoding='utf-8', delay="true"),
                              'PID%s ' % getpid())
        else:
            self._add_handler(logger, FileHandler(self.log_name, mode="w", encoding='utf-8', delay="true"))

        if debug:
            # create console handler
            self._add_handler(logger, StreamHandler(stdout))

    def _add_handler(self, logger, handler, pid=''):
        handler.setLevel(DEBUG)
        format = '%(levelname)s: ' + pid + '%(asctime)s %(filename)s:\t%(funcName)s():\t%(lineno)d:\t%(message)s'

        formatter = Formatter(format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @staticmethod
    def _get_log_path(_log_directory: str) -> Path:
        """
        Get path for saving logs
        :param _log_directory: Directory name
        :return: Full directory path
        """
        logging_path = Path(executable).resolve()
        logging_path, exe = split(logging_path)
        if exe in ('python.exe', 'pythonw.exe'):  # Don't log to python directory
            logging_path = Path(_log_directory).resolve()
        else:
            logging_path = Path(logging_path, _log_directory)
            

        logging_path = Path('.', logging_path).absolute()

        if not access(logging_path, W_OK): # If writing access is denied, make directory in AppData/Roaming
            # WINDOWS ONLY
            app_data_path = Path(expandvars('%APPDATA%')).resolve()
            if not app_data_path.exists():
                raise FileNotFoundError
            logging_path = Path(app_data_path, *logging_path.parts[-2:])

        logging_path.mkdir(parents=True, exist_ok=True)
        return logging_path

    @staticmethod
    def delete_old_logs(logging_path: Path, max_count_logfiles: int) -> list:
        """
        Delete old log files in directory
        :param logging_path: Logging path
        :param max_count_logfiles: Number of log files to be kept
        :return: List of logging files
        """
        dir_list = listdir(logging_path)
        dir_list = list(filter(lambda x: x.endswith(".log"), dir_list))

        for file in dir_list[:-max_count_logfiles]:
            Path(logging_path, file).unlink(missing_ok=True)

        return dir_list

    def shutdown(self):
        info(self.log_name)
