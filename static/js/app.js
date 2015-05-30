$(document).ready(function() {
    var MAX_CAPACITY = 6;
    var namespace = '/server';

    // TODO: for testing, just randomly pick a username. later let them customize
    var username = ['david', 'albert', 'ivan', 'fat'][Math.floor(Math.random() * 4)];
    $('#username').text('Hello, ' + username);


    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('client_connect', {'username': username});
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
        var joinRoom = function(room) {
            return function() {
                var $room = $('#room-' + room.id);
                $room.children('.join-button').prop('disabled', true); // disable button
                socket.emit('join_room', {'room': room.id});
                // TODO: switch views
            };
        };

        $('#rooms').empty();
        for (var i = 0; i < rooms.length; i++) {
            var roomHTML = '<div id="room-' + i + '">' +
                             '<h4 class="room-name">a</h4>' +
                             '<p class="room-users">b</p>' +
                             '<p class="room-capacity">c</p>' +
                             '<button type="button" class="join-button" id="join-' + rooms[i].id + '">Join</button>' +
                           '</div>';
            $('#rooms').append(roomHTML);
            $('#join-' + rooms[i].id).click(joinRoom(rooms[i]));
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
            $room.children('.join-button').prop('disabled', true); // disable button
        }
    }
});
