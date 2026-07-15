from fastapi import FastAPI

from db.session import veritabanini_olustur
from data_models.user import User
from data_models.post import Post
from data_models.comment import Comment
from data_models.clap import Clap
from data_models.follow import Follow
from data_models.tag import Tag
from data_models.post_tag_link import PostTagLink

from routers import auth, user, post, comment, clap, follow, tag

app = FastAPI(title="Medium Clone API")


@app.on_event("startup")
def startup():
    veritabanini_olustur()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(clap.router)
app.include_router(follow.router)
app.include_router(tag.router)