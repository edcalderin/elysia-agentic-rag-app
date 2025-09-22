import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import sys

FILE_NAME = "sample_data.csv"

class WeaviateDataLoader:
    def __init__(self):
        load_dotenv()

        self.weaviate_url = os.getenv("WEAVIATE_URL")
        self.weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
        self.client = self.connect_to_weaviate()
        self.data_dir = Path("data")
        self.data_dict = self.load_data()
        self.movies = self.client.collections.use(os.getenv("COLLECTION_NAME"))

    def connect_to_weaviate(self):
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=self.weaviate_url,
            auth_credentials=Auth.api_key(self.weaviate_api_key),
        )
        print(
            "✅ Connection established"
            if client.is_ready()
            else "❌ Error connecting"
        )
        return client

    def load_data(self) -> list[dict]:
        data = pd.read_csv(self.data_dir / FILE_NAME)
        print(f"Data size: {sys.getsizeof(data) / 2048:.2f} mb")
        return data.to_dict(orient="records")

    def import_data(self):
        with self.movies.batch.fixed_size(batch_size=200) as batch:
            for record in self.data_dict:
                batch.add_object(
                    {
                        # "id": d["id"],
                        "title": record["title"],
                        "vote_average": record["vote_average"],
                        "vote_count": record["vote_count"],
                        "status": record["status"],
                        "release_date": record["release_date"],
                        "revenue": record["revenue"],
                        "runtime": record["runtime"],
                        "adult": record["adult"],
                        "backdrop_path": record["backdrop_path"],
                        "budget": record["budget"],
                        "homepage": record["homepage"],
                        "imdb_id": record["imdb_id"],
                        "original_language": record["original_language"],
                        "original_title": record["original_title"],
                        "overview": record["overview"],
                        "popularity": record["popularity"],
                        "poster_path": record["poster_path"],
                        "tagline": record["tagline"],
                        "genres": record["genres"],
                        "production_companies": record["production_companies"],
                        "production_countries": record["production_countries"],
                        "spoken_languages": record["spoken_languages"],
                        "keywords": record["keywords"],
                    }
                )
                if batch.number_errors > 10:
                    print("Batch import stopped due to excessive errors.")
                    break

        failed_objects = self.movies.batch.failed_objects
        if failed_objects:
            print(f"Number of failed imports: {len(failed_objects)}")
            print(f"First failed object: {failed_objects[0]}")

    def close_connection(self):
        self.client.close()  # Free up resources


if __name__ == "__main__":
    loader = WeaviateDataLoader()
    loader.import_data()
    loader.close_connection()
