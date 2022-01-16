import sys
import os
from app.server import server

if __name__ == "__main__":
    foo = server.DevServer()
    foo.run()