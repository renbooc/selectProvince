# Vercel Serverless Function Entry Point
from app import app

# Vercel will automatically handle the request/response conversion
# when using the @vercel/python builder
app_handler = app