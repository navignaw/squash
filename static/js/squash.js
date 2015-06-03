$(document).ready(function() {
    var namespace = '/squash';

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        console.log('client connected!');
    });

    socket.on('response', function(msg) {
        $('#log').append('<li>' + msg.data + '</li>');
    });

    socket.on('load_room', function(room) {
        displayRoom(room);
    });

    socket.on('update_room', function(room) {
        updateRoom(room);
    });


    // Renders HTML for each room
    function displayRoom(room) {
        var roomHTML = '<h4 class="room-name">a</h4>' +
                       '<p class="room-users">b</p>';
        $('#room').append(roomHTML);
        updateRoom(room);
    }

    // Update name, users, and capacity text
    function updateRoom(room) {
        var $room = $('#room');
        var capacity = room.users.length;
        $room.children('.room-name').text(room.name);
        $room.children('.room-users').text('Users: ' + room.users.join(', '));
    }
});
