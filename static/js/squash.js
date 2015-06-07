$(document).ready(function() {
    var MAX_CAPACITY = 6;
    var namespace = '/squash';
    var gameBegan = false;
    var room_id = $('#room-id').val();

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        console.log('client connected!');
    });

    socket.on('response', function(msg) {
        $('#log').append('<li>' + msg.data + '</li>');
    });

    socket.on('update_room', function(room) {
        updateRoom(room);
    });


    // Update name, users, and capacity text
    function updateRoom(room) {
        var $room = $('#room');
        var capacity = room.users.length;
        $room.find('.room-name').text(room.name);
        $room.find('.room-users').text('Users: ' + room.users.join(', '));
        if (capacity === MAX_CAPACITY) {
            // TODO: ready to begin game
            if (!gameBegan) {
                $room.find('#game-status').text('Ready to begin!');
                gameBegan = true;
            }
        } else {
            $room.find('#game-status').text(
                'Waiting for ' + (MAX_CAPACITY - capacity).toString() +
                ' more players...'
            );
            if (gameBegan) {
                // TODO: uh oh, we lost a player. pause or forfeit the game?
            }
        }
    }

    // Leave room when player leaves page.
    $('#leave-room').click(function() {
        socket.emit('leave_room', {room: room_id});
    });
});
