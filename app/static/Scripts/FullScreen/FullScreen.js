$(document).ready(function () {
    $('#fullscreen-button').on('click', function () {
        toggleFullScreen();
    });

    function toggleFullScreen() {
        if (!document.fullscreenElement &&
            !document.mozFullScreenElement &&
            !document.webkitFullscreenElement &&
            !document.msFullscreenElement) {
            // Enter fullscreen
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            } else if (document.documentElement.msRequestFullscreen) {
                document.documentElement.msRequestFullscreen();
            } else if (document.documentElement.mozRequestFullScreen) {
                document.documentElement.mozRequestFullScreen();
            } else if (document.documentElement.webkitRequestFullscreen) {
                document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
            }
            $('#fullscreen-button i').removeClass('fa-expand-arrows-alt white-icon').addClass('fa-compress-arrows-alt white-icon'); // Change icon to exit fullscreen
        } else {
            // Exit fullscreen
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            }
            $('#fullscreen-button i').removeClass('fa-compress-arrows-alt white-icon').addClass('fa-expand-arrows-alt white-icon'); // Change icon to enter fullscreen
        }
    }

    $(document).on('fullscreenchange mozfullscreenchange webkitfullscreenchange msfullscreenchange', function () {
        if (!document.fullscreenElement &&
            !document.mozFullScreenElement &&
            !document.webkitFullscreenElement &&
            !document.msFullscreenElement) {
            $('#fullscreen-button i').removeClass('fa-compress-arrows-alt white-icon').addClass('fa-expand-arrows-alt white-icon');
        } else {
            $('#fullscreen-button i').removeClass('fa-expand-arrows-alt white-icon').addClass('fa-compress-arrows-alt white-icon');
        }
    });
});