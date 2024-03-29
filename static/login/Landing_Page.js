$(function () {
    $('a.smoothScroll').on('click', function () {

        var $link = $(this);
        var $destination = $($link.attr('href'));
        var destination_position = $destination.position().top;

        $('html, body').animate(
            {
                scrollTop: destination_position
            }, 1200);

        return false
    });
});

var images = new Array({ % static
'pages/100.png' %
},
{%
    static
    'pages/101.png' %
}
,
{%
    static
    'pages/102.png' %
}
,
{%
    static
    'pages/103.png' %
}
,
{%
    static
    'pages/104.png' %
}
)
;

function rotateLeft() {
    var current_image = document.getElementById("profile_image").src;
    var i = current_image.charAt(current_image.length - 9);

    if (i == 0) {
        prev = 4;
    }
    else {
        prev = i - 1;
    }


    document.getElementById("profile_image").style.right = -320 + "px";


    document.getElementById("profile_image").src = images[prev];
    document.getElementById("profile_image").style.left = 0 + "px";

}

function rotateRight() {
    var current_image = document.getElementById("profile_image").src;
    var i = current_image.charAt(current_image.length - 9);

    if (i == 4) {
        i = 0;
    }
    else {
        i++;
    }

    document.getElementById("profile_image").src = images[i];
}
