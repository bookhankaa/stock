// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/items',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(vendor_code, uuid) {
            let ajax_options = {
                type: 'POST',
                url: 'api/items',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'vendor_code': vendor_code,
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(vendor_code, uuid) {
            let ajax_options = {
                type: 'PUT',
                url: 'api/items/' + uuid,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    'vendor_code': vendor_code,
                    'uuid': uuid
                })
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(uuid) {
            let ajax_options = {
                type: 'DELETE',
                url: 'api/items/' + uuid,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $vendor_code = $('#vendor_code'),
        $uuid = $('#uuid');

    // return the API
    return {
        reset: function() {
            $uuid.val('');
            $vendor_code.val('').focus();
        },
        update_editor: function(vendor_code, uuid) {
            $uuid.val(uuid);
            $vendor_code.val(vendor_code).focus();
        },
        build_table: function(items) {
            let rows = ''

            $('.items table > tbody').empty();

            if (items) {
                for (let i=0, l=items.length; i < l; i++) {
                    rows += `<tr>
                    <td class="vendor_code">${items[i].vendor_code}</td>
                    <td class="uuid">${items[i].uuid}</td>
                    `;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $vendor_code = $('#vendor_code'),
        $uuid = $('#uuid');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(vendor_code, uuid) {
        return vendor_code !== "" && uuid !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let vendor_code = $vendor_code.val(),
            uuid = $uuid.val();

        e.preventDefault();

        if (validate(vendor_code)) {
            model.create(vendor_code)
        } else {
            view.error('Problem with input');
        }
    });

    $('#update').click(function(e) {
        let vendor_code = $vendor_code.val(),
            uuid = $uuid.val();

        e.preventDefault();

        if (validate(vendor_code, uuid)) {
            model.update(vendor_code, uuid)
        } else {
            view.error('Problem with input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let uuid = $uuid.val();

        e.preventDefault();

        if (validate('placeholder', uuid)) {
            model.delete(uuid)
        } else {
            view.error('Problem with input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            vendor_code,
            uuid;

        vendor_code = $target
            .parent()
            .find('td.vendor_code')
            .text();

        uuid = $target
            .parent()
            .find('td.uuid')
            .text();

        view.update_editor(vendor_code, uuid);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));


