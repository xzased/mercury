#
# Press plugin will add hooks for init, layout, download, and post. The hooks
# will update the mercury task with a progress delta and a custom action.
#
# The press 'complete' (or error) event will be handled by the native press
# orchestrator.

import logging

from mercury.agent.client import BackEndClient

log = logging.getLogger(__name__)


def get_mercury_configuration(press_configuration):
    """
    Validates and returns our mercury configuration
    :param press_configuration: The full press configuration
    :return: (dict) mercury_configuration
    """
    required = ['task_id', 'backend_zurl']
    try:
        mercury_configuration = press_configuration['mercury']
    except KeyError:
        log.error('Mercury section is missing from press configuration')
        return

    missing = []
    for key in required:
        if key not in mercury_configuration:
            missing.append(key)

    if missing:
        log.error('Mercury configuration is missing: {}'.format(missing))
        return

    return mercury_configuration


class MercurySpecialLoggingHandler(logging.Handler):
    def __init__(self, backend_client, task_id):
        super(MercurySpecialLoggingHandler, self).__init__()
        self.backend_client = backend_client
        self.task_id = task_id

    def emit(self, record):
        if hasattr(record, 'press_event'):
            log.debug('Press Event: {}'.format(record.press_event))
            self.backend_client.task_update(
                {'task_id': self.task_id,
                 'action': 'Press: ' + record.press_event,
                 'progress': 0.5  # TODO: press event to progress map
                 }
            )


def plugin_init(configuration):
    log.info('Mercury plugin initialization')
    mc = get_mercury_configuration(configuration)
    if not mc:
        log.info('Mercury configuration missing from Press configuration')
        return

    backend_client = BackEndClient(mc['backend_zurl'])
    task_id = mc['task_id']

    root_logger = logging.getLogger('')
    root_logger.addHandler(MercurySpecialLoggingHandler(backend_client, task_id))
