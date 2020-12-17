import os
from configparser import ConfigParser


def getConfig(filename="config/database_config.ini", section="trainer_one"):
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
            "Need TR_AI_NER_POSTGRES_PASSWORD as environment variablen\nTry:\nexport TR_AI_NER_POSTGRES_PASSWORD='password'"
        )
    return db_config
