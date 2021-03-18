import configparser
import os.path
from cbpro import AuthenticatedClient
########
# This file should be used by any other file that needs to import secret variables. 
# In otherwords, do not read secrets from any file but this one!
# I guess you can use the class vars to get secrets... maybe there's a way around this.
########

class SecretsManager():
    """
    This class is meant to handle anything sensitive in dcabot.
    Sensitive info such as secrets should be accessed only through this class.
    """

    def __init__(self, secrets_file="/home/mike/.dcabot_secrets"):
        self.secrets_file = secrets_file

        if(os.path.exists(self.secrets_file)):
            self.secrets = configparser.ConfigParser()
            self.secrets.read(self.secrets_file)
            self.smtp_username = self.secrets['email_secrets']['smtp_username']
            self.smtp_password = self.secrets['email_secrets']['smtp_password']
            self.api_key = self.secrets['coinbase_secrets']['api_key']
            self.api_secret = self.secrets['coinbase_secrets']['api_secret']
            self.api_password = self.secrets['coinbase_secrets']['api_password']
        else:
            raise FileNotFoundError(f"Could not find secrets file ({self.secrets_file})")

    def cbpro_auth_client(self):
        """
        Simply create and return the cbpro authenticated client.
        This should suffice for most usecases, since DCAbot doesn't need to maintain open connections.
        """
        return AuthenticatedClient(
            key=self.api_key,
            b64secret=self.api_secret,
            passphrase=self.api_password)

    def check_conffile_exists(self, filepath):
        """
        Verifies configuration is usable. Exits the program otherwise.
        This could probably turn into its own class, as methods to perform new checks  are added.
        """
        if (not os.path.exists(filepath)):
            print(f"ERROR: Could not find configuration file at ../etc/dcabot.conf. Exiting! (should ask to generate a new one)")
            print("There should be a program-closing exception here.")
            exit(1)
        else:
            return True






