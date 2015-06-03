$(document).ready(function() {
    var MAX_CAPACITY = 6;
    var namespace = '/server';

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        console.log('client connected!');
    });

    socket.on('response', function(msg) {
        $('#log').append('<li>' + msg.data + '</li>');
    });

    socket.on('load_rooms', function(data) {
        displayRooms(data.rooms);
    });

    socket.on('update_room', function(room) {
        updateRoom(room);
    });


    // Renders HTML for each room
    function displayRooms(rooms) {
        $('#rooms').empty();
        for (var i = 0; i < rooms.length; i++) {
            var roomHTML = '<div id="room-' + rooms[i].id + '">' +
                             '<h4 class="room-name">a</h4>' +
                             '<p class="room-users">b</p>' +
                             '<p class="room-capacity">c</p>' +
                             '<a class="room-join" href="squash/room/' + rooms[i].id + '">Join</a>' +
                           '</div>';
            $('#rooms').append(roomHTML);
            updateRoom(rooms[i]);
        }
    }

    // Update name, users, and capacity text
    function updateRoom(room) {
        var $room = $('#room-' + room.id);
        var capacity = room.users.length;
        $room.children('.room-name').text(room.name);
        $room.children('.room-users').text('Users: ' + room.users.join(', '));
        $room.children('.room-capacity').text('Capacity: ' + capacity.toString() + (capacity == MAX_CAPACITY ? ' (FULL)' : ''));
        if (capacity == MAX_CAPACITY) {
            $room.children('.room-join').prop('disabled', true); // disable link
        }
    }
});
