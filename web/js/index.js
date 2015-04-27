jQuery(function($) {
    var form = $('#login-form')
    var formFields = form.find('input, select, textarea')
    var formSubmit = form.find('button[type="submit"]')
    var formRegister = null
    
    var register = function(e) {
        e.preventDefault()

        api.query('POST', '/api/register', formFields.serialize())
            .done(function(json) {
                formRegister.apiNotify(json, '/question1')
            })
    }
    

    form.on('submit', function(e) {
        e.preventDefault()

        api.query('POST', '/api/login', formFields.serialize())
            .done(function(json) {
                if (!json.status) {
                    formSubmit.apiNotify(json)
                    if (json.data && json.data.button && !formRegister) {
                        formRegister = $('<button>')
                            .prop('type', 'button')
                            .text('Join')
                            .on('click', register)
                            .css('margin-left', '20px')
                            .insertAfter(formSubmit)
                    }
                } else {
                    formSubmit.apiNotify(json, json.data.next)
                }
            })
    })
})
