var express = require('express');
var app = express();


app.get('/', function (req,res) {
    res.send('Hello Express');
});

app.listen(8000, () => 
    console.log('Express is ready at http://localhost:8000')
);
