console.log(Cookies.get('csrftoken'))
    console.log($('#createForm').serialize())

    $('#createForm').on("submit", function(e){
        e.preventDefault()
        var str = $(this).serialize()
        console.log((str))
        $.ajax({
            url: 'http://localhost:8000/api/v1/create/',
            type: 'POST',
            headers: {'Authorization': 'Token ' + localStorage.getItem('token')},
            headers: {'X-CSRFToken':Cookies.get('csrftoken')},
            data: str,
            success: function (result) {
                location.reload()
                console.log(result)}
        });
    })