# Albanian News Classifier

You can classify news articles from our supported categories:<br><strong>Sport, Teknologji, Politike, Ekonomi, Shqiperi, Sociale, Show Biz, Bota, Finance, Kosova, Kulture, Rajoni</strong>


## How to run it
```
docker build -t news_classify . && docker run --rm -it -p 5000:5000 news_classify
```

Navigate to: [localhost:50000](http://localhost:5000)