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

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.set("view engine","ejs");
require('dotenv').config()
var cookieParser = require('cookie-parser');
app.use(cookieParser());


const postgresClient = new  pg.Client({
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
    try {
        var login = req.cookies.login;
        var pass = req.cookies.pass;
        res.redirect("/team/" + login + "/" + pass);
    }
    catch(e) {
        console.log("login error:");
        console.log(e);
        res.sendFile(__dirname + '/views/index.html');
    }
});

app.post('/', async (req, res) => {
    if (req.body.login & req.body.pass) {
        try {
            res.redirect('/team/' + req.body.login + "/" + req.body.pass);
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
    res.sendFile(__dirname + '/views/game.html');
});

app.get('/register', (req, res) => {
    res.sendFile(__dirname + '/views/register.html');
});

app.post('/register', async (req, res) => {
    if (req.body.name) {
        const q = {
            text: "INSERT INTO players (name, login, password) VALUES ($1, $2, $3)",
            values: [req.body.name, req.body.login, req.body.pass],
            rowMode: 'array',
        }

        try {
            const res_ = await postgresClient.query("SELECT * FROM players WHERE name = '" + req.body.name + "'");
            if(res_.rows.length > 0) {
                alert("Такое название уже занято!");
            }
            else {
                res.cookie('login', req.body.login, {expire: 360000 + Date.now()});
                res.cookie('pass', req.body.pass, {expire: 360000 + Date.now()});
                await postgresClient.query(q);
                res.redirect("/");
            }
        } catch (e) {
            console.log("register error:")
            console.log(e);
            res.redirect('/register');
        }
    }
    else {
        res.redirect('/register');
    }

});

app.get('/team/:login/:pass', async (req, res) => {
    try {
        const res_ = await postgresClient.query("SELECT * FROM players WHERE login = '" + req.params.login + "' AND password = '" +
        req.params.pass + "'");
        res.cookie('login', req.params.login, {expire: 360000 + Date.now()});
        res.cookie('pass', req.params.pass, {expire: 360000 + Date.now()});
        res.render('team', {name: res_.rows[0].name, code: res_.rows[0].code});
    }
    catch(e) {
        console.log("home error:");
        console.log(e);
        res.redirect('/');
        alert("Неверный логин/пароль");
    }
});

app.post('/team/:login/:pass', async (req, res) => {
    if (req.body.script) {
         const q = {
            text: "UPDATE players SET code = $1 WHERE login = $2 AND password = $3",
            values: [req.body.script, req.params.login, req.params.pass],
            rowMode: 'array',
        }
        try {
            await postgresClient.query(q);
            res.redirect('/team/' + req.params.login + '/' + req.params.pass);
        } catch (e) {
            console.log(e)
            res.redirect('/')
        }
    }
    else {
        res.redirect('/team/' + req.params.login + '/' + req.params.pass);
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