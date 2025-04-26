
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    # Relationships
    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref=backref("children", cascade="all, delete-orphan"))
