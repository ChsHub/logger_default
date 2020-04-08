from datetime import datetime
from logging import DEBUG, INFO, getLogger, info, StreamHandler, Formatter, FileHandler
from os import mkdir, listdir, getpid
from os.path import join, exists, abspath, split
from sys import executable, stdout

from send2trash import send2trash


def get_clean_date():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")  # 2019-03-19 19_50_48_200077


class Logger:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def __init__(self, max_logfile_count=30, debug=False, child=False):
        """
        Set log name and formatters, create directory if necessary
        :param max_logfile_count: Maximum number of files to be kept in log file directory
        :param debug: If true, print log messages to console
        :param child: If true, creates no new log file, and appends log messages to  the last written log file
        """

        logger = getLogger()
        logger.setLevel(INFO)

        logging_path = self._get_log_path()
        if not exists(logging_path):
            mkdir(logging_path)
        self.log_name = self.delete_old_logs(logging_path, max_logfile_count)

        if self.log_name and child:
            self.log_name = join(logging_path, self.log_name[-1])
        else:
            self.log_name = join(logging_path, get_clean_date() + '.log')

        if child:
            self._add_handler(logger, FileHandler(self.log_name, "a", encoding='utf-8', delay="true"),
                              'PID%s ' % getpid())
        else:
            self._add_handler(logger, FileHandler(self.log_name, "w", encoding='utf-8', delay="true"))

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
    def _get_log_path():
        logging_path = abspath(executable)
        logging_path, exe = split(logging_path)
        if exe != 'python.exe':
            exe = 'log_files'
            logging_path = join(logging_path, exe)
        else:
            logging_path = 'log_files'

        return logging_path

    @staticmethod
    def delete_old_logs(logging_path, max_count_logfiles):
        dir_list = listdir(logging_path)
        dir_list = list(filter(lambda x: x.endswith(".log"), dir_list))

        for file in dir_list[:-max_count_logfiles]:
            send2trash(join(logging_path, file))

        return dir_list

    def shutdown(self):
        info(self.log_name)
