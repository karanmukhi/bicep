import os
from configparser import ConfigParser


def getConfig(filename=None, section="trainer_one"):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), "database_config.ini")
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    params = parser.items(section)
    try:
        for param in params:
            db_config[param[0]] = param[1]
    except:
        raise Exception("Error in database_config")
    try:
        db_config["password"] = os.environ["TR_AI_NER_POSTGRES_PASSWORD"]
    except:
        raise Exception(
            "Need TR_AI_NER_POSTGRES_PASSWORD as environment variable\nTry:\nexport TR_AI_NER_POSTGRES_PASSWORD='password'"
        )
    db_config["host"] = os.environ.get("POSTGRES_HOST", db_config.get("host", "localhost"))
    return db_config
