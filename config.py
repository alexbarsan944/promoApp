from datetime import timedelta

SESSION_COOKIE_SAMESITE = None
PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
MONGO_URI = 'mongodb://user:DBpassword*@cluster0-shard-00-00.ymxkw.mongodb.net:27017,' \
            'cluster0-shard-00-01.ymxkw.mongodb.net:27017,' \
            'cluster0-shard-00-02.ymxkw.mongodb.net:27017/promoApp?ssl=true&replicaSet=atlas-t0m0wu-shard-0' \
            '&authSource=admin&retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE'
