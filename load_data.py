import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import sys

load_dotenv()

# Best practice: store your credentials in environment variables
weaviate_url = os.getenv("WEAVIATE_URL")
weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

print("✅ Connection established" if client.is_ready() else "❌ Error connecting :(")

data_dir = Path("data")
data = pd.read_csv(data_dir / "sample_movies.csv")
print(f"Data size: {sys.getsizeof(data) / 2048:.2f} mb")
data_dict = data.to_dict(orient="records")

movies = client.collections.use("SampleMovies2024")

with movies.batch.fixed_size(batch_size=200) as batch:
    for d in data_dict:
        batch.add_object(
            {
                # "id": d["id"],
                "title": d["title"],
                "vote_average": d["vote_average"],
                "vote_count": d["vote_count"],
                "status": d["status"],
                "release_date": d["release_date"],
                "revenue": d["revenue"],
                "runtime": d["runtime"],
                "adult": d["adult"],
                "backdrop_path": d["backdrop_path"],
                "budget": d["budget"],
                "homepage": d["homepage"],
                "imdb_id": d["imdb_id"],
                "original_language": d["original_language"],
                "original_title": d["original_title"],
                "overview": d["overview"],
                "popularity": d["popularity"],
                "poster_path": d["poster_path"],
                "tagline": d["tagline"],
                "genres": d["genres"],
                "production_companies": d["production_companies"],
                "production_countries": d["production_countries"],
                "spoken_languages": d["spoken_languages"],
                "keywords": d["keywords"],
            }
        )
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = movies.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close()  # Free up resources
