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
}

init_redis()

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/', async (req, res) => {
    if (req.body.key && req.body.script) {
        const q = {
            text: "UPDATE players SET code = $1, state = 'ready' WHERE key = $2",
            values: [req.body.script, req.body.key],
            rowMode: 'array',
        }

        try {
            await postgresClient.query(q)
            res.redirect('/game')
        } catch (e) {
            console.log(e)
            res.redirect('/')
        }
    }
    else {
        res.redirect('/')
    }


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
            text: "INSERT INTO players (name, key) VALUES ($1, $2)",
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