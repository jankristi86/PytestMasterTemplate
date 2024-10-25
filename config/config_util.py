from config import config_logging

log = config_logging.config_root(__name__)


class ConfigUtil(object):

    @staticmethod
    def get_app_url(base_url=None, port_number="10005"):
        base_url = "http://localhost:" + port_number
        log.info("*********")
        log.info(base_url)
        log.info("********")
        return base_url
