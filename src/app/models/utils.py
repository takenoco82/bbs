from dateutil import tz

from app.database import db


class AwareDateTime(db.TypeDecorator):
    '''Results returned as aware datetimes, not naive ones.

    https://stackoverflow.com/questions/23316083/sqlalchemy-how-to-load-dates-with-timezone-utc-dates-stored-without-timezone
    '''

    impl = db.DateTime

    def process_result_value(self, value, dialect):
        return value and value.replace(tzinfo=tz.UTC)
