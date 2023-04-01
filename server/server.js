const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const {Server} = require("socket.io");
const io = new Server(server);
const redis = require('redis');
const pg = require('pg')
const helpers = require('./helpers')
var bodyParser = require('body-parser')

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

require('dotenv').config()


const postgresClient = new pg.Client({
    host: process.env.PG_HOST,
    port: process.env.PG_PORT,
    user: process.env.PG_LOGIN,
    password: process.env.PG_PASSWORD,
    database: process.env.PG_DATABASE
})
postgresClient.connect()

let connections = []

const init_redis = async () => {

    const client = redis.createClient();
    const subscriber = client.duplicate();
    await subscriber.connect();

    await subscriber.subscribe('edota_frame', (message) => {
        connections.forEach(socket => {
            socket.emit('frame', message)
        })
    });
    await subscriber.subscribe('victory', (side) => {
        connections.forEach(socket => {
            socket.emit('victory', {"side": side})
        })
    });

}

init_redis()

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/', async (req, res) => {
    // check data
    for (var i = 1; i <= 5; i+=1) {
        if (!req.body["name" + i] || !req.body["code" + i]) {
            console.log(i, req.body)
            res.redirect('/')
        }
    }

    for (var j = 1; j <= 5; j++) {
        var code = req.body["code" + j]
        var name = req.body["name" + j]

        const q = {
            text: "UPDATE players SET code = $1, state = 'ready' WHERE name = $2",
            values: [code, name],
            rowMode: 'array',
        }

        try {
            console.log(q.text)
            await postgresClient.query(q)
        } catch (e) {
            console.log(e)
            res.redirect('/')
        }
    }

    res.redirect('/game')

});

app.get('/game', (req, res) => {
    res.sendFile(__dirname + '/game.html');
});

app.get('/register', (req, res) => {
    res.sendFile(__dirname + '/register.html');
});

app.post('/register', async (req, res) => {
    if (req.body.name) {
        let key = helpers.makeKey(6)
        const q = {
            text: "INSERT INTO players (name, code) VALUES ($1, $2)",
            values: [req.body.name, key],
            rowMode: 'array',
        }

        try {
            await postgresClient.query(q)
            res.send(key)
        } catch (e) {
            console.log(e)
            res.redirect('/register')
        }
    }
    else {
        res.redirect('/register')
    }

});

app.use('/static', express.static(__dirname + '/static'))

io.on('connection', (socket) => {
    connections.push(socket)

    console.log(`Client with id ${socket.id} connected`)

    socket.on('disconnect', async () => {
        connections = connections.filter(e => e.id !== socket.id)
        console.log(`Client with id ${socket.id} disconnected`)
    })
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});