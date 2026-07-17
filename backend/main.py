from fastapi import FastAPI

from db.session import veritabanini_olustur
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, user, post, comment, clap, follow, tag

app = FastAPI(title="Medium Clone API")


@app.on_event("startup")
def startup():
    veritabanini_olustur()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(clap.router)
app.include_router(follow.router)
app.include_router(tag.router)