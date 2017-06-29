if(!global['App']) {
    global.App = {};
}

var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var nodeCleanup = require('node-cleanup');
var dbClient = require('mongodb').MongoClient;

dbClient.connect("mongodb://localhost:27017/news_scraper", function(err, db) {
  if(err) 
	return console.dir(err); 
  else 
	global.App.db = db;

});


var path = require('path');

var router = express.Router()

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

router.get('/', function(req, res) {
    res.json({ message: 'hooray! welcome to our api!' });   
});

router.get('/mostRecent' , function(req, res) {
	db = global.App.db;
	data = db.col.find().sort({"_id": -1}).limit(1).pretty();
	res.json(data);
	
});

router.get('/oneWeek' , function(req, res) {
        db = global.App.db;
        data = db.col.find().sort({"_id": -1}).limit(1).pretty();
        print(r);
        res.json(data);

});

router.get('/twoWeeks' , function(req, res) {
        db = global.App.db;
        data = db.col.find().sort({"_id": -1}).limit(1).pretty();
        print(r);
        res.json(data);

});

router.get('/threeWeeks' , function(req, res) {
        db = global.App.db;
        data = db.col.find().sort({"_id": -1}).limit(1).pretty();
        print(r);
        res.json(data);

});

router.get('/fourWeeks' , function(req, res) {
        db = global.App.db;
        data = db.col.find().sort({"_id": -1}).limit(1).pretty();
        print(r);
        res.json(data);

});

router.get('/custom' , function(req, res) {
        db = global.App.db;
        data = db.col.find().sort({"_id": -1}).limit(1).pretty();
        print(r);
        res.json(data);

});


app.use(express.static(path.join(__dirname, 'ui')));

app.use('/api', router);

app.listen(9950);

nodeCleanup(function (exitCode, signal) {
    // release resources here before node exits 

    global.App.db.close();
});
