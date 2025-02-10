import sys
sys.path.append('./app/')

# import application
from main import app as application, main

# run app
try:
    main()
except Exception:
    pass
