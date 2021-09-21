var express = require("express");
var app = express();

app.use(express.urlencoded({ extended: true }))
app.use(express.json());

const { MongoClient,ObjectId } = require('mongodb');
var url = "mongodb://localhost:27017/";

app.get("/",(req,res)=>{
    res.send("successfull")
})
//insertone
app.post("/insert",(req,res)=>{
    MongoClient.connect(url,function(err,conn){
        var db = conn.db("user_profile");
        db.collection("users").insertOne(req.body,function(err,data){
            res.send(data)
        })
    })
})


//bulk insert

app.post("/bulkinsert",(req,res)=>{
    MongoClient.connect(url,function(err,conn){
        var db = conn.db("user_profile");
        db.collection("users").insertMany(req.body,function(err,data){
            res.send(data)
        })
    })
})

//update
app.patch("/update/:id",(req,res)=>{
    MongoClient.connect(url,function(err,conn){
        var db = conn.db("user_profile");
        db.collection("users").updateOne(
            {_id:ObjectId(req.params.id)},
            {$set:req.body},(err,data)=>{
                res.send(data)
            })
        
    })
})

//delete
app.get("/delete/:id",(req,res)=>{
    MongoClient.connect(url,function(err,conn){
        var db = conn.db("user_profile");
        db.collection("users").findOneAndDelete({_id:ObjectId(req.params.id)},(err,data)=>{
            res.send(data)
        })
        
    })
})

//read

app.get('/user/:id',(req,res) => {
    MongoClient.connect(url,(err,conn) => {
        var db = conn.db('user_profile');        
        db.collection('users').find({_id : ObjectId(req.params.id)}).toArray((err,data) => {
            console.log(data);
          res.send(data)        
        })    
    })
})

//list view

app.get('/userlist',(req,res) => {
    MongoClient.connect(url,(err,conn) => {
        var db = conn.db('user_profile');        
        db.collection('users').find().toArray((err,data) => {
            console.log(data);
          res.send(data)        
        })    
    })
})

app.listen(7060,()=>{console.log("listening on 7060");})