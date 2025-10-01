
import configparser

config = configparser.RawConfigParser()
config.read(".\\Configurations\\config.ini")

class ReadConfig:

    @staticmethod
    def getURL(region):
        """Get URL for the given region (AP, ME, US, EU)"""
        return config.get(region, "baseURL")

    @staticmethod
    def getClientID(region):
        """Get client ID for the given region"""
        return config.get(region, "clientID")

    @staticmethod
    def getUsername(region):
        """Get username for the given region"""
        return config.get(region, "username")

    @staticmethod
    def getPassword(region):
        """Get password for the given region"""
        return config.get(region, "password")
