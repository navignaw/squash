$(document).ready(function() {
    var namespace = '/server';
    // TODO: for testing, just randomly pick a username. later let them customize
    var username = ['david', 'albert', 'ivan', 'fat'][Math.floor(Math.random() * 4)];
    $('#username').text('Hello, ' + username);


    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('client_connect', {data: 'Client connected'});
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
                $('#join-' + room.name).prop('disabled', true); // disable button
                socket.emit('join_room', {'room': room.name, 'username': username});
                // TODO: switch views
            };
        };

        $('#rooms').empty();
        for (var i = 0; i < rooms.length; i++) {
            var roomHTML = '<div id="#' + rooms[i].name + '">' +
                             '<h4 class="room-name"></h4>' +
                             '<p class="room-users"></p>' +
                             '<p class="room-capacity"></p>' +
                             '<button type="button" class="button" id="#join-' + rooms[i].name + '">Join</button>' +
                           '</div>';
            $('#rooms').append(roomHTML);
            $('#join-' + rooms[i].name).click(joinRoom(rooms[i]));
            updateRoom(rooms[i]);
        }
    }

    // Update name, users, and capacity text
    function updateRoom(room) {
        var $room = $('#rooms #' + room.name);
        $room.children('.room-name').text(room.name);
        $room.children('.room-users').text('Users: ' + room.users.join(', '));
        $room.children('.room-capacity').text('Capacity: ' + room.users.length.toString());
    }
});
