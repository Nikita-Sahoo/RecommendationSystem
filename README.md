# RecommendationSystem


This project presents a Content-Based Music Recommendation System designed to suggest songs based on their metadata and content features, such as genre, artist, mood, and ratings. Using deep learning techniques like TF-IDF and autoencoders, the system learns user preferences and recommends songs that are semantically similar to the provided content or searched.

Introduction :
With the rapid growth of digital music libraries, recommending relevant songs to users has become both a challenge and a necessity. This project focuses on building a Content-Based Music Recommendation System that suggests similar songs based on audio metadata and textual descriptions such as genre, artist, mood, and ratings. The system aims to enhance user experience by recommending songs that align with their preferences without relying on other users' behavior.


Methodology
a. Data Collection
  • Collected metadata for songs (title, artist, genre, mood, etc.)
  • Ratings or user preferences included for enhanced filtering.
b. Data Cleaning
  • Remove Missing Values
    o Drop or impute rows with missing values in critical columns and Fill missing values with default values
  • Remove Duplicates
    o Identify and remove duplicate songs based on title + artist combination to avoid redundancy.
  • Standardize Text Data
    o Convert all text to lowercase (e.g., rock and Rock become the same).
    o Strip extra spaces, special characters, and inconsistent formatting in fields like genre or artist name.
  • Handle Multi-Genre Fields
    o Split multi-genre entries (e.g., "pop, dance") into separate tags or lists for proper vectorization.
  • Tokenize and Clean Metadata
    o Remove stop words or unhelpful words ("the", "feat.", "official") from description or title fields.
    o Apply stemming.
  • Convert Categorical to Numeric
    o Encode categorical fields (like mood or genre) using TF-IDF for vectorization.
c. Feature Engineering
  • Used TF-IDF to convert song metadata into numerical vectors.
  • Combined this with ratings to form a hybrid feature vector.
d. Modeling
  • Implemented a deep autoencoder to learn compressed representations of songs.
  • Calculated cosine similarity between encoded songs to find the most similar tracks.
e. Recommendation Process
  • When a user selects or likes a song, the system returns top 6 similar songs.

  
