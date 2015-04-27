jQuery(function($) {
    var form = $('#question-form')
    var formFields = form.find('input, select, textarea')
    var formSubmit = form.find('button[type="submit"]')

    form.on('submit', function(e) {
        e.preventDefault()
        api.query('POST', '/api/question', formFields.serialize())
            .done(function(json) {
                if (!json.status) {
                    formSubmit.apiNotify(json)
                } else {
                    formSubmit.apiNotify(json, json.data.url)
                }
            })
    })
})
