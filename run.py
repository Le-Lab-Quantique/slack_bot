import os

from src import web, setup_web_app 

if __name__ == "__main__":
    web_app = setup_web_app() 
    web.run_app(web_app)
