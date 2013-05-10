#!/usr/bin/env python
#
# NRPE plugin to monitor connections established
#
# Script by Jesus Armando Uch jahrmando@gmail.com
#
# Website: https://github.com/jahrmando
#
# Usage: ./check_netstat.py -w [value] -c [value]
#
import pynagios
from pynagios import Plugin, Response
import subprocess


class CkeckNetstat(Plugin):

    def numEstablish(self):
        try:
            cmd = "/bin/netstat -tua --numeric | /bin/grep -oP 'ESTABLISHED' | wc -l"
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_value, stderr_value = proc.communicate()
            if not stderr_value:
                value = int(stdout_value)
                result = self.response_for_value(value, "%s Connections established" % value)
                result.set_perf_data("Connections", value, "", self.options.warning, self.options.critical, 0, 1024)
                return result
            else:
                return Response(pynagios.UNKNOWN, "Plugin failed!")
        except Exception:
            return Response(pynagios.UNKNOWN, "Plugin failed!")

if __name__ == '__main__':
    CkeckNetstat().numEstablish().exit()
