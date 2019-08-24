from kivy.logger import Logger as KivyLogger
from kivy.utils import get_hex_from_color, escape_markup

COLORS  = {
    'info': (.3,1,.4,1),
    'warning': (1,1,0,1),
    'error': (1,.5,.2,1),
    }

class LoggerBase:

    def _format_log(self, log_type, msg):
        msg = msg.split(':',1) + ['']
        log_color = get_hex_from_color(COLORS[log_type])
        log_title = "[color=%s]&bl;[b]%-14s[/b]&br;[/color]  " \
            % (log_color, log_type.upper())
        if msg[1]:
            log_msg = "[%-18s] %s" % (msg[0], msg[1])
        else:
            log_msg = "%s" % msg[0]
        
        return log_title+log_msg

    def info(self, msg, log_out=False):
        log = self._format_log('info', msg)
        self._log_out(msg, log, 'info', log_out=log_out)
        
    def warning(self, msg, log_out=False):
        log = self._format_log('warning', msg)
        self._log_out(msg, log, 'warning', log_out=log_out)

    def error(self, msg, log_out=False):
        log = self._format_log('error', msg)
        self._log_out(msg, log, 'error', log_out=log_out)

    def _log_out(self, msg, log, log_type, log_out=False):
        from kivystudio.components.codeplace import terminal
        terminal.logger.log(log)
        if log_out:
            getattr(KivyLogger, log_type)(msg)

    def clear_logs(self):
        from kivystudio.components.codeplace import terminal
        terminal.logger.clear_logs()

Logger = LoggerBase()

from kivy.clock import mainthread
@mainthread
def test_log(*args):
    Logger.info('KivyStudio: sdsdsdsds')
    Logger.info('sdsdsdsds')
    Logger.warning('KivyStudio: sdsdsdsds')
    Logger.warning('sdsdsdsds')
    Logger.error('KivyStudio: sdsdsdsds')
    Logger.error('sdsdsdsds')
test_log()