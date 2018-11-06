import logging
import traceback

from flask import current_app, url_for
from flask_restplus import Api

from app.exceptions import NoResultFound

log = logging.getLogger(__name__)


class Custom_API(Api):
    @property
    def specs_url(self):
        '''
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        '''
        return url_for(self.endpoint('specs'), _external=False)


rest_api = Custom_API(version='1.0', title='Orders API', doc=None,
                      description='documentation of orders micro-service')


@rest_api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config['FLASK_DEBUG']:
        return {'message': message}, 500


@rest_api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    """resource not found"""
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
