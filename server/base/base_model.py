from flask_sqlalchemy import SQLAlchemy

from utils.time import utcnow

# Initialize SQLAlchemy
db = SQLAlchemy()

class SoftDeleteQuery(db.Query):
    """ Custom query class that excludes is_deleted=True records by default """
    def only_deleted(self):
        """ Query only soft-deleted records """
        return self.filter_by(is_deleted=True)

    def with_deleted(self):
        """ Query all records, including soft-deleted ones """
        return self

    def not_deleted(self):
        """ Query only non-deleted records (default behavior) """
        return self.filter_by(is_deleted=False)

class BaseModel(db.Model):
    __abstract__ = True  # Indicate that this is an abstract base class
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    query_class = SoftDeleteQuery  # Use the custom query class

    create_time = db.Column(db.DateTime, default=utcnow)
    update_time = db.Column(db.DateTime, default=utcnow, onupdate=utcnow)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def save(self):
        """ Save the current object to the database """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kwargs):
        """ Update attributes of the current object """
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            self.update_time = utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self, soft=True):
        """ Soft delete (default) or hard delete """
        try:
            if soft:
                self.is_deleted = True
                self.update_time = utcnow()
            else:
                db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def restore(self):
        """ Restore a soft-deleted record """
        try:
            self.is_deleted = False
            self.update_time = utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def force_delete(self):
        """ Permanently delete the record """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def save_all(*instances):
        """ Save multiple objects at once """
        try:
            # tuple or list (o1, o2, o3) or [o1, o2, o3]
            if len(instances) == 1 and isinstance(instances[0], list):
                instances = instances[0]
            db.session.add_all(instances)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
