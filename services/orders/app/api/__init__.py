import logging
import traceback

from flask import current_app, url_for
from flask_restplus import Api

from app.exceptions import NoResultFound, IntegrityError, StorageError

log = logging.getLogger(__name__)


class Custom_API(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)


rest_api = Custom_API(version='1.0', title='Orders API', doc='/doc/',  # doc=None,
                      description='documentation of orders micro-service')


@rest_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config['DEBUG']:
        return {'message': message}, 500


def default_error_handler_func(error):
    if current_app.config['DEBUG']:
        log.warning(traceback.format_exc())
    return {'message': error.message}, error.status_code


@rest_api.errorhandler(NoResultFound)
def database_not_found_error_handler(error):
    """resource not found"""
    return default_error_handler_func(error)


@rest_api.errorhandler(IntegrityError)
def integrity_error_handler(error):
    """data integrity error"""
    return default_error_handler_func(error)


@rest_api.errorhandler(StorageError)
def integrity_error_handler(error):
    """database error"""
    return default_error_handler_func(error)
