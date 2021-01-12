from app import app
from datetime import timedelta
 
#make page fresh regularly
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.run(debug=True)
