from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from utils.time import utcnow

# Initialize SQLAlchemy
db = SQLAlchemy()


def db_execute(sql, params=None):
    session = sessionmaker(bind=db.engine)()
    try:
        cursor = session.execute(text(sql), params)
        if sql.strip().lower().startswith("select"):
            columns = cursor.keys()  # Get column names
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return rows
        else:
            session.commit()
            return cursor.rowcount
    except Exception as e:
        print(f"ExecuteSqleError: {e}")
        session.rollback()
        raise e
    finally:
        session.close()


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

    create_time = db.Column(db.DateTime, default=utcnow, server_default=text('CURRENT_TIMESTAMP'))
    update_time = db.Column(db.DateTime, default=utcnow, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    is_deleted = db.Column(db.Boolean, default=False, server_default=text('0'), nullable=False)

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

    def dict(self, exclude=None, include=None, include_relationships=False):
        """
        Converts the SQLAlchemy model instance to a dictionary.

        :param exclude: List of field names to exclude from the output.
        :param include: List of field names to include (only these fields will be returned).
        :param include_relationships: If True, include related objects (requires relationships to be defined).
        :return: Dictionary representation of the model.
        """
        # Convert all table columns to a dictionary
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        # Convert datetime fields to ISO format
        for key, value in data.items():
            import datetime
            if isinstance(value, datetime.datetime):
                data[key] = value.isoformat()

        # Exclude specified fields
        if exclude:
            for field in exclude:
                data.pop(field, None)

        # Include only specified fields
        if include:
            data = {k: v for k, v in data.items() if k in include}

        # Include relationship fields if enabled
        if include_relationships:
            for rel in self.__mapper__.relationships.keys():
                related_obj = getattr(self, rel)
                if related_obj is not None:
                    if isinstance(related_obj, list):  # One-to-many relationship
                        data[rel] = [obj.to_dict() for obj in related_obj]
                    else:  # One-to-one relationship
                        data[rel] = related_obj.to_dict()

        return data
