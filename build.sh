docker build -t sentiment_analysis_app .
docker images
docker run -p 8080:7860 --name sentiment_analysis_app image_id
# docker run -p 8080:7860 -d sentiment_analysis_app
docker ps