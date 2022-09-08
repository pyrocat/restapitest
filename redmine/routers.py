from loguru import logger

logger.add('db_router.log')


class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'auth', 'contenttypes', 'admin', 'authtoken', 'sessions', 'core'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'auth'
        return False

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        logger.info('Auth router writes')
        logger.info(f'  Now writing Model <{model}>')
        logger.info(f'  Model meta <{model._meta}>')

        if model._meta.app_label in self.route_app_labels:
            return 'auth'
        return False

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        logger.info('Auth router performing migration')
        logger.info(f'  Migrating DB <{db}> app label <{app_label}>')
        if app_label in self.route_app_labels:
            return db == 'auth'
        return False



class RedmineRouter():
    """
    A router to control all database operations on models in
    the redmine application
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on redmine app models to 'redmine' database
        """
        logger.info('Redmine router reads')
        logger.info(f'  Now reading Model <{model}>!')
        logger.info(f'  Model meta app label <{model._meta.app_label}>')

        if model._meta.app_label == 'redmine':
            return 'redmine'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on redmine app models to 'other'
        """
        logger.info('Redmine router writes')
        logger.info(f'  Now writing Model <{model}>')
        logger.info(f'  Model meta <{model._meta}>')
        logger.info(f'  This ultimately leads to None, the request slides to "default" and raises an error' )
        return None
        # if model._meta.app_label == 'redmine':
        #     logger.info(f'  Model meta.app_label is <{model._meta.app_label}> which must be redmine')
        #     return False # writing to 'redmine' not allowed /
        # # an attempt to do so will result in an exception if respective table is missing
        # # TODO clarify this behaviour, as it may lead to unpredictable results
        #
        # logger.info(f'  No, apparently, it is not redmine')


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Migrations are not allowed
        """
        logger.info('Redmine router performing migration')
        # logger.info(f'  Migrating DB <{db}> app label <{app_label}>')
        # if db == 'redmine' or app_label == 'redmine':
        logger.info('    no migrations allowed')
        return False

