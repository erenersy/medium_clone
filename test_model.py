from sqlmodel import SQLModel, create_engine
from data_models.user import User
from data_models.post import Post
from data_models.comment import Comment
from data_models.clap import Clap
from data_models.follow import Follow
from data_models.tag import Tag
from data_models.post_tag_link import PostTagLink

engine = create_engine("sqlite:///test.db")
SQLModel.metadata.create_all(engine)
print("Tüm tablolar başarıyla oluşturuldu!")