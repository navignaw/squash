$(document).ready(function() {
    var namespace = '/server';

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('client_connect', {data: 'Client connected'});
    });

    socket.on('response', function(msg) {
        $('#log').append('<li>' + msg.data + '</li>');
    });

});
