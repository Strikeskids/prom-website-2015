;(function($) {
    var B = function() {
    }

    function notifyClass(data) {
        switch (data.status) {
            case 0:
            case false:
            case 'error':
                return 'error'
            case 1:
            case true:
            case 'success':
                return 'success'
            default:
                return 'info'            
        }
    }

    B.prototype.notify = function(data, redirect, config) {
        var dataClass = notifyClass(data)
        config = config || {}
        config.className = config.className || dataClass
        var ret = $.notify(data.message, config)
        if (redirect && dataClass === 'success') {
            setTimeout(function() {
                window.location = redirect
            }, 1000)
        }
        return ret
    }

    B.prototype.query = function(type, url, data) {
        data = data || {}
        if (type === 'POST') {
            data.token = $.cookie('token')
        }
        return $.ajax({
            cache: false,
            dataType: 'json',
            url: url,
            type: type,
            data: data,
        })
            .fail(function() {
                api.notify({
                    message: "The server is currently down. Don't worry. We're trying to fix it.",
                    status: 0,
                })
            })
    }

    B.prototype.logout = function() {
        api.query('GET', '/api/logout')
            .done(function(data) {
                window.location = data.status ? '/' : '/login'
            })
    }

    jQuery.fn.serialize = function() {
        var keys = {}
        this.each(function() {
            if (this.name && this.value) {
                keys[this.name] = this.value
            }
        })
        return keys
    }

    jQuery.fn.apiNotify = function(data, redirect, config) {
        var dataClass = notifyClass(data)
        config = config || {}
        config.className = config.className || dataClass
        config.position = config.position || 'bottom center'
        var ret = $(this).notify(data.message, config)
        if (redirect && dataClass === 'success') {
            setTimeout(function() {
                window.location = redirect
            }, 1000)
        }
        return ret
    }

    window.api = new B()
})(jQuery)

jQuery(function($) {
    var statusChecks = api.statusChecks || []

    function checkHardRedirects() {
        statusChecks.forEach(function(check) {
            if (check.hard) {
                setTimeout(function() {
                    window.location = check.url
                }, 1000)
            }
        })
    }

    function toggleSessionStateClasses() {
        $(document.body).toggleClass('logged-in', $.cookie('logged_in') === 'true')
    }

    toggleSessionStateClasses()

    api.query('GET', '/api/status')
        .done(function(data) {
            if (data.status === 1) {
                api.userStatus = data.data
                statusChecks.forEach(function(check) {
                    if (check.key === 'question') {
                        if (data.data.num+1 < check.state) {
                            api.notify(
                                {status:1, message:'You need to solve the previous questions first'},
                                '/question'+(data.data.num+1),
                                {className: 'error'}
                            )
                        }
                    } else if (!!data.data[check.key] === !!check.state) {
                        window.location = check.url
                    }
                })
                $.cookie('logged_in', !!data.data.logged_in)
                toggleSessionStateClasses()
            } else {
                checkHardRedirects()
            }
        })
        .fail(checkHardRedirects)

    $('.pseudo-select').each(function() {
        var $el = $(this)
        var inp = $('<input>')
            .prop('name', $el.data('name'))
            .prop('type', 'hidden')
            .insertAfter($el)
        var prev = null
        $el.children('div')
            .on('click', function(e) {
                var $targ = $(e.target)
                inp.val($targ.data('value'))
                if (prev) {
                    prev.removeClass('selected')
                }
                prev = $targ.addClass('selected')
            })
    })
})
