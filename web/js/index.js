jQuery(function($) {
    var form = $('#login-form')
    var formFields = form.find('input, select, textarea')
    var formSubmit = form.find('button[type="submit"]')
    var formRegister = null

    form.on('submit', function(e) {
        e.preventDefault()

        var $targ = $(e.target)

        if ($targ.hasClass('create')) {
            api.query('GET', '/api/register', formFields.serialize())
                .done(function(json) {
                    $targ.apiNotify(json, '/question1')
                })
        } else {
            api.query('POST', '/api/login', formFields.serialize())
                .done(function(json) {
                    if (!json.status) {
                        $targ.apiNotify(json)
                        if (json.data && json.data.button && !formRegister) {
                            formRegister = $('<button>')
                                .prop('type', 'submit')
                                .addClass('create')
                                .text('Join')
                                .insertAfter(formSubmit)
                        }
                    } else {
                        $targ.apiNotify(json, json.data.next)
                    }
                })
        }
    })
})