# Copyright 2015 Jared Rodriguez (jared.rodriguez@rackspace.com)
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
import threading
import time
import zmq

from mercury.rpc.ping2 import ping as ping2


RETRIES = 5  # TODO: YAML
PING_TIMEOUT = 2500  # TODO: YAML
BACK_OFF = .42


log = logging.getLogger(__name__)


def ping(ctx, host):

    failures = 0

    result = False
    while failures < RETRIES:
        _timeout = int((PING_TIMEOUT + (failures and PING_TIMEOUT or 0) * (failures**BACK_OFF)))
        result = ping2(ctx, host, timeout=_timeout)
        if result:
            break
        failures += 1

    return result


def pinger(server, mercury_id, db_controller):
    ctx = zmq.Context()
    while True:
        log.debug('Pinging %s : %s' % (mercury_id, server))
        result = ping(ctx, server)
        if not result:
            break
        time.sleep(5)  # TODO: YAML
    # Scan jobs for any tasks targeting this node
    #  1. Fail the task
    #  2. Signal to any active worker threads to stop processing the task
    log.info('%s : %s ping timeout' % (mercury_id, server))
    # log.debug('Attempting to destroy thread 0mq context')
    # ctx.destroy()  ## HANGS!!!!
    # log.debug('Context destroyed')
    db_controller.delete(mercury_id)  # Threads persist


def spawn(server, mercury_id, db_controller):
    thread = threading.Thread(target=pinger, args=[server, mercury_id, db_controller])
    log.info('Spawning pinger thread: %s : %s' % (mercury_id, server))
    thread.start()

