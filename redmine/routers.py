class RedmineRouter(object):
    """
    A router to control all database operations on models in
    the redmine application
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on redmine app models to 'redmine' database
        """
        if model._meta.app_label == 'redmine':
            return 'redmine'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on redmine app models to 'other'
        """
        if model._meta.app_label == 'redmine':
            return 'default' # writing to 'redmine' not allowed /
        # an attempt to do so will result in an exception if respective table is missing
        # TODO clarify this behaviour, as it may lead to unpredictable results
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the 'redmine' app only appears on the 'other' db
        """
        if db == 'redmine':
            return model._meta.app_label == 'redmine'
        elif model._meta.app_label == 'redmine':
            return False
        return None