from fastapi import FastAPI

from db.session import veritabanini_olustur

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