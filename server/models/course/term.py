from sqlalchemy import UniqueConstraint, text

from base.base_model import BaseModel, db


class Term(BaseModel):
    __tablename__ = 'terms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)
    season = db.Column(db.String(10))
    section = db.Column(db.SmallInteger, default=1, server_default=text('1'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        UniqueConstraint('year', 'season', name='uq_year_season'),
    )

    def __repr__(self):
        return f'<Term {self.year} {self.season} {self.section}>'
