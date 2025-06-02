from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_USER: str
    MONGO_PASSWORD: str

    COLLECTION: str
    DATABASE: str

    model_config = SettingsConfigDict(env_file='.env')

    @property
    def MONGO_URI(self) -> str:
        uri = (f"mongodb+srv://{self.MONGO_USER}:{self.MONGO_PASSWORD}@cluster0.qopigct.mongodb.net/"
               f"?retryWrites=true&w=majority&appName=Cluster0")
        return uri


settings = Settings()
