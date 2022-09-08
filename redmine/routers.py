from loguru import logger

logger.add('db_router.log')


class RedmineRouter():
    """
    A router to control all database operations on models in
    the redmine application
    """

    def db_for_read(self, model, **hints):
        """
        Point all Read operations on redmine app models to 'redmine' database
        """
        logger.info('Redmine router reads')
        logger.info(f'  Now reading Model <{model}>!')
        logger.info(f'  Model meta app label <{model._meta.app_label}>')
        if model._meta.app_label == 'redmine':
            return 'redmine'
        return None  # forwarded to "default"

    def db_for_write(self, model, **hints):
        """
        Restrict all Write operations on redmine app models.
        """
        logger.info('Redmine router writes')
        logger.info(f'  Now writing Model <{model}>')
        logger.info(f'  Model meta <{model._meta}>')
        if model._meta.app_label == 'redmine':
            raise PermissionError
        return None  # forwarded to "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Migrations allowed to all models except for redmine
        """
        logger.info('Redmine router performing migration')
        logger.info(f'  Migrating DB <{db}> app label <{app_label}>')
        if db == 'redmine' or app_label == 'redmine':
            logger.info('    no migrations to redmine allowed')
            return False
        return None  # forwarded to "default"

