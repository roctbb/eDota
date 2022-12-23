const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const {Server} = require("socket.io");
const io = new Server(server);
const redis = require('redis');

let connections = []

const init_redis = async () => {

    const client = redis.createClient();
    const subscriber = client.duplicate();
    await subscriber.connect();

    await subscriber.subscribe('edota_frame', (message) => {
        console.log("message from redis")
        connections.forEach(socket => {
            socket.emit('frame', message)
        })
    });
}

init_redis()

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.use('/static', express.static('static'))

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