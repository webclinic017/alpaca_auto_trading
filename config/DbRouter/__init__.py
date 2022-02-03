class DroidRouters:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    model_droid = {
        'universe'
    }


    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.db_table in self.model_droid:
            return 'droid'
        return 'default'

