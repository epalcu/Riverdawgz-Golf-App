var updatePositions = function() {
    $.ajax({
        url: "/home/update",
        type: "GET",
        cache: false,
        contentType: false,
        processData: false,
        success: function(m) {
            window.location.href="/home";
        }
    });
};

var interval = 1000 * 60 * 1;

setInterval(updatePositions, interval);