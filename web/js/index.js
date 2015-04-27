jQuery(function($) {
    var form = $('#login-form')
    var formFields = form.find('input, select, textarea')
    var formSubmit = form.find('button[type="submit"]')
    
    form.on('submit', function(e) {
        e.preventDefault()

        if (formSubmit.hasClass('create')) {
            api.query('GET', '/api/register', formFields.serialize())
                .done(function(json) {
                    formSubmit.apiNotify(json, '/question1')
                })
        } else {
            api.query('POST', '/api/login', formFields.serialize())
                .done(function(json) {
                    if (!json.status) {
                        formSubmit.apiNotify(json)
                        if (json.data && json.data.button) {
                            formSubmit.text(json.data.button)
                            formSubmit.addClass('create')
                        }
                    } else {
                        formSubmit.apiNotify(json, json.data.next)
                    }
                })
        }
    })
})