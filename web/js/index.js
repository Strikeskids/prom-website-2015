jQuery(function($) {
    var form = $('#login-form')
    var formFields = form.find('input, select, textarea')
    var formSubmit = form.find('button[type="submit"]')
    var formRegister = form.find('button[type="button"]')
    
    formRegister.on('click', function(e) {
        e.preventDefault()

        if (!form[0].checkValidity()) {
            formSubmit.trigger('click')
            return
        }

        api.query('POST', '/api/register', formFields.serialize())
            .done(function(json) {
                formRegister.apiNotify(json, '/question1')
            })
    })

    form.on('submit', function(e, skip) {
        e.preventDefault()

        api.query('POST', '/api/login', formFields.serialize())
            .done(function(json) {
                formSubmit.apiNotify(json, json.data && json.data.next)
            })
    })
})
