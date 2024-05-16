from housing_finder_app.__ini__ import create_app
import os
from dotenv import load_dotenv


load_dotenv(".env")

app = create_app(settings_module=os.getenv("CONFIGURATION_SETUP"))


if __name__ == '__main__':
    app.run(debug=True, port=5003)