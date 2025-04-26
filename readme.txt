run the backend
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


github:https://github.com/Hamabi-Minami/MyBlog

vercel:https://my-blog-delta-beryl.vercel.app

AWS cloud Backend API Docs:http://3.99.168.182:8000/docs#/
